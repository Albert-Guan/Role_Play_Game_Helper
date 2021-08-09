import matplotlib.pyplot as plt
from random import random
from datetime import datetime


def uniq_rand_color_gen(num_of_color):
    color_set = set()
    for i in range(0, num_of_color):
        color_gen = (random(), random(), random())
        while color_gen in color_set:
            color_gen = (random(), random(), random())
        color_set.add(color_gen)
    return list(color_set)


def convert_str_to_datetime(time_str, current_date):
    if ' ' not in time_str:
        time_str = current_date + " " + time_str

    return datetime.strptime(time_str+":00", "%Y-%m-%d %H:%M:%S")


current_date = '2020-09-01'
events = [
    ('P1', '12:45', '13:45', 'L1'),
    ('P2', '11:30', '12:30', 'L2'),
    ('P3', '23:00', '2020-09-02 00:50', 'L3')
]

# convert time string representation with datetime
events_with_datetime = [
    (event[0],
     convert_str_to_datetime(event[1], current_date),
     convert_str_to_datetime(event[2], current_date),
     event[3])
    for event in events
]

# calculate get all people and all locations
total_people = list(dict.fromkeys(event[0] for event in events_with_datetime))
total_loc = list(dict.fromkeys(event[3] for event in events_with_datetime))

# 10 pixels per people
graph_height = len(total_people) * 10

# generate random color for different location
colors = uniq_rand_color_gen(len(total_loc))
loc_color_map = {loc: color for loc, color in zip(total_loc, colors)}

# get largest datetime and smallest datetime
max_time = max([event[2] for event in events_with_datetime])
min_time = min([event[1] for event in events_with_datetime])

#
#
fig, gnt = plt.subplots()
fig.suptitle("Timelines for all locations")
gnt.set_ylim(0, graph_height)
gnt.set_xlim([min_time, max_time])

gnt.set_xlabel('Timeline')
gnt.set_ylabel('People')

gnt.set_yticks([10 * (i + 1) for i in range(0, len(total_people))])
gnt.set_yticklabels(total_people)

gnt.grid(True)

# draw general timeline for all events
for i in range(len(total_people)):
    people = total_people[i]
    for event in events_with_datetime:
        if people == event[0]:
            gnt.broken_barh([(event[1], event[2] - event[1])], (i * 10, 10), color=loc_color_map[event[3]])
            gnt.text(x=event[1] + (event[2] - event[1]) / 2, y=i * 10 + 5, s=event[3],
                     ha='center', va='center', color='white')

# draw timeline chart for each locations
for loc in total_loc:
    fig, gnt = plt.subplots()
    fig.suptitle("Timeline for loc="+loc)
    gnt.set_ylim(0, graph_height)
    gnt.set_xlim([min_time, max_time])

    gnt.set_xlabel('Timeline')
    gnt.set_ylabel('People')

    gnt.set_yticks([10 * (i + 1) for i in range(0, len(total_people))])
    gnt.set_yticklabels(total_people)

    gnt.grid(True)
    for i in range(len(total_people)):
        people = total_people[i]
        for event in events_with_datetime:
            if people == event[0] and loc == event[3]:
                gnt.broken_barh([(event[1], event[2] - event[1])], (i * 10, 10), color=loc_color_map[event[3]])
                gnt.text(x=event[1] + (event[2] - event[1]) / 2, y=i * 10 + 5, s=event[3],
                         ha='center', va='center', color='white')

plt.show()
