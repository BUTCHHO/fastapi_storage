from pathlib import Path
from tempfile import mkdtemp
from zipfile import ZipFile, ZIP_DEFLATED


class Archivator:
    def __init__(self):
        self._zip_path = None
        self.tmp_dir = Path(mkdtemp())

    def has_zip_path(self):
        return self._zip_path is not None

    def make_zip_in_tmp_dir(self, archivable_dir):
        return self.tmp_dir / f"{archivable_dir.name}.zip"

    def write_from_dir_to_zip(self, dir, zip):
        with ZipFile(zip, mode='w', compression=ZIP_DEFLATED, allowZip64=True, compresslevel=6) as zipf:
            for file_path in dir.rglob('*'):
                if file_path.is_file():
                    entity = file_path.relative_to(dir)
                    zipf.write(file_path, entity)

    def cleanup_temp_files(self):
        if self.has_zip_path():
            self._cleanup()
            self._zip_path = None

    def _cleanup(self):
        self._zip_path.unlink(missing_ok=True)

    def create_large_zip(self, archivable_dir_path: str) -> Path:
        archivable_dir = Path(archivable_dir_path)
        self._zip_path = self.make_zip_in_tmp_dir(archivable_dir)
        self.write_from_dir_to_zip(archivable_dir, self._zip_path)
        return self._zip_path
