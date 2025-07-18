from typing import Any, Dict, Collection

from process_mining_core.datastructure.core.event import Event

from core.object import GenericObjectSource
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
        new_rows = []
        new_row = {}
        new_row["ocel:eid"] = event.node + str(self.index)
        new_row["ocel:timestamp"] = event.timestamp
        new_row["ocel:activity"] = event.activity
        new_row["ocel:node"] = event.node
        new_row["ocel:workstation"]: event.group
        for type in self.object_types:
            involved_objects = self.get_objects_of_type(type, event.input, object_store)
            involved_objects.extend(self.get_objects_of_type(type, event.output, object_store))
            for involved_object in involved_objects:
                new_row["ocel:type"] = type
                new_row["ocel:" + type + ":name"] = involved_object.name
                new_row["ocel:" + type + ":size"] = involved_object.size
                new_row["ocel:" + type + ":lastChange"] = involved_object.last_change
                new_row["ocel:" + type + ":oid"] = involved_object.unique_ids
        new_rows.append(new_row)

        for row in new_rows:
            self.rowsList.append(row)
        self.contentRoot = root
        self.index += 1

    def start_timeframe(self):
        pass

    def end_timeframe(self):
        additional_object_attributes = Dict[str, Collection[str]]
        # ocel = pm4py.convert.convert_log_to_ocel(log=self.el, activity_column="activiy", timestamp_column="timestamp",
        #                                         object_types=self.object_types, obj_separator=", ",
        #                                         additional_event_attributes=["node", "group"],
        #                                         additional_object_attributes=additional_object_attributes)
        # ocel = classic.OCEL(events=self.events, objects=self.objects, relations=self.relations, globals=None,
        #                    parameters=parameters, o2o=self.o2o, e2e=self.e2e, object_changes=self.object_changes)
        # parameters_alg = dict[Any, Any]
        # parameters_alg.EVENT_ACTIVITY = "x"
        # parameters_alg.OBJECT_TYPE = "y"
        # classic.apply(ocel=ocel, parameters=parameters_alg)
        pd.DataFrame(self.rowsList).to_csv(self.contentRoot + "/ocel.csv", index=False)

    def get_objects_of_type(self, type, objects, object_store):
        objects_of_type = []
        for obj in objects.split("{\'name\': \'"):
            if type in obj:
                count = obj.split("Count = {")[1].split("}")[0].strip()
                unique_ids_part = ast.literal_eval(obj.split("Unique IDs = {")[1].split("}")[0].strip())
                object_example = object_store.find_object_by_id(unique_ids_part[0])
                if object_example:
                    object_summary = ObjectSummary(object_example.object_id_name.id, object_example.object_type, object_example.size,
                                      object_example.get_last_changed_value() ,count, unique_ids_part)
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
