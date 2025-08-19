import pytest

from pathlib import Path

from logic.storage_writer import StorageWriter
from logic.storage_reader import StorageReader
from utils.path_creator import PathJoiner
from utils.path_cutter import PathCutter
from config import Config

Config.reconfigure_values_for_tests()

@pytest.fixture
def storage_writer():
    return StorageWriter(Config.DIR_FOR_TESTS)

@pytest.fixture
def path_joiner():
    return PathJoiner(Config.DIR_FOR_TESTS)

@pytest.fixture
def path_cutter():
    return PathCutter(Config.DIR_FOR_TESTS)

@pytest.fixture
def storage_reader(path_joiner, path_cutter):
    return StorageReader(Config.DIR_FOR_TESTS, path_joiner, path_cutter)

class TestStorageWriter:

    @pytest.fixture(scope='class', autouse=True)
    def clear_dir_before_start(self):
        path_to_test_dir = Path(Config.DIR_FOR_TESTS)
        if path_to_test_dir.exists():
            path_to_test_dir.rmdir()
            path_to_test_dir.mkdir()
        else:
            path_to_test_dir.mkdir()
        yield
    def test_create_dir(self, storage_writer, storage_reader):
        name = 'test_dir'
        path = ''
        storage_writer.create_dir(name, path, exist_ok=True)
        is_exists = storage_reader.is_exists(name)
        assert is_exists == True
