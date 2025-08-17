from pathlib import Path
from zipfile import ZipFile, ZIP_DEFLATED


class Archivator:
    def __init__(self, dir_for_zips):
        self.zip_dir = Path(dir_for_zips)


    def create_path_to_zip(self, archivable_dir):
        return self.zip_dir / f"{archivable_dir.name}.zip"

    def write_from_dir_to_zip(self, archivable_dir, zip_path):
        with ZipFile(zip_path, mode='w', compression=ZIP_DEFLATED, allowZip64=True, compresslevel=6) as zipf:
            print('here i am')
            for file_path in archivable_dir.rglob('*'):
                print(file_path, 'its file path')
                if file_path.is_file():
                    entity = file_path.relative_to(archivable_dir)
                    zipf.write(file_path, entity)

            print('im done')
    def delete_zip(self, zip_name):
        Path(self.zip_dir, zip_name).unlink(missing_ok=True)

    def create_large_zip(self, archivable_dir_path: str) -> Path:
        archivable_dir = Path(archivable_dir_path)
        zip_path = self.create_path_to_zip(archivable_dir)
        self.write_from_dir_to_zip(archivable_dir, zip_path)
        return zip_path
