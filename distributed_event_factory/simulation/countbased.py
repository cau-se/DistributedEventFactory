from distributed_event_factory.provider.data.case_provider import CaseIdProvider
from distributed_event_factory.provider.data.count_provider import CountProvider
from distributed_event_factory.simulation.abstract_simulation import Simulation
from distributed_event_factory.simulation.process_simulation import ProcessSimulator
from simulation.process_simulation_object_centric import ProcessSimulationObjectCentric
from simulation.simulator_objects.object_storage import ObjectStorage
from simulation.simulator_objects.workprocessstep import WorkProcessStep


class CountBasedSimulation(Simulation):

    def __init__(self, simulation_steps: int, case_id_provider: CaseIdProvider, max_concurrent_cases: CountProvider):
        super().__init__()
        self.case_id_provider = case_id_provider
        self.simulation_steps = simulation_steps
        self.sinks = dict()
        self.max_concurrent_cases = max_concurrent_cases

    def run_simulation(self, datasources, sinks, objects, routes, stocks, workforce_start_positions, hook=lambda: None):
        self.setup_datasource_sink_mapping(sinks)
        # process_simulator = ProcessSimulator(
        #    case_id_provider=self.case_id_provider,
        #    data_sources=datasources,
        #    max_concurrent_cases=self.max_concurrent_cases,
        #    objects=objects,
        #    routes=routes,
        #    stocks=stocks,
        process_simulator = ProcessSimulationObjectCentric(
            object_storage=ObjectStorage(),
            data_sources=datasources,
            objects=objects,
            routes=routes,
            stocks=stocks,
            workforce_start_positions=workforce_start_positions
        )

        for i in range(200):
            event = process_simulator.simulate()
            self.send_event(event)
        hook()
