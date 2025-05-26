def log(exception):
    print(exception)

def dlog(func):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            log(e)
    return wrapper
