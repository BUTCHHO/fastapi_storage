from app.domain.entities.repository import Repository
from app.domain.exceptions.base import DomainFieldError

from app.domain.value_objects.repository.name.repository_name import RepositoryName
from app.domain.value_objects.repository.repository_id import RepositoryID
from app.domain.value_objects.repository.limit.limit_size import RepositoryLimitSize
from app.domain.enums.repository_statuses import RepositoryStatus

from app.domain.exceptions.repository import RepositoryFilesCountError, RepositoryDirsCountError

from app.domain.ports.repo_id_generator import RepoIDGenerator


class RepositoryService:
    def __init__(self, repo_id_generator):
        self.repo_id_generator: RepoIDGenerator = repo_id_generator

    def create_repository(self, name: RepositoryName,
                          limit_size_bytes: RepositoryLimitSize,
                          repo_status: RepositoryStatus):
        repo_id = RepositoryID(self.repo_id_generator.generate())
        return Repository(id=repo_id,
                          name=name,
                          limit_size=limit_size_bytes,
                          files_count=0,
                          dirs_count=0,
                          current_size=0,
                          status=repo_status
                          )

    def rename_repository(self, repository: Repository, new_name: RepositoryName):
        repository.name = new_name

    def increase_files_count(self,repository: Repository, increase_by: int=1):
        repository.files_count += increase_by

    def increase_dirs_count(self, repository: Repository, increase_by: int=1):
        repository.dirs_count += increase_by

    def decrease_files_count(self, repository: Repository, decrease_by: int=1):
        if repository.files_count - decrease_by < 0:
            raise RepositoryFilesCountError('repository files count cant be less than zero!')
        repository.files_count -= decrease_by

    def decrease_dirs_count(self, repository: Repository, decrease_by: int=1):
        if repository.dirs_count - decrease_by < 0:
            raise RepositoryDirsCountError('repository dirs count cant be less than zero!')
        repository.dirs_count -= decrease_by