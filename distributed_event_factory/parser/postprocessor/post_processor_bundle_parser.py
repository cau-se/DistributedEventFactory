from distributed_event_factory.parser.parser import Parser


class PostProcessorBundleParser(Parser):
    def __init__(self):
        self.dependencies = {}

    def add_dependency(self, key: str, dependency):
        self.dependencies[key] = dependency
        return self

    def parse(self, config):
        processors = config["processors"]
        if not isinstance(processors, list):
            raise ValueError("PostProcessorBundle spec.processors must be a list")

        parsed_processors = {}
        for processor in processors:
            if not isinstance(processor, dict):
                raise ValueError("Each processor in a PostProcessorBundle must be a mapping")
            name = processor.get("name")
            if not isinstance(name, str) or not name.strip():
                raise ValueError("Each processor in a PostProcessorBundle must have a non-empty name")
            if name in parsed_processors:
                raise ValueError(f"Duplicate post processor name in bundle: {name}")

            processor_config = {key: value for key, value in processor.items() if key != "name"}
            parsed_processors[name] = self.dependencies["postProcessor"].parse(processor_config)

        return parsed_processors
