import unittest
from unittest.mock import patch

from distributed_event_factory.parser.postprocessor.insertion_post_processor_parser import InsertionPostProcessorParser
from distributed_event_factory.parser.postprocessor.missing_data_post_processor_parser import MissingDataPostProcessorParser
from distributed_event_factory.parser.postprocessor.out_of_order_post_processor_parser import OutOfOrderPostProcessorParser
from distributed_event_factory.parser.postprocessor.payload_uncertainty_post_processor_parser import PayloadUncertaintyPostProcessorParser
from distributed_event_factory.parser.postprocessor.time_uncertainty_post_processor_parser import TimeUncertaintyPostProcessorParser
from distributed_event_factory.provider.postprocessor.insertion_post_processor import InsertionPostProcessor
from distributed_event_factory.provider.postprocessor.missing_data_post_processor import MissingDataPostProcessor
from distributed_event_factory.provider.postprocessor.out_of_order_post_processor import OutOfOrderPostProcessor
from distributed_event_factory.provider.postprocessor.payload_uncertainty_post_processor import PayloadUncertaintyPostProcessor
from distributed_event_factory.provider.postprocessor.time_uncertainty_post_processor import TimeUncertaintyPostProcessor
from distributed_event_factory.simulation.abstract_simulation import Simulation


class _Event:
    def __init__(self, activity="A1", caseid="case-1"):
        self.activity = activity
        self.caseid = caseid
        self.node = "Node-1"
        self.timestamp = "2025-01-01 00:00:00"
        self.payload = 50.0


class _Simulation(Simulation):
    pass


class _Sink:
    def __init__(self):
        self.events = []

    def send(self, event):
        self.events.append(event)


class AdditionalPostProcessorTest(unittest.TestCase):
    def test_all_new_processor_types_are_registered(self):
        parsed_processors = (
            PayloadUncertaintyPostProcessorParser().parse({"probability": 0.5, "sigma": 1}),
            TimeUncertaintyPostProcessorParser().parse({"probability": 0.5, "sigmaSeconds": 1}),
            MissingDataPostProcessorParser().parse({}),
            OutOfOrderPostProcessorParser().parse({"probability": 0.5, "windowSize": 2}),
            InsertionPostProcessorParser().parse({"probability": 0.5}),
        )
        self.assertEqual(5, len(parsed_processors))

    def test_payload_uncertainty_clamps_payload_range(self):
        processor = PayloadUncertaintyPostProcessor(probability=1.0, sigma=5.0)
        event = _Event()
        with patch("distributed_event_factory.provider.postprocessor.payload_uncertainty_post_processor.random.gauss",
                   return_value=100):
            processor.process(event)
        self.assertEqual(100.0, event.payload)

    def test_time_uncertainty_applies_seconds_offset(self):
        processor = TimeUncertaintyPostProcessor(probability=1.0, sigma_seconds=5.0)
        event = _Event()
        with patch("distributed_event_factory.provider.postprocessor.time_uncertainty_post_processor.random.gauss",
                   return_value=30):
            processor.process(event)
        self.assertEqual("2025-01-01 00:00:30", event.timestamp)

    def test_missing_data_can_remove_each_configured_attribute(self):
        processor = MissingDataPostProcessor(1.0, 1.0, 1.0)
        event = _Event()
        processor.process(event)
        self.assertIsNone(event.payload)
        self.assertIsNone(event.timestamp)
        self.assertIsNone(event.activity)

    def test_out_of_order_reorders_full_windows_and_flushes_partial_window(self):
        processor = OutOfOrderPostProcessor(probability=1.0, window_size=2)
        first, second, third = _Event("A1"), _Event("A2"), _Event("A3")
        self.assertIsNone(processor.process(first))
        with patch("distributed_event_factory.provider.postprocessor.out_of_order_post_processor.random.shuffle",
                   side_effect=lambda events: events.reverse()):
            self.assertEqual([second, first], processor.process(second))
            self.assertIsNone(processor.process(third))
            self.assertEqual([third], processor.flush())

    def test_out_of_order_window_is_shared_across_cases(self):
        processor = OutOfOrderPostProcessor(probability=1.0, window_size=2)
        first = _Event("A1", caseid="case-1")
        second = _Event("A2", caseid="case-2")

        self.assertIsNone(processor.process(first))
        with patch("distributed_event_factory.provider.postprocessor.out_of_order_post_processor.random.shuffle",
                   side_effect=lambda events: events.reverse()):
            self.assertEqual([second, first], processor.process(second))

    def test_insertion_emits_copy_with_alternative_activity(self):
        processor = InsertionPostProcessor(probability=1.0)
        processor.set_transition_alternatives({"Node-1": ["A1", "A2"]})
        event = _Event()
        with patch("distributed_event_factory.provider.postprocessor.insertion_post_processor.random.choice",
                   return_value="A2"):
            result = processor.process(event)
        self.assertEqual(2, len(result))
        self.assertIs(event, result[0])
        self.assertEqual("A2", result[1].activity)
        self.assertIsNot(event, result[1])
        self.assertEqual(event.caseid, result[1].caseid)

    def test_pipeline_passes_inserted_events_to_later_processors(self):
        simulation = _Simulation()
        insertion = InsertionPostProcessor(probability=1.0)
        insertion.set_transition_alternatives({"Node-1": ["A1", "A2"]})
        missing = MissingDataPostProcessor(0.0, 0.0, 1.0)
        simulation.setup_post_processors({"insertion": insertion, "missing": missing})
        with patch("distributed_event_factory.provider.postprocessor.insertion_post_processor.random.choice",
                   return_value="A2"):
            processed = simulation.process_events([_Event()])
        self.assertEqual(2, len(processed))
        self.assertTrue(all(event.activity is None for event in processed))

    def test_simulation_flushes_buffered_events_to_sinks(self):
        simulation = _Simulation()
        simulation.setup_post_processors({
            "outOfOrder": OutOfOrderPostProcessor(probability=0.0, window_size=3),
        })
        sink = _Sink()
        simulation.datasource_sink_mapping["Node-1"] = [sink]
        event = _Event()

        simulation.send_event(event)
        self.assertEqual([], sink.events)
        simulation.flush_post_processors_to_sinks()
        self.assertEqual([event], sink.events)


if __name__ == "__main__":
    unittest.main()
