import asyncio


async def _handleStream(stream: asyncio.StreamReader, isPrint: bool, encoding: str, resultList: list[str]) -> None:
    while True:
        line = await stream.readline()
        if line:
            msg = line.decode(encoding).replace('\r\n', '\n')
            if msg.endswith('\n'):
                msg = msg[:-1]
            resultList.append(msg)
            if isPrint:
                print(msg)
        else:
            break


async def run(cmd: str, isPrint: bool = False, encoding: str = 'GBK') -> tuple[str, int]:
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    
    assert process.stdout
    assert process.stderr

    resultList: list[str] = []
    taskList = [
        asyncio.create_task(
            _handleStream(process.stdout, isPrint, encoding, resultList)
        ),
        asyncio.create_task(
            _handleStream(process.stderr, isPrint, encoding, resultList)
        ),
    ]

    await process.wait()
    for task in taskList:
        task.cancel()
    return '\n'.join(resultList), process.returncode or 0
