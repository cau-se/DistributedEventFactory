from provider.sink.kafka.partition.partition_provider import ConstantPartitionProvider, CaseIdPartitionProvider


class PartitionProviderRegistry:

    def get(self, config):
        registry = dict()
        registry["constant"] = lambda config: ConstantPartitionProvider(config["number"])
        registry["caseId"] = lambda config: CaseIdPartitionProvider(config["numberPartitions"])
        return registry[config["type"]](config)