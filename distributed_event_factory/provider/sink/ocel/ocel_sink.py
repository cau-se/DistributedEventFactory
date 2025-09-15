from datetime import datetime
from typing import Dict

import pm4py

from distributed_event_factory.provider.object.size_params_provider import SizeParamsProvider
from distributed_event_factory.simulation.object_event import ObjectEvent

from distributed_event_factory.provider.sink.sink_provider import Sink, SinkProvider
import pandas as pd
import ast


class OcelConsole(Sink):

    def __init__(self, id, data_source_ref):
        super().__init__(data_source_ref)
        self.id = id
        self.object_types = []
        self.el = []
        self.rowsList = []
        self.contentRoot = None
        self.index = 0
        self.object_types = []
        self.input_counter = 0
        self.output_counter = 0
        self.start_time = None
        self.end_time = None
        self.problem_event_counter = 0

    def send(
        self,
        event: ObjectEvent
    ) -> None:
        if self.start_time is None:
            self.start_time = event.timestamp

        if "Failure:" in event.activity:
            self.problem_event_counter += 1

        print("Sensor " + event.node + ": " + str(event))
        self.el.append("Sensor " + event.node + ": " + str(event))
        new_row = {}
        new_row["ocel:eid"] = event.node + str(self.index)
        new_row["ocel:timestamp"] = event.timestamp
        new_row["ocel:activity"] = event.activity
        new_row["ocel:node"] = event.node
        new_row["ocel:workstation"]= event.group

        #TODO hrei hier bitte mehr Objekt-Typen mit considern
        for input_event in event.input:
            new_row[input_event.get_object_type()] = input_event.get_object_type()
            if input_event.get_object_type() not in self.object_types:
                self.object_types.append(input_event.get_object_type())
        for output_event in event.output:
                new_row[output_event.get_object_type()] = output_event.get_object_type()
                if output_event.get_object_type() not in self.object_types:
                    self.object_types.append(output_event.get_object_type())

        self.rowsList.append(new_row)
        self.index += 1
        self.end_time = event.timestamp

    def start_timeframe(self):
        pass

    def end_timeframe(self):
        df = pd.DataFrame.from_records(
            data=self.rowsList
        )

        # TODO hrei check here whether we need additional payloads..
        ocel = pm4py.convert.convert_log_to_ocel(
            log=df,
            activity_column="ocel:activity",
            timestamp_column="ocel:timestamp",
            object_types=self.object_types,
            #additional_event_attributes=["ocel:node", "ocel:workstation"],
            #additional_object_attributes=type_attributes
        )

        petri_net = pm4py.algo.discovery.ocel.ocpn.variants.classic.apply(ocel=ocel, parameters=ocel.parameters)
        pm4py.visualization.ocel.ocpn.visualizer.apply(ocpn=petri_net).view()
        #pm4py.objects.ocel.exporter.jsonocel.exporter.apply(ocel=ocel, target_path=self.contentRoot + "/ocel.jsonocel")

        start_time_dt = datetime.strptime(self.start_time, "%Y-%m-%d %H:%M:%S")
        end_time_dt = datetime.strptime(self.end_time, "%Y-%m-%d %H:%M:%S")

        petri_nety_per_object_type = petri_net.get("petri_nets")
        simplicity_nodes = []
        simplicity_transition = []
        for object_type in self.object_types:
            petri_type = petri_nety_per_object_type.get(object_type)
            if petri_type is not None:
                simplicity_nodes.append(len(petri_type[0].places))
                simplicity_transition.append(len(petri_type[0].transitions))

        print("Time: " + str(end_time_dt - start_time_dt))
        print("Duration: " + str(datetime.now() - start_time_dt))
        print("Simplicity nodes: " + str(simplicity_nodes))
        print("Simplicity transitions: " + str(simplicity_transition))
        print("Problems Events: " + str(self.problem_event_counter))
        print("Input objects per event: " + str(self.input_counter / self.index))
        print("Output objects per event: " + str(self.output_counter / self.index))

    def get_objects_of_type(self, type, objects, object_store):
        objects_of_type = []
        for obj in objects.split("{\'name\': \'"):
            if type in obj:
                count = obj.split("Count = {")[1].split("}")[0].strip()
                unique_ids_part = ast.literal_eval(obj.split("Unique IDs = {")[1].split("}")[0].strip())
                object_example = object_store.find_object_by_id(unique_ids_part[0])
                if object_example:
                    object_summary = ObjectSummary(
                        object_example.object_id_name.id,
                        object_example.object_type,
                        object_example.size,
                        object_example.get_last_changed_value(),
                        count,
                        unique_ids_part
                    )
                    if object_summary not in objects_of_type:
                        objects_of_type.append(object_summary)
                else:
                    length = None
                    width = None
                    depth = None
                    size = None
                    name = obj.split(",")[0]
                    obj_type = obj.split("\'object_type\': \'")[0].split("\',")[0].strip()
                    if "size" in obj:
                        size = obj.split(",")[2].split("{")[1].split("}")[0]
                        if "length" in size:
                            length = size.split("length\':")[1].strip()
                        if "width" in size:
                            width = size.split("width\':")[1].strip()
                        if "depth" in size:
                            depth = size.split("depth\':")[1].strip()
                        size = SizeParamsProvider(width, length, depth)
                    object_summary = ObjectSummary(name, obj_type, size, None, count, unique_ids_part)
                    if object_summary not in objects_of_type:
                        objects_of_type.append(object_summary)
        return objects_of_type


class PrintOcelConsoleSinkProvider(SinkProvider):
    def get_sender(self, id) -> Sink:
        return OcelConsole(id)


class ObjectSummary:
    def __init__(self, name, type, size, last_change, count, unique_ids):
        self.name = name
        self.type = type
        self.size = size
        self.last_change = last_change
        self.count = count
        self.unique_ids = unique_ids
        self.is_input = False
        self.is_output = False

    def set_is_input(self, is_input: bool):
        self.is_input = is_input

    def set_is_output(self, is_output: bool):
        self.is_output = is_output
