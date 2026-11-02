import unittest

from distributed_event_factory.parser.postprocessor.drop_rate_post_processor_parser import DropRatePostProcessorParser
from distributed_event_factory.parser.postprocessor.missing_data_post_processor_parser import MissingDataPostProcessorParser
from distributed_event_factory.parser.postprocessor.post_processor_bundle_parser import PostProcessorBundleParser
from distributed_event_factory.parser.postprocessor.post_processor_parser import PostProcessorParser
from distributed_event_factory.provider.postprocessor.drop_rate_post_processor import DropRatePostProcessor
from distributed_event_factory.provider.postprocessor.missing_data_post_processor import MissingDataPostProcessor


class PostProcessorBundleParserTest(unittest.TestCase):
    def setUp(self):
        post_processor_parser = (PostProcessorParser()
                                 .add_dependency("dropRate", DropRatePostProcessorParser())
                                 .add_dependency("missingData", MissingDataPostProcessorParser()))
        self.parser = PostProcessorBundleParser().add_dependency("postProcessor", post_processor_parser)

    def test_parses_processors_in_configuration_order(self):
        parsed = self.parser.parse({
            "processors": [
                {"name": "drop", "type": "dropRate", "dropRate": 0.25},
                {"name": "missing", "type": "missingData", "payloadProbability": 0.1},
            ]
        })

        self.assertEqual(["drop", "missing"], list(parsed))
        self.assertIsInstance(parsed["drop"], DropRatePostProcessor)
        self.assertIsInstance(parsed["missing"], MissingDataPostProcessor)

    def test_rejects_duplicate_processor_names(self):
        with self.assertRaisesRegex(ValueError, "Duplicate post processor name"):
            self.parser.parse({
                "processors": [
                    {"name": "same", "type": "dropRate", "dropRate": 0.1},
                    {"name": "same", "type": "dropRate", "dropRate": 0.2},
                ]
            })

    def test_rejects_missing_processor_name(self):
        with self.assertRaisesRegex(ValueError, "non-empty name"):
            self.parser.parse({"processors": [{"type": "dropRate", "dropRate": 0.1}]})

    def test_rejects_non_list_processors(self):
        with self.assertRaisesRegex(ValueError, "must be a list"):
            self.parser.parse({"processors": {"drop": {"type": "dropRate", "dropRate": 0.1}}})


if __name__ == "__main__":
    unittest.main()
