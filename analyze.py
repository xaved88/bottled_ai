"""
be provided a list of ids
go back through, get them, report on them
"""
import json
import os
import statistics

from prettytable import PrettyTable

from definitions import ROOT_DIR
from rs.helper.seed import get_seed_string

run_seeds = [
    '9FD0ISNSV7HZ',
    '7K0YGMFJZHM0',
    'C2GFXDCD16NK',
    '11490VR6B1W7E',
    'Q9ZYXWTCUMZG',
    'EMDMEUKW3HK9',
    '117K2637X6MQA',
    '6JANY1VUMX34',
    '11252A1T7FIP7',
]

latest_runs_title = "Latest Run"
earlier_runs_title = "Earlier Run"


### BELOW HERE ACTUALL CODE


class RunSummary:
    def __init__(self, data: dict):
        self.seed = get_seed_string(int(data['seed_played']))
        self.floor_reached = data['floor_reached']
        self.campfire_choices = data['campfire_choices']
        self.damage_taken = data['damage_taken']
        self.path = data['path_per_floor']
        self.killed_by = "unknown" if 'killed_by' not in data else data['killed_by']

    def summarize(self):
        hallway_fights = [[], [], []]
        elite_fights = [[], [], []]
        boss_fights = []

        for p in self.damage_taken:
            floor_type = self.path[p['floor'] - 1]
            act = 1 if p['floor'] < 16 else 2 if p['floor'] < 32 else 3
            if floor_type == 'B':
                boss_fights.append(p['damage'])
            elif floor_type == 'E':
                elite_fights[act - 1].append(p['damage'])
            else:
                hallway_fights[act - 1].append(p['damage'])

        # upgrade/rest percentage
        upgrade_percent = "~" if not self.campfire_choices else \
            sum([1 for c in self.campfire_choices if c['key'] == "SMITH"]) / len(self.campfire_choices)

        return {
            'Act 1 Hallway (mean)': "-" if not hallway_fights[0] else statistics.mean(hallway_fights[0]),
            'Act 1 Hallway (sd)': "-" if len(hallway_fights[0]) < 2 else statistics.stdev(hallway_fights[0]),
            'Act 2 Hallway (mean)': "-" if not hallway_fights[1] else statistics.mean(hallway_fights[1]),
            'Act 2 Hallway (sd)': "-" if len(hallway_fights[1]) < 2 else statistics.stdev(hallway_fights[1]),
            'Act 3 Hallway (mean)': "-" if not hallway_fights[2] else statistics.mean(hallway_fights[2]),
            'Act 3 Hallway (sd)': "-" if len(hallway_fights[2]) < 2 else statistics.stdev(hallway_fights[2]),
            'Act 1 Elites (mean)': "-" if not elite_fights[0] else statistics.mean(elite_fights[0]),
            'Act 2 Elites (mean)': "-" if not elite_fights[1] else statistics.mean(elite_fights[1]),
            'Act 3 Elites (mean)': "-" if not elite_fights[2] else statistics.mean(elite_fights[2]),
            'Bosses (mean)': "-" if not boss_fights else statistics.mean(boss_fights),
            "Campfire Upgrade %": upgrade_percent,
            "Killed By": self.killed_by,
            "Final Floor": self.floor_reached
        }


def most_common(lst):
    return max(set(lst), key=lst.count)


if not run_seeds:
    print("You need to include some seeds to check!")
    exit(0)

dir = ROOT_DIR + "/../../runs/ironclad/"
run_files = sorted(os.listdir(dir), reverse=True)

latest = {}
earlier = {}

current_count = 0
needed_count = run_seeds * 2

for run in run_files:
    file = open(dir + run, 'r')
    summary = RunSummary(json.loads(file.read()))
    file.close()
    if summary.seed in run_seeds:
        if summary.seed not in latest:
            latest[summary.seed] = summary
            current_count += 1
        elif summary.seed not in earlier:
            earlier[summary.seed] = summary
            current_count += 1
    if current_count == needed_count:
        break

for seed in run_seeds:
    table = PrettyTable()
    table.title = seed

    a = None if seed not in latest else latest[seed]
    b = None if seed not in earlier else earlier[seed]

    if a:
        table.field_names = ["Field", latest_runs_title, earlier_runs_title, "Difference"]
        ap = a.summarize()
        bp = None if not b else b.summarize()
        for k in ap:
            diff = "-" if isinstance(ap[k], str) or isinstance(bp[k], str) else "{:.2f}".format(ap[k] - bp[k])
            adc = ap[k] if not isinstance(ap[k], float) else "{:.2f}".format(ap[k])
            bdc = "-" if not bp else bp[k] if not isinstance(bp[k], float) else "{:.2f}".format(bp[k])
            table.add_row([k, adc, bdc, diff])

    print(table)


def woot(group):
    agg = {}
    for r in group:
        summary = group[r].summarize()
        for k in summary:
            if k not in agg:
                agg[k] = []
            if summary[k] != "-":
                agg[k].append(summary[k])
    return agg


latest_agg = woot(latest)
earlier_agg = woot(earlier)


def formatish(a):
    return "-" if a == "-" else "{:.2f}".format(a)


table = PrettyTable()
table.title = f"Summary of {len(run_seeds)} runs"
table.field_names = ["Field", latest_runs_title + "s", earlier_runs_title + "s", "Difference"]
for k in latest_agg:
    if k == "Killed By":
        a = most_common(latest_agg[k])
        a += f" {latest_agg[k].count(a)}x"
        b = most_common(earlier_agg[k])
        b += f" {earlier_agg[k].count(b)}x"
        diff = "-"
        table.add_row([k, a, b, diff])
    else:
        a = "-" if not latest_agg[k] else statistics.mean([i for i in latest_agg[k] if not isinstance(i, str)])
        b = "-" if not earlier_agg[k] else statistics.mean([i for i in earlier_agg[k] if not isinstance(i, str)])
        diff = "-" if a == "-" or b == "-" else a - b
        table.add_row([k, formatish(a), formatish(b), formatish(diff)])

print(table)
