import numpy


class NextSensorProvider:

    def __init__(self, probability_distribution):
        self.probability_distribution = probability_distribution

    def get_next_sensor(self):
        return numpy.random.choice(len(self.probability_distribution), p=numpy.array(self.probability_distribution))


class NextSensorChooseProvider:
    def __init__(self, number_of_sensors):
        self.number_of_sensors = number_of_sensors

    def get(self, probability_distribution) -> NextSensorProvider:
        distribution = probability_distribution[0:self.number_of_sensors - 1]
        remaining_probability = 1.0 - sum(distribution)
        distribution.append(remaining_probability)
        return NextSensorProvider(distribution)