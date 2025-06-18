class MemCacher:
    def __init__(self, client, data_expire_time):
        self.client = client
        self.expire_time = data_expire_time

    def get_data(self, key):
        return self.client.get(key)

    def put_data(self, key, value):
        self.client.add(key, value, self.expire_time)

    def delete_data(self, key):
        self.client.delete(key)