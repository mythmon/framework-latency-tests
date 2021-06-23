from molotov import scenario
from faker import Faker

_API = "http://localhost:8000"

faker = Faker()

@scenario()
async def incrementer(session):
    color = faker.color_name()
    url = f"{_API}/{color}"
    async with session.get(url) as res:
        data = await res.json()
        assert res.status == 200
        assert color in data
