import asyncio

from sanic import Sanic
from sanic.log import logger
from sanic.response import json

from collections import Counter

app = Sanic("SpeedTest")
app.ctx.counters = Counter()

@app.get("/<name:string>")
async def increment(request, name: str):
    await asyncio.sleep(0.05)
    app.ctx.counters[name] += 1
    value = app.ctx.counters[name]
    logger.info(f"incremented {name} to {value}")
    return json({name: value})

if __name__ == "__main__":
    app.run(workers = 4, port=9001)
