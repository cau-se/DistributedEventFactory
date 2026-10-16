import unittest
from unittest.mock import patch

from distributed_event_factory.parser.postprocessor.transition_mistake_post_processor_parser import (
    TransitionMistakePostProcessorParser,
)
from distributed_event_factory.provider.postprocessor.transition_mistake_post_processor import (
    TransitionMistakePostProcessor,
)


class _Event:
    def __init__(self, node, activity):
        self.node = node
        self.activity = activity
        self.caseid = "case-1"
        self.payload = 42


class TransitionMistakePostProcessorTest(unittest.TestCase):
    def test_configuration_parses_transition_mistake_probability(self):
        parsed = TransitionMistakePostProcessorParser().parse({"probability": 0.1})

        self.assertIsInstance(parsed, TransitionMistakePostProcessor)
        self.assertEqual(0.1, parsed.probability)

    def test_rewrites_to_an_alternative_for_the_same_datasource(self):
        processor = TransitionMistakePostProcessor(probability=1.0)
        processor.set_transition_alternatives({"Node-1": ["A1", "A2"]})
        event = _Event("Node-1", "A1")

        with patch("distributed_event_factory.provider.postprocessor.transition_mistake_post_processor.random.choice",
                   return_value="A2"):
            processed = processor.process(event)

        self.assertIs(event, processed)
        self.assertEqual("A2", processed.activity)
        self.assertEqual("case-1", processed.caseid)
        self.assertEqual(42, processed.payload)

    def test_keeps_event_when_no_alternative_exists_or_mistake_not_selected(self):
        processor = TransitionMistakePostProcessor(probability=1.0)
        processor.set_transition_alternatives({"Node-1": ["A1"]})
        event = _Event("Node-1", "A1")
        self.assertIs(event, processor.process(event))

        processor.probability = 0.0
        processor.set_transition_alternatives({"Node-1": ["A1", "A2"]})
        with patch("distributed_event_factory.provider.postprocessor.transition_mistake_post_processor.random.random",
                   return_value=0.5):
            self.assertIs(event, processor.process(event))
        self.assertEqual("A1", event.activity)

    def test_probability_must_be_between_zero_and_one(self):
        with self.assertRaises(ValueError):
            TransitionMistakePostProcessor(probability=1.1)


if __name__ == "__main__":
    unittest.main()
