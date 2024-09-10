# Kafka Sink
Kafka is the most sophisticated Sink available.


## Basic Configuration
A basic Kafka Sender is configured as follows:
```yaml
bootstrapServer: localhost:9092
topic: input
```

The `bootstrapServer` takes the URL of the bootstrap server of the kafka cluster.
`topic` defines the topic to send messages to.

## Partitioning
It supports [Partitioning](partition/README.md)