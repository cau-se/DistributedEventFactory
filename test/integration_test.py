import unittest

from distributed_event_factory.event_factory import EventFactory
from distributed_event_factory.provider.sink.test.test_sink import TestSink
from distributed_event_factory.provider.sink.test.test_sink_parser import TestSinkParser


class IntegrationTest(unittest.TestCase):
    def test_integration(self):
        event_factory = EventFactory()
        event_factory.add_sink_parser("test", TestSinkParser())
        (event_factory
         .add_directory(directory="config/assemblyline/datasource")
         .add_directory(directory="test/test_files")
         .run())
        sink_mock: TestSink = event_factory.get_sink("test")
        self.assertEqual(100, len(sink_mock.event_log))
