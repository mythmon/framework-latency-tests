import molotov
import time

_STARTS = {}
_ENDS = {}

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
    if len(_ENDS) == 0:
        return
    average = sum(_ENDS.values()) / len(_ENDS)
    print(
        f"[W{worker_id}] Average response time "
        f"of {len(_ENDS)} requests: {average:.2f}ms"
    )
