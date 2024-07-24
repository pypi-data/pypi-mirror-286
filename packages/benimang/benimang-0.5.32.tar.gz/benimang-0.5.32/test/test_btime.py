import datetime

import pytest

from beni.btime import networkTime


@pytest.mark.asyncio
async def test_networkTime():
    result = await networkTime()
    assert type(result) is datetime.datetime
