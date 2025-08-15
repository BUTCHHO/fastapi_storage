
class Cacher:
    def __init__(self, client, expire_time):
        self.client = client
        self.expire_time = expire_time

    def get_data(self, key):
        raise NotImplementedError

    def put_data(self, key, value):
        raise NotImplementedError

    def delete_data(self, key):
        raise NotImplementedError

class MemCacher(Cacher):
    def __init__(self, memcache_client, data_expire_time):
        super().__init__(memcache_client, data_expire_time)

    def get_data(self, key):
        return self.client.get(key)

    def put_data(self, key, value):
        self.client.add(key, value, self.expire_time)

    def delete_data(self, key):
        self.client.delete(key)

class RedisCacher(Cacher):
    def __init__(self, redis_client, data_expire_time):
        super().__init__(redis_client, data_expire_time)

    def get_data(self, key):
        return self.client.get(key)


    def put_data(self, key, value):
        self.client.set(key, value, ex=self.expire_time, nx=True)

    def delete_data(self, key):
        self.client.delete(key)

    def is_data_exists(self, key):
        return self.client.exists(key)