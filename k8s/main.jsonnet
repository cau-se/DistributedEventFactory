local load = import 'load.jsonnet';
local flink = import 'flink.jsonnet';
local kafkaNamespace = "kafka";
local inputTopic = "testi";
local bootstrapServer = "my-cluster-kafka-bootstrap:9092";

local defDeployment = load.loadDefDeployment(
    namespace=kafkaNamespace,
);

local defBackendDeployment = load.loadBackendDeployment(
    namespace=kafkaNamespace,
    topic=inputTopic,
    bootstrapServer=bootstrapServer
);

local defBackendService = load.loadBackendService(kafkaNamespace);

local flinkDeployment = flink.heuristicsMinerFlinkDeployment(
    namespace = kafkaNamespace,
    bootstrapServer = bootstrapServer,
    inputTopic = inputTopic,
    modelTopic = "model",
    group = "heuristics-miner",
    parallelism = "1",
    sampleSize = "200",
    batchSize = "100",
    andThreshold = "0.5",
    dependencyThreshold = "0.5"
);

[defDeployment, defBackendDeployment, defBackendService, flinkDeployment]