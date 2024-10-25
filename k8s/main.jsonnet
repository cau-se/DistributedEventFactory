local load = import 'load.jsonnet';

local a = load.loadDeployment(
    namespace="kafka",
    topic="testi",
    bootstrapServer="minikube:1234"
);

[a]