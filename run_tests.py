import asyncio
import signal
import subprocess
from time import sleep
import os
import pytest
from config import Config

Config.reconfigure_values_for_tests()

def run_server():
    env = os.environ.copy()
    env["DATABASE_URL"] = env["TEST_DATABASE_URL"]
    env["STORAGE_PATH"] = env['TEST_STORAGE_PATH']
    env["CACHE_PORT"] = env['TEST_CACHE_PORT'] #make sure you have config for the corresponding cache port
    env['ZIPS_PATH'] = env['TEST_ZIPS_PATH']
    server_process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )

    sleep(3)
    return server_process

async def prepare_tables():
    from alchemy.async_engine import async_engine
    print(async_engine.url,' URL')
    from alchemy.models import Base
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