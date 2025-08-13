import asyncio
import signal
import subprocess
from alchemy.async_engine import async_engine
from alchemy.models import Base
from time import sleep
import os
import pytest

def run_server():
    server_process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    sleep(3)
    return server_process

async def prepare_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

def prepare_for_tests():
    asyncio.run(prepare_tables())

def run_tests():
    pytest.main(['-v','-s', 'tests/test_api.py'])

def run():
    print('preparing')
    prepare_for_tests()
    print('prepare finish')
    print('starting server, please wait...')
    server_process = run_server()
    print('server is ready')
    print('running_tests')
    run_tests()
    print('tests finish!')
    print('killing server...')
    os.kill(server_process.pid, signal.SIGKILL)
    print('finish!')

run()