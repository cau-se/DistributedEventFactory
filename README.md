# Distributed Event Factory (DEF)

![Factory](factory.png)

## About

The Distributed Event Factory (DEF) is a simulation tool for Distributed Process Mining.
It is designed for simulating real world processes utilizing Markov chains.
It produces events consisting of *caseId*, *activity* and *timestamp* on distributed event sources.
In contrast to traditional process mining, multiple independent event streams are generated instead of a single large
one.

## Who should use the DEF?

DEF mainly targets researchers who like to test and evaluate distributed data mining algorithms.
It is suited for generating data at large scale. So, it can be leveraged for benchmarking and load testing.

## Motivation

The Distributed Event Factory was designed for testing and evaluating Distributed Process Mining Algorithms.
A use case for the tool is the simulation of a smart factory with multiple production facilities.
Each Sensor writes its own event logs. On this data process mining should be applied.
We use such a factory as a running example for configuring the DEF.

## Core concepts

DEF is based on a Markov chain. The vertices of the Markov chain represent the distributed data sources.
The edges represent transitions between the data sources. They contain a probability for transitioning, the activity
performed
and a function modelling the process duration.  
![Markov Chain](markov.png)

## Minimal Running Example

The DEF is configured via a yaml file. A minimal running example is presented here

```yaml
numberOfDataSources:
  type: static
  count: 7
caseId: increasing
type: load
loadType: constant
tickCount: 100
load: 10
dataSourceTopology:
  defaultSink:
    type: console
  dataSources:
    - name: "GoodsDelivery"
      groupId: "factory"
      eventGeneration:
        selection: genericProbability
        distribution: [ 0.1, 0.7, 0.2 ]
        from:
          events:
            - activity: "Reject"
              transition: 7
              duration: 1
```

The configuration of the DEF can be separated into two parts:
simulation configuration and the datasource topology.

### Simulation Configuration

`type:` Describes how the simulation is run. Currently, the values `debug` and `load` are supported.
The `load` type gives the possibility to define how the fast the simulation is running.
The `debug` option should be used for development and produces more verbose stacktraces.

`caseId:` Defines a strategy how the caseIds are generated

`loadType`: Defines the function which describes the load. In this example it is set to a `constant` load function.

`load`: Describes the speed the simulation is running

### Data Source Topology

The data sources are defined via a Markov chain. The Markov Chain is configured in a distributed fashion.
Each data source knows its successor. On every edge a duration, a generated activity and the next invoked datasource is
defined. More details can be found [here](src/distributed_event_factory/provider/datasource/README.md)

## Installation

Requirements:
- Python >= 3.10

Install dependencies:
```shell
pip install -r requirements.txt
```

### Start the Programm

Define the `Distribted Event Factory` and specify a config file like mentioned above.

```python
from simulation.distributed_event_factory import DistributedEventFactory

config_file = "src/distributed_event_factory/config/assembly_line.yml"
DistributedEventFactory(config_file).start()
```

