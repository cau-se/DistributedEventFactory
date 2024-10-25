{
   loadDeployment(topic, bootstrapServer):: {
     apiVersion: "apps/v1",
     kind: "Deployment",
     metadata: {
       name: "distributed-event-factory",
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

   loadService():: {

   },
}