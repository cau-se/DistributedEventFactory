from simulation.process_simulation_object_centric import ProcessSimulationObjectCentric
from simulation.simulator_objects.object_storage import ObjectStorage
from simulation.simulator_objects.workprocessstep import WorkProcessStep

if __name__ == '__main__':
    simulator: ProcessSimulationObjectCentric = ProcessSimulationObjectCentric(
        object_storage=ObjectStorage(),
        workstation_steps=[
            WorkProcessStep(
                activity="A",
                node="W1",
                group_id="W1",
                input_objects=[],
                output_objects=["O1"],
                duration=60,
            ),
            WorkProcessStep(
                activity="B",
                node="W2",
                group_id="W2",
                input_objects=["O1"],
                output_objects=["O2"],
                duration=20,
            ),
            WorkProcessStep(
                activity="C",
                node="W3",
                group_id="W3",
                input_objects=["O1", "O2"],
                output_objects=[],
                duration=10,
            )
        ]
    )
    for i in range(10):
        print(simulator.simulate())