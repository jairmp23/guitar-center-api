from fastapi import HTTPException


class EntitieNotFound(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=404, detail=detail)
