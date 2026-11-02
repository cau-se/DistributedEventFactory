import unittest
from statistics import mean

from distributed_event_factory.event_factory import EventFactory
from distributed_event_factory.provider.sink.test.test_sink import TestSink
from distributed_event_factory.provider.sink.test.test_sink_parser import TestSinkParser
from distributed_event_factory.simulation.process_simulation import Token


class IntegrationTest(unittest.TestCase):
    def test_integration(self):
        event_factory = EventFactory()
        event_factory.add_sink_parser("test", TestSinkParser())
        (event_factory
         .add_directory(directory="config/datasource/assemblyline")
         .add_file("config/simulation/countbased.yaml")
         .add_file("config/sink/test-sink.yaml")
         .run())
        sink_mock: TestSink = event_factory.get_sink("test")
        self.assertEqual(100, len(sink_mock.event_log))

    def test_integration_with_post_processor_drop_all(self):
        event_factory = EventFactory()
        event_factory.add_sink_parser("test", TestSinkParser())
        (event_factory
         .add_directory(directory="config/datasource/assemblyline")
         .add_file("config/simulation/countbased.yaml")
         .add_file("config/postprocessor/drop-all.yaml")
         .add_file("config/sink/test-sink.yaml")
         .run())
        sink_mock: TestSink = event_factory.get_sink("test")
        self.assertEqual(0, len(sink_mock.event_log))

    def test_integration_payload_aware_selection(self):
        event_factory = EventFactory()
        event_factory.add_sink_parser("test", TestSinkParser())
        (event_factory
         .add_directory(directory="config/datasource/assemblyline-payload")
         .add_file("config/simulation/countbased-payloadaware.yaml")
         .add_file("config/sink/test-sink-payloadaware.yaml")
         .run())
        sink_mock: TestSink = event_factory.get_sink("test-payloadaware")
        self.assertEqual(100, len(sink_mock.event_log))

    def test_payload_clamp(self):
        token = Token("case_1", None, None, None, 50)
        token.update_payload(1000)
        self.assertEqual(100.0, token.payload)
        token.update_payload(-1000)
        self.assertEqual(0.0, token.payload)

    def test_payload_aware_transition_uses_distribution(self):
        event_factory = EventFactory()
        event_factory.add_sink_parser("test", TestSinkParser())
        event_factory.add_directory(directory="config/datasource/assemblyline-payload")

        material_preparation = event_factory.get_datasource("MaterialPreparation")
        provider = material_preparation.get_event_provider()
        low_payload_event = provider.get_event_data(10)
        mid_payload_event = provider.get_event_data(50)
        high_payload_event = provider.get_event_data(99)

        self.assertEqual("AssemblyLineSetup", low_payload_event.get_transition())
        self.assertEqual("MaterialPreparation", mid_payload_event.get_transition())
        self.assertEqual("MaterialPreparation", high_payload_event.get_transition())
        self.assertEqual("Internal Error", high_payload_event.get_activity())

    def test_payload_updates_apply_and_stay_bounded(self):
        event_factory = EventFactory()
        event_factory.add_sink_parser("test", TestSinkParser())
        event_factory.add_directory(directory="config/datasource/assemblyline-payload")
        material_preparation = event_factory.get_datasource("MaterialPreparation")
        provider = material_preparation.get_event_provider()

        payload = 50.0
        payload_values = []
        for _ in range(50):
            event_data = provider.get_event_data(payload)
            payload = min(100.0, max(0.0, payload + event_data.get_payload_delta()))
            payload_values.append(payload)

        self.assertTrue(all(0.0 <= value <= 100.0 for value in payload_values))
        self.assertGreater(mean(payload_values), 0)
