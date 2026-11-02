from distributed_event_factory.parser.parser import Parser


class SinkBundleParser(Parser):
    def __init__(self):
        self.dependencies = {}

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        sinks = config["sinks"]
        if not isinstance(sinks, list):
            raise ValueError("SinkBundle spec.sinks must be a list")

        parsed_sinks = {}
        for sink in sinks:
            if not isinstance(sink, dict):
                raise ValueError("Each sink in a SinkBundle must be a mapping")
            name = sink.get("name")
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Each sink in a SinkBundle must have a non-empty name")
            if name in parsed_sinks:
                raise ValueError(f"Duplicate sink name in bundle: {name}")

            sink_config = {key: value for key, value in sink.items() if key != "name"}
            parsed_sinks[name] = self.dependencies["sink"].parse(sink_config)

        return parsed_sinks
