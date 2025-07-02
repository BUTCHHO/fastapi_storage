from interfaces import IStorageWriter

class StorageDeleter:
    def __init__(self, storage_writer):
        self.storage_writer: IStorageWriter = storage_writer

    def delete_storage_with_recoverability(self, user_id):
        raise NotImplementedError

    def delete_storage_by_user_id(self, user_id):
        self.storage_writer.delete_entity(user_id)
