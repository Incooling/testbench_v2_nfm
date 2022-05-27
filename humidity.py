import asyncio
import re
from omega_tx import Barometer


async def read_once():
    async with Barometer("10.58.32.248", '2000') as tx:
        value = str(await tx.get())
        value = re.sub('\D', '', value)
        value = float(value)
        return value / 10
