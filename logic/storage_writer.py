import shutil

from aiofiles import open as aio_open
from pathlib import Path


from exceptions.path_exc import EntityDoesNotExists, DirectoryAlreadyExists


class StorageWriter:
    def __init__(self, root_dir_abs_path: str):
        if not isinstance(root_dir_abs_path, str):
            raise TypeError(f'root_dir_abs_path argument must be str, not {type(root_dir_abs_path)}')
        self.root_dir = Path(root_dir_abs_path)

    def delete_all_entities_in_dir(self, path_to_dir=''):
        """deletes all entities in dir excluding this dir"""
        path = Path(path_to_dir)
        for name, path in path.iterdir():
            print(name, 'name')
            print(path, 'path')

    def delete_entity(self, path: str | None):
        entity = Path(self.root_dir, path)
        if entity.exists():
            if entity.is_dir():
                shutil.rmtree(entity)
            elif entity.is_file():
                entity.unlink()
        else:
            raise EntityDoesNotExists(path)


    def create_dir(self, name:str, path: str | None=None, exist_ok=True):
        """
        Creates directory/folder in specified path with specified name
        :param path: Path to the location of the future directory.
        The path must be relative to the root directory, which is passed as an argument to __init__ as root_dir_abs_path.
        This rule is used in every object where root_dir_abs_path is passed during initialization.
        you can set path param as empty string if you need to make dir in root_ dir
        :param name: name of dir
        :return: None
        :raises: FileExistsError
        """
        if path is None:
            path = ''
        if not isinstance(path, str):
            raise TypeError(f'path argument must be str, not {type(path)}')
        if not isinstance(name, str):
            raise TypeError(f'name argument must be str, not {type(path)}')
        root_dir = Path(self.root_dir, path, name)
        try:
            root_dir.mkdir(exist_ok=exist_ok)
        except FileNotFoundError:
            raise EntityDoesNotExists('')
        except FileExistsError:
            raise DirectoryAlreadyExists()
    def create_file(self, path: str | None , name: str, exist_ok):
        """
        Create file in specified path with specified name
        :param path: Path to the location of the future file.
        The path must be relative to the root directory, which is passed as an argument to __init__ as root_dir_abs_path.
        This rule is used in every object where root_dir_abs_path is passed during initialization.
        you can set path param as empty string if you need to make file in root_ dir
        :param name: name of file
        :return: None
        """
        if path is None:
            path = ''
        if not isinstance(path, str):
            raise TypeError(f'path argument must be str, not {type(path)}')
        if not isinstance(name, str):
            raise TypeError(f'name argument must be str, not {type(path)}')
        path_to_future_file = Path(self.root_dir, path, name)
        path_to_future_file.touch(exist_ok=exist_ok)

    async def async_write_from_fastapi_uploadfile_to_file(self, source_file, output_file_path, exist_ok=True):
        """
        special method for fastapi uploading file to hard disk
        :param source_file: fastapi UploadFile object
        :param output_file_path: path where an actual file will be saved on hard disk
        :return: None
        """
        output_file_path = Path(self.root_dir, output_file_path)
        async with aio_open(output_file_path, 'wb') as output_file:
            while content := await source_file.read(1024):
                await output_file.write(content)