from pathlib import Path
from os import walk
from collections import defaultdict
from tabulate import tabulate

data_by_server = defaultdict(lambda: [])
data_root = Path("data")

for root, dirs, files in walk(data_root):
    root = Path(root)
    server = root.name
    for file in files:
        if not file.endswith(".txt"):
            continue
        with open(root / file) as f:
            for line in f.readlines():
                if not line.strip():
                    continue
                data_by_server[server].append(float(line.strip()) - 10.0)

print(
    tabulate(
        [
            {
                "server": server,
                "count": float(len(data_by_server[server])),
                "average": sum(data_by_server[server]) / len(data_by_server[server]),
            }
            for server in data_by_server.keys()
        ],
        headers={
            "server": "\nServer",
            "count": "Request\nCount",
            "average": "Average\nLatency (ms)",
        },
        tablefmt="presto",
        floatfmt=["", ",.0f", ".2f"],
    )
)
