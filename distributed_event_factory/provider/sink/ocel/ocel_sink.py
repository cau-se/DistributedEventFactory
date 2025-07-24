from typing import Any, Dict, Collection

import pm4py
from process_mining_core.datastructure.core.event import Event

from distributed_event_factory.provider.sink.sink_provider import Sink, SinkProvider
import pandas as pd
import ast

from provider.object.size_params_provider import SizeParamsProvider


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

    def send(self, event: Event, root, object_sources, object_store) -> None:
        # print(event.timestamp)
        if not self.object_types:
            for object_source in object_sources.values():
                if object_source.object_type not in self.object_types:
                    self.object_types.append(object_source.object_type)
        print("Sensor " + event.node + ": " + str(event))
        self.el.append("Sensor " + event.node + ": " + str(event))
        new_row = {}
        new_row["ocel:eid"] = event.node + str(self.index)
        new_row["ocel:timestamp"] = event.timestamp
        new_row["ocel:activity"] = event.activity
        new_row["ocel:node"] = event.node
        new_row["ocel:workstation"]: event.group
        type_objects: Dict[str, list[ObjectSummary]] = {}
        for type in self.object_types:
            input_objects = self.get_objects_of_type(type, event.input, object_store)
            output_objects = self.get_objects_of_type(type, event.output, object_store)
            involved_objects = []
            for input_object in input_objects:
                if input_object in output_objects:
                    output_objects.remove(input_object)
                    input_object.set_is_output(True)
                input_object.set_is_input(True)
                involved_objects.append(input_object)
            for output_object in output_objects:
                output_object.set_is_output(True)
                involved_objects.append(output_object)
            type_objects[type] = involved_objects
        for type, involved_object in type_objects.items():
            #new_row["ocel:" + type + ":type"] = type
            new_row[type + "-name"] = ", ".join(
                [item.name for item in involved_object if item.name is not None])
            new_row[type + "-size"] = ", ".join(
                [str(item.size) for item in involved_object if item.size is not None])
            new_row[type + "-lastChange"] = ", ".join(
                [item.last_change for item in involved_object if item.last_change is not None])
            new_row[type] = ", ".join(
                [str(item.unique_ids) for item in involved_object if item.unique_ids is not None])
            new_row[type + "-input"] = ", ".join(
                [str(item.is_input) for item in involved_object if item.is_input is not None])
            new_row[type + "-output"] = ", ".join(
                [str(item.is_output) for item in involved_object if item.is_output is not None])
        self.rowsList.append(new_row)
        self.contentRoot = root
        self.index += 1

    def start_timeframe(self):
        pass

    def end_timeframe(self):
        df =pd.DataFrame.from_records(data = self.rowsList)#.to_csv(self.contentRoot + "/ocel.csv", index=False, sep=";")
        type_attributes: Dict[str, list[str]] = {}
        for object_type in self.object_types:
            type_attributes[object_type] = [object_type + "-name", object_type + "-size",
                                            object_type + "-lastChange",object_type + "-oid",
                                            object_type + "-input", object_type + "-output"]
        ocel = pm4py.convert.convert_log_to_ocel(log=df, activity_column="ocel:activity",
                                                 timestamp_column="ocel:timestamp",
                                                 object_types=self.object_types, obj_separator=", ",
                                                 additional_event_attributes=["ocel:node", "ocel:workstation"],
                                                 additional_object_attributes=type_attributes)
        pm4py.algo.discovery.ocel.ocpn.variants.classic.apply(ocel=ocel, parameters=ocel.parameters)

    def get_objects_of_type(self, type, objects, object_store):
        objects_of_type = []
        for obj in objects.split("{\'name\': \'"):
            if type in obj:
                count = obj.split("Count = {")[1].split("}")[0].strip()
                unique_ids_part = ast.literal_eval(obj.split("Unique IDs = {")[1].split("}")[0].strip())
                object_example = object_store.find_object_by_id(unique_ids_part[0])
                if object_example:
                    object_summary = ObjectSummary(object_example.object_id_name.id, object_example.object_type,
                                                   object_example.size,
                                                   object_example.get_last_changed_value(), count, unique_ids_part)
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
