from logic import Archivator
from config import STORAGE_PATH

archiver = Archivator()

def test_create_large_zip():
    path_to_archivable = f"{STORAGE_PATH}/music"
    zip = archiver.create_large_zip(path_to_archivable)
    zip_name = zip.name
    expected_zip_name = 'music.zip'
    assert zip_name == expected_zip_name
    archiver.cleanup_temp_files()

