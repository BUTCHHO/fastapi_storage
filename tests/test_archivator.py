import pytest

from logic.archivator import Archivator
from logic.storage_reader import StorageReader
from logic.storage_writer import StorageWriter
from utils.path_creator import PathJoiner
from utils.path_cutter import PathCutter

from config import Config
Config.reconfigure_values_for_tests()
@pytest.fixture
def archivator():
    return Archivator(Config.ZIPS_PATH)

@pytest.fixture
def storage_reader():
    return StorageReader(Config.ZIPS_PATH, PathJoiner(Config.ZIPS_PATH), PathCutter(Config.ZIPS_PATH))

@pytest.fixture
def storage_actor():
    return StorageWriter(Config.ZIPS_PATH)


def test_create_large_zip(archivator, storage_reader, storage_actor):
    test_dir_name = 'testy'
    expected_zip_name = f'{test_dir_name}.zip'
    storage_actor.create_dir(name=test_dir_name)
    test_file_name = 'test_file.txt'
    full_path_to_file = storage_reader.join_with_root_path(f'{test_dir_name}/{test_file_name}')
    full_path_to_dir = storage_reader.join_with_root_path(test_dir_name)
    with open(full_path_to_file, 'w') as file:
        some_text = 'text text text text'
        content = ''
        for i in range(10):
            content += some_text
        file.write(content)
    zip_path = archivator.create_large_zip(full_path_to_dir)
    assert storage_reader.is_exists(zip_path.__str__()) is True
    assert zip_path.name == expected_zip_name

    assert zip_path.stat().st_size > 22

    #TODO рефактор этого ужаса

    #TODO тесты удаления архива