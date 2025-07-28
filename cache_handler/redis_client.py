from redis import Redis

cache_client = Redis('local', 1111)

def get_cache_client():
    global cache_client
    if cache_client is None:
        raise RuntimeError('cache client is not initialized')
    return cache_client

def init_redis_client(host:str, port:int):
    global cache_client
    if cache_client:
        cache_client.close()
        cache_client.connection_pool.disconnect()
    return Redis(host=host,port=port)