{
   loadDefDeployment(namespace, topic, bootstrapServer):: {
     apiVersion: "apps/v1",
     kind: "Deployment",
     metadata: {
       name: "distributed-event-factory",
       namespace: namespace,
       labels: {
         app: "distributed-event-factory"
       }
     },
     spec: {
       replicas: 1,
       selector: {
         matchLabels: {
           app: "distributed-event-factory"
         }
       },
       template: {
         metadata: {
           labels: {
             app: "distributed-event-factory"
           }
         },
         spec: {
           containers: [
             {
               name: "distributed-event-factory",
               image: "hendrikreiter/distributed_event_factory:0.2.0-SNAPSHOT",
               imagePullPolicy: "Always",
               env: [
                 {
                    name: "TOPIC",
                    value: topic
                 },
                 {
                    name: "BOOTSTRAP_SERVER",
                    value: bootstrapServer
                 },
                 {
                    name: "SIMULATION",
                    value: "loadtest"
                 },
                 {
                    name: "DATASOURCE",
                    value: "assemblyline"
                 },
                 {
                    name: "SINK",
                    value: "loadtest-sink"
                 },
                 {
                    name: "ROOT",
                    value: "/app"
                 }
               ],
               ports: [
                 {
                   containerPort: 8080
                 }
               ]
             }
           ]
         }
       }
     }
   },
   loadBackendDeployment(namespace, topic, bootstrapServer):: {
     apiVersion: "apps/v1",
     kind: "Deployment",
     metadata: {
       name: "load-backend",
       namespace: namespace,
       labels: {
         app: "load-backend"
       }
     },
     spec: {
       replicas: 1,
       selector: {
         matchLabels: {
           app: "load-backend"
         }
       },
       template: {
         metadata: {
           labels: {
             app: "load-backend"
           }
         },
         spec: {
           containers: [
             {
               name: "load-backend",
               image: "hendrikreiter/def-loadtest-backend:0.1.0",
               imagePullPolicy: "Always",
               env: [
                 {
                    name: "TOPIC",
                    value: topic
                 },
                 {
                    name: "BOOTSTRAP_SERVER",
                    value: bootstrapServer
                 }
               ],
               ports: [
                 {
                   containerPort: 8080
                 }
               ]
             }
           ]
         }
       }
     }
   },
   loadBackendService(namespace):: {
     apiVersion: "v1",
     kind: "Service",
     metadata: {
        name: "load-backend",
        namespace: namespace
     },
     spec: {
        selector: {
            app: "load-backend"
        },
        ports: [
          {
            port: 8080,
            targetPort: 8080
          }
        ]
     }
   }
}