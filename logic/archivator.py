
from pathlib import Path
from tempfile import mkdtemp
from zipfile import ZipFile, ZIP_DEFLATED
import shutil

class Archivator:

    def create_large_zip(self, archived_dir: str) -> Path:
        archivable_dir = Path(archived_dir)
        temp_dir = Path(mkdtemp())
        self.zip_path = temp_dir / f"{archivable_dir.name}.zip"
        try:
            with ZipFile(
                    self.zip_path,
                    mode='w',
                    compression=ZIP_DEFLATED,
                    allowZip64=True,
                    compresslevel=6
            ) as zipf:
                for file_path in archivable_dir.rglob('*'):
                    if file_path.is_file():
                        arcname = file_path.relative_to(archivable_dir)
                        zipf.write(file_path, arcname)
        except Exception as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise e

        return self.zip_path

    def cleanup_temp_files(self):
        temp_dir = self.zip_path.parent
        try:
            self.zip_path.unlink(missing_ok=True)
            temp_dir.rmdir()
        except OSError:
            shutil.rmtree(temp_dir, ignore_errors=True)