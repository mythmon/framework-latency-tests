import molotov
import time
import pathlib
import os

_STARTS = {}
_ENDS = {}

_SERVER = os.environ['SERVER']
_VARIANT = os.environ['VARIANT']

def _now():
    return time.time() * 1000

@molotov.events()
async def record_time(event, **info):
    req = info.get("request")
    if event == "sending_request":
        _STARTS[req] = _now()
    elif event == "response_received":
        _ENDS[req] = _now() - _STARTS[req]

@molotov.teardown_session()
async def display_average(worker_id, session):
    data_dir = pathlib.Path("data") / f"{_SERVER}-{_VARIANT}"
    data_dir.mkdir(parents=True, exist_ok=True)
    with open(data_dir / f"worker_{worker_id}.txt", 'w') as f:
        f.write('\n'.join(str(t) for t in _ENDS.values()))
