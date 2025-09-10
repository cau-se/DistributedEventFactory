import os
import sys

from dotenv import load_dotenv
from distributed_event_factory.event_factory import EventFactory
from distributed_event_factory.provider.data.case_provider import CaseIdProvider
from distributed_event_factory.provider.data.constant_count_provider import ConstantCountProvider
from distributed_event_factory.provider.data.count_provider import CountProvider
from distributed_event_factory.provider.data.increasing_case import IncreasingCaseIdProvider
from distributed_event_factory.simulation.process_simulation import DefProcessSimulator
from distributed_event_factory.simulation.xes_process_simulator import XesProcessSimulator
from drift_conformance_checking_sink import DriftConformanceCheckingSink

if __name__ == '__main__':
    if "local" in sys.argv:
        load_dotenv()
    datasource = os.environ["DATASOURCE"]
    sink = os.environ["SINK"]
    simulation = os.environ["SIMULATION"]
    content_root = os.environ["ROOT"]

    print("Running with config:")
    print(f"datasource directory: {datasource}")
    print(f"Sink: {sink}")
    print(f"Simulation: {simulation}")
    print(f"Content root: {content_root}")

    event_factory = EventFactory()

    (event_factory
     .add_directory(f"{content_root}/config/datasource/{datasource}")
     .add_file(f"{content_root}/config/simulation/{simulation}")
     #.add_file(f"{content_root}/config/sink/{sink}")
     .add_process_simulator(
        DefProcessSimulator(
              case_id_provider=IncreasingCaseIdProvider(),
              data_sources=dict(),
              max_concurrent_cases=ConstantCountProvider(1)
            )
    ).add_sink("Hi", DriftConformanceCheckingSink(
        ["A","B","C","D","E"]
    ))
     .run()


     XesProcessSimulator(
         "../config/Road_Traffic_Fine_Management_Process.xes"
     )
        #DefProcessSimulator(
        #   case_id_provider=IncreasingCaseIdProvider(),
        #   data_sources=dict(),
        #   max_concurrent_cases=ConstantCountProvider(1)
        #)
     )
     #).run()
