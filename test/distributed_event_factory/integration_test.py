import unittest

from distributed_event_factory.event_factory import EventFactory
from distributed_event_factory.provider.sink.test.test_sink import TestSink
from distributed_event_factory.provider.sink.test.test_sink_parser import TestSinkParser


class IntegrationTest(unittest.TestCase):

    def test_integration(self):
        event_factory = EventFactory()
        event_factory.add_sink_parser("test", TestSinkParser())
        event_factory.run(directory="test_file")
        sink_mock: TestSink = event_factory.get_datasource("test")
        sink_mock.contains_event(None)


if __name__ == '__main__':
    unittest.main()
