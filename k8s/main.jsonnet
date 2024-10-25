local load = import 'load.jsonnet';

local a = load.loadDeployment(
    topic="testi",
    bootstrapServer="minikube:1234"
);

local b = load.loadDeployment(
    topic="testi",
    bootstrapServer="minikube:1234"
);

[a]