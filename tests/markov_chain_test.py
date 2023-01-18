import datetime
from sensors.sensor_collection import simulate_temperature_sensor, simulate_gas_sensor, simulate_biosensor, \
    simulate_camera_sensor, simulate_accelerometer_sensor, simulate_microphone_sensor, simulate_pressure_sensor, \
    simulate_infrared_sensor, simulate_wifi_sensor, simulate_single_value_sensor
from utils.markov_chain import MarkovChain
from utils.types import SensorLog
import pandas as pd
from uuid import uuid4

sensors = [
    simulate_wifi_sensor(),
    simulate_single_value_sensor(["door opens"]),
    simulate_single_value_sensor(["enter bakery"]),
    simulate_single_value_sensor(["enter store"]),
    simulate_single_value_sensor(
        [
            "checkout A",
            "checkout B",
            "checkout C",
            "checkout D",
            "checkout E",
            "checkout F"
        ]
    ),
    simulate_single_value_sensor(
        [
            "freezer",
            "shelf fruits",
            "shelf vegetables",
            "shelf meats",
            "shelf drinks",
            "shelf candy"
        ]
    ),
]
duration: list[float] = [0.1, 1, 5, 1, 6, 2]


def sensor_generators():
    # Create sensor instances
    temperature_sensor = simulate_temperature_sensor()
    gas_sensor = simulate_gas_sensor()
    biosensor = simulate_biosensor()
    i_w, i_h = 64, 48
    camera_sensor = simulate_camera_sensor(i_w, i_h)
    accelerometer_sensor = simulate_accelerometer_sensor()
    microphone_sensor = simulate_microphone_sensor()
    pressure_sensor = simulate_pressure_sensor()
    infrared_sensor = simulate_infrared_sensor()
    wifi_sensor = simulate_wifi_sensor()

    print(f"Current temperature: {next(temperature_sensor)}°C")
    print(f"Current gas concentration: {next(gas_sensor)} ppm")
    print(f"Current organism activity: {next(biosensor)}")

    img_data = next(camera_sensor)
    print(f"Generated {i_w}x{i_h} image with {len(img_data)} pixels")

    (x, y, z) = next(accelerometer_sensor)
    print(f"Acceleration: ({x}, {y}, {z})")
    print(f"Current sound level: {next(microphone_sensor)}")
    print(f"Current pressure: {next(pressure_sensor)} kPa")
    print(f"Distance to object: {next(infrared_sensor)} meters")
    wifi_log = next(wifi_sensor)
    print(f"mac-address {wifi_log[1]} - signal-strength {wifi_log[2]}")


def test_markov_chains():
    """
    This creates a MarkovChain instance that has 4 states A, B, C and D ,
    with transition matrix given above with probability of staying in same state is 0.9 and 0.8 respectively.
    And it simulates 10 steps starting from state A.

    You can also add other functionality to this class,
    such as methods to compute the steady-state probabilities of the Markov chain,
    or to generate sample sequences of states from the Markov chain.
    """
    transition_matrix = [[0.7, 0.1, 0.1, 0.1],
                         [0.2, 0.6, 0.1, 0.1],
                         [0.2, 0.2, 0.4, 0.2],
                         [0.1, 0.1, 0.1, 0.7]]
    states = ["A", "B", "C", "D"]
    mc = MarkovChain(transition_matrix, states)

    current_state = 0
    num_steps = 100
    simulated_states = mc.simulate(current_state, num_steps)

    # print steady state probabilities
    print("Steady state probabilities: ", mc.steady_state())
    print("Simulated States: ", simulated_states)

    # print edges with weight
    for edge in mc.all_edges():
        print(f"{edge[0]} -> {edge[1]} : {edge[2]}")

    # visualize the Markov Chain
    mc.visualize()


def markov_chain_store_example():
    transition_matrix = [
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],  # Wifi_Sensor
        [0.0, 0.0, 0.2, 0.8, 0.0, 0.0],  # Door_Sensor
        [0.2, 0.0, 0.0, 0.8, 0.0, 0.0],  # Bakery_Sensor
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0],  # Store_Sensor
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Checkout_Sensor
        [0.0, 0.0, 0.0, 0.0, 0.2, 0.8]   # Shelf_Sensor
    ]

    states = ["Wifi_Sensor", "Door_Sensor", "Bakery_Sensor", "Store_Sensor", "Checkout_Sensor", "Shelf_Sensor"]
    mc = MarkovChain(transition_matrix, states)

    current_state = 0
    num_steps = 100
    simulated_states = mc.simulate(current_state, num_steps)

    ###

    i = 0
    sensor_logs: list[dict] = []
    uuid = str(uuid4())[:8]
    date_now = datetime.datetime.now()

    for state in simulated_states:

        if state == states[current_state]:
            i = 0
            uuid = str(uuid4())[:8]

        date_now = date_now + datetime.timedelta(minutes=duration[states.index(state)])

        sensor_log: SensorLog = SensorLog(
            sensor_value=next(sensors[states.index(state)]),
            case_id=f"{uuid}_{i}",
            timestamp=date_now,
            sensor_name=state,
            status="valid"
        )

        sensor_logs.append(sensor_log.__dict__)
        i = i + 1

    df = pd.DataFrame(sensor_logs)
    print(df.to_string())

    mc.visualize()

def markov_chain_market_example():
    transition_matrix = [[0.1, 0.2, 0.2, 0.1, 0.2, 0.2],
                         [0.1, 0.1, 0.3, 0.2, 0.2, 0.1],
                         [0.2, 0.1, 0.1, 0.3, 0.2, 0.1],
                         [0.1, 0.2, 0.2, 0.2, 0.2, 0.1],
                         [0.2, 0.2, 0.2, 0.2, 0.1, 0.1],
                         [0.3, 0.1, 0.1, 0.1, 0.1, 0.3]]

    sensors = ["Meat", "Dairy", "Produce", "Bakery", "Frozen", "HomeGoods"]

    mc = MarkovChain(transition_matrix, sensors)

    # Define the starting sensor and number of steps
    current_sensor = 0
    num_steps = 15

    # Use the simulate method to generate a sequence of sensor triggers
    simulated_sensors = mc.simulate(current_sensor, num_steps)

    # Print the starting sensor and the sequence of simulated sensor triggers
    print("Starting sensor: ", current_sensor)
    print("Simulated sensor triggers: ", simulated_sensors)

    # visualize the Markov Chain
    mc.visualize()
