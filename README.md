# SENSOR-FLOW-DISTRIBUTION-ENGINE (SFDE)
## About

SFDE, or SENSOR-FLOW-DISTRIBUTION-ENGINE, 
is a tool that empowers users to synthetically create 
distributed systems from sensor networks. 
The primary purpose of this system is to cater to the specific 
demands of Process Mining, a critical field in data analysis.

By harnessing the power of SFDE, users can generate an artificial stream of data. 
This stream serves as a resource for developing, testing, 
and deploying new methods tailored to the domain of distributed process mining. 
In essence, SFDE enables researchers and practitioners to explore and refine their approaches 
in a controlled yet dynamic environment.

## Installation
Requirements:
- Python >= 3.11


Install dependencies:  
``
pip install -r requirements.txt 
``

## Usage


1. Create a new SensorManager and add two SingularValueSensors. A SensorManager holds all Sensors for an environment
```python 
from sensors.sensor_collection import SingleValueSensor
from sensors.sensors import SensorManager

SUPERMARKET_SENSOR_MANAGER: SensorManager = SensorManager()
SUPERMARKET_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Enter Entrance"], "Entrance_and_exit"))
SUPERMARKET_SENSOR_MANAGER.add_sensor(SingleValueSensor(["Enter sweets and snacks"], "Sweets_snacks"))
```

2. Create the transitionmatrix with the TransitionMatrixBuilder class.
It is also possible to create a n*n Matrix where n is amount of Sensors.
The name of the state must be the same as the name of the sensor 

```python
from utils.transition_matrix_builder import TransitionMatrixBuilder

SUPERMARKET_BUILDER = TransitionMatrixBuilder()
SUPERMARKET_BUILDER.add_state("Entrance_and_exit", p=0.0)\
    .to(next_state="Sweets_snacks", p=1, t=(1, 2))

SUPERMARKET_BUILDER.add_state("Sweets_snacks", p=0.0)\
    .to(next_state="Entrance_and_exit", p=0.25, t=(1, 2))
```

3. In the next step, a certain number of nodes can be created. 
    In this example, a Markov chain is used to trigger the sensors.

```python
from behavior_modifier.modifier_list import OutlierBehaviorModifier
from network.markov_chain_node_data_processor import MarkovChainNodeDataProcessor
from network.cluster import Node
from tests.scenarios.supermarket_scenario import SUPERMARKET_BUILDER, SUPERMARKET_SENSOR_MANAGER
from utils.utils_types import OutlierCategory
from typing import List

nodes: List[Node] = []
    
for i in range(5):
    data_processor: MarkovChainNodeDataProcessor = MarkovChainNodeDataProcessor(
        i,
        sensor_manager=SUPERMARKET_SENSOR_MANAGER,
        transition_matrix=SUPERMARKET_BUILDER.to_transition_matrix(),
        duration_matrix=SUPERMARKET_BUILDER.to_duration_matrix()
    )

    node = Node(i, data_processor, cache_length=300)
    
    nodes.append(node)
```

4. To change the behavior of the nodes behavior modifiers can be added

```python
from behavior_modifier.modifier_list import OutlierBehaviorModifier,  RandomizeBehaviorModifier, NoiseBehaviorModifier
from utils.utils_types import OutlierCategory

nodes[0].add_behavior_modifier(
    OutlierBehaviorModifier(OutlierCategory.CONTEXTUAL_OUTLIERS, 0.1)
)
nodes[1].add_behavior_modifier(
    RandomizeBehaviorModifier()
)
nodes[2].add_behavior_modifier(
    NoiseBehaviorModifier(0.1, 0.5)
)
```

5. The last thing that can be done is to create the cluster from the nodes. 
 As second parameter the cluster gets an optional node_join_function. 
 This function gets a list of SensorLogs and returns a single SensorLog. 
 This determines which SensorLogs are passed on per network tick. 
 The list consists of the current data of each node. 
 On this example the list would be five elements, because five nodes were created. 
 If no function is specified, the list of SensorLogs is simply passed without a filter.


```python
from utils.utils_types import SensorLog
from typing import List
import random as rd
from network.cluster import Cluster

def node_join_function(data: List[SensorLog]) -> SensorLog:
    return rd.choice(data)


cluster: Cluster = Cluster(nodes, node_join_function)
cluster.start("localhost:8080", tick_speed=0.5)
```

## Sensors

| Class Name          | Description                                                                                                                   | Input Parameters          | Output                                           |
|---------------------|-------------------------------------------------------------------------------------------------------------------------------|---------------------------|--------------------------------------------------|
| TemperatureSensor   | Represents a temperature sensor that generates random temperature data between -50 and 50°C.                                  | None                      | Generator[float, Any, None]                      |
| GasSensor           | Represents a gas sensor that generates random gas concentration data between 0 and 100 units.                                 | None                      | Generator[float, Any, None]                      |
| BioSensor           | Represents a biological sensor that generates random organism activity data between 0 and 1.                                  | None                      | Generator[float, Any, None]                      |
| CameraSensor        | Represents an optical sensor (camera) that generates random pixel data with specified width and height.                       | width (int), height (int) | Generator[list[tuple[int, int, int]], Any, None] |
| AccelerometerSensor | Represents a motion sensor (accelerometer) that generates random acceleration data for three axes (x, y, z) between -1 and 1. | None                      | Generator[tuple[float, float, float], Any, None] |
| AudioSensor         | Represents an audio sensor that generates random sound level data between 0 and 1.                                            | None                      | Generator[float, Any, None]                      |
| PressureSensor      | Represents a pressure sensor that generates random pressure data between 0 and 1000 units.                                    | None                      | Generator[float, Any, None]                      |
| InfraredSensor      | Represents a proximity sensor (infrared sensor) that generates random proximity data between -273.15 and 1000°C.              | None                      | Generator[float, Any, None]                      |
| WifiSensor          | Represents a WiFi sensor that generates random MAC address and signal strength data.                                          | None                      | Generator[tuple[str, int], Any, None]            |
| SingleValueSensor   | Represents a sensor that generates random data from a given list of elements.                                                 | elements (List[str])      | Generator[Any, Any, None]                        |

## BehaviorModifier

| Class Name                | Description                                                                                                | Input Parameters                                                                                                            | Output                                                      |
|---------------------------|------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------|
| BaseBehaviorModifier      | An abstract base class representing a behavior modifier.                                                   | None                                                                                                                        | None                                                        |
| NoiseBehaviorModifier     | A behavior modifier that adds noise to a list of SensorLog.                                                | frequency (float): The percentage of elements to add noise to.<br>change_value (float): Possibility of changing SensorValue | List[SensorLog]: The modified list with added noise.        |
| OutlierBehaviorModifier   | A behavior modifier that does not modify the cache (placeholder).                                          | type (str): The type of the outlier behavior.<br>frequency (float): The frequency of applying the behavior                  | List[SensorLog]: The original cache (unchanged).            |
| RandomizeBehaviorModifier | A behavior modifier that randomly shuffles the elements in the cache using Fisher-Yates shuffle algorithm. | None                                                                                                                        | List[SensorLog]: The modified cache with shuffled elements. |
