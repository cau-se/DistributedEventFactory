import pm4py

from process_mining_core.datastructure.core.event import Event

log = pm4py.read_xes("../config/Road_Traffic_Fine_Management_Process.xes")
activities = set()
for i in range(len(log)):
    event = Event(
        activity=log["concept:name"][i],
        case_id=log["case:concept:name"][i],
        timestamp=log["time:timestamp"][i],
        group_id=log["concept:name"][i],
        node=log["concept:name"][i],
    )
    #print(event)
    activities.add(log["concept:name"][i])
print("Done")
print(activities)