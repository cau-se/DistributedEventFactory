from simulation.distributed_event_factory import DistributedEventFactory

if __name__ == '__main__':
    config_file = "config/example_use_case_assembly_line.yml" #os.environ["CONFIG_FILE"]
    DistributedEventFactory(config_file).start()
