from pathlib import Path
from os import walk
from collections import defaultdict
from tabulate import tabulate
from math import *

def load_data():
    data_by_server = defaultdict(lambda: [])
    data_root = Path("data")

    for root, dirs, files in walk(data_root):
        root = Path(root)
        server = root.name
        print(f"Reading {root}")
        for file in files:
            if not file.endswith(".txt"):
                continue
            with open(root / file) as f:
                for line in f.readlines():
                    if not line.strip():
                        continue
                    try:
                        time = float(line.strip())
                    except ValueError as e:
                        continue
                    if 'nosleep' not in server:
                        time -= 10
                    data_by_server[server].append(time)
        if data_by_server[server]:
            yield server, data_by_server[server]

stats = []
for server, data in load_data():
    count = len(data)
    average = sum(data) / count
    data.sort()
    median = data[int(count * 0.50)]
    p95 = data[int(count * 0.95)]
    stdev = sqrt(sum((d - average) ** 2 for d in data) / count)
    stats.append({"server": server, "count": count, "average": average, "median": median, "p95": p95, "stdev": stdev})

print(
    tabulate(
        sorted(stats, key=lambda row: row['p95']),
        headers={
            "server": "\nServer",
            "count": "Request\nCount",
            "average": "Average\nLatency (ms)",
            "stdev": "Standard\nDeviation (ms)",
            "median": "Median (ms)",
            "p95": "95 percentile (ms)",
        },
        tablefmt="presto",
        floatfmt=".2f",
    )
)
