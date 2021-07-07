from molotov import scenario
from faker import Faker
import os

_API = {
    "sanic": "http://localhost:9001",
    "express-full": "http://localhost:9002",
    "express-quarter": "http://localhost:9002",
    "actix": "http://localhost:9003",
    "spring-boot": "http://localhost:8080",
}[os.environ['SERVER']]

faker = Faker()

@scenario()
async def incrementer(session):
    color = faker.color_name()
    url = f"{_API}/{color}"
    async with session.get(url) as res:
        data = await res.json()
        assert res.status == 200
        assert color in data
