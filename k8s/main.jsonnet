local load = import 'load.jsonnet';
local kafkaNamespace = "kafka";

local defDeployment = load.loadDefDeployment(
    namespace=kafkaNamespace,
    topic="testi",
    bootstrapServer="minikube:1234"
);

local defBackendDeployment = load.loadBackendDeployment(
    namespace=kafkaNamespace,
    topic="testi",
    bootstrapServer="minikube:1234"
);

local defBackendService = load.loadBackendService(kafkaNamespace);

[defDeployment, defBackendDeployment, defBackendService]