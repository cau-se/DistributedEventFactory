import random
import datetime

# Physical sensor
def simulate_temperature_sensor():
    while True:
        temperature = random.uniform(-50, 50)
        yield temperature

# Chemical sensor


def simulate_gas_sensor():
    while True:
        gas_concentration = random.uniform(0, 100)
        yield gas_concentration

# Biological sensor


def simulate_biosensor():
    while True:
        organism_activity = random.uniform(0, 1)
        yield organism_activity

# Optical sensor


def simulate_camera_sensor(width, height):
    while True:
        pixels = []
        for i in range(width * height):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            pixels.append((r, g, b))
        yield pixels

# Motion sensor


def simulate_accelerometer_sensor():
    while True:
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        z = random.uniform(-1, 1)
        yield (x, y, z)

# Audio sensor


def simulate_microphone_sensor():
    while True:
        sound_level = random.uniform(0, 1)
        yield sound_level

# Pressure sensor


def simulate_pressure_sensor():
    while True:
        pressure = random.uniform(0, 1000)
        yield pressure

# Proximity sensor


def simulate_infrared_sensor():
    while True:
        distance = random.uniform(0, 10)
        yield distance


# Wifi sensors
def simulate_wifi_sensor():
    while True:
        mac_address = ':'.join(['{:02x}'.format(random.randint(0, 255)) for _ in range(6)])
        signal_strength = random.randint(-100, -30)
        yield mac_address, signal_strength


# List Sensors
def simulate_single_value_sensor(elements: list[str]):
    while True:
        yield random.choice(elements)
