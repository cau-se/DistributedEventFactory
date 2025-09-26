import matplotlib.pyplot as plt

from algorithms.conformance_sink import ConformanceSink
from distributed_event_factory.configurator import DefConfigurator
from distributed_event_factory.event_factory import EventFactory
from distributed_event_factory.provider.sink.sink_provider import Sink
from distributed_event_factory.simulation.xes_process_simulator import XesProcessSimulator
from process_mining_core.datastructure.core.event import Event


class MySink(Sink):
    def send(self, event: Event) -> None:
        print(f"My sink: {event}")

if __name__ == '__main__':
    configurator = DefConfigurator()
    event_factory = EventFactory()
    sink = ConformanceSink(["<any>"])
    (event_factory
    .add_file(configurator.get_simulation_file())
    .add_process_simulator(
        XesProcessSimulator(
            "../config/xes/Road_Traffic_Fine_Management_Process.xes",
            node_key="concept:name",
            group_id_key="concept:name"
        ))
    .add_sink("my", sink))

    event_factory.run()
    sink.end()

    recall = []
    precision = []
    outlier_recall = []
    outlier_precision = []
    ngram_recall = []
    ngram_precision = []
    labels = []

    for i in range(20):
        recall.append(sink.get_recall())
        precision.append(sink.get_precision())
        outlier_recall.append(sink.get_recall_outlier(i*0.01))
        outlier_precision.append(sink.get_precision_outlier(i*0.01))
        labels.append(i)
        ngram_recall.append(sink.get_recall_n_gram(i*0.01))
        ngram_precision.append(sink.get_precision_n_gram(i*0.01))

    plt.figure(figsize=(8, 6))
    #plt.plot(labels, outlier_recall, marker='o', linestyle=':', color='blue')
    plt.plot(labels, outlier_precision, marker='o', linestyle='-', color='blue')
    #plt.plot(labels, ngram_recall, marker='o', linestyle=':', color='red')
    plt.plot(labels, ngram_precision, marker='o', linestyle='-', color='red')
    #plt.plot(labels, recall, marker='o', linestyle=':', color='green')
    #plt.plot(labels, precision, marker='o', linestyle='-', color='green')

    plt.title('Line Chart of Six Values')
    plt.xlabel('Point')
    plt.ylabel('Value')
    plt.grid(True)
    plt.show()