class Logger:

    @staticmethod
    def log(exception):
        print(f'LOG {exception}')

    @staticmethod
    def decor_log(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                Logger.log(e)
        return wrapper
