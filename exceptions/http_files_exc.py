from fastapi import HTTPException


class APITooManyFiles(HTTPException):
    def __init__(self):
        detail = {"message": 'Too many files were uploaded at once. Please try again with fewer files per upload.',
                  "code": 'too_many_files'}
        status_code = 429
        super().__init__(detail, status_code)