from logging import Logger as SiteLogger

class Logger:

    def __init__(self):
        self.red_log = "\033[1;31mLOG\033[0m"
        self.logger = SiteLogger

    def log(self, exception):
        print(f'{self.red_log}{exception}{self.red_log}')

    def decor_log(self, func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                Logger.log(e)
        return wrapper
