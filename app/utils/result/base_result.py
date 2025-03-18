from typing import Union


class BaseResult:
    def __init__(self, status: int, message: str, data: Union[dict, list, None] = None):
        self.status = status
        self.message = message
        self.data = data

    def to_dict(self):
        return {
            "status": self.status,
            "message": self.message,
            "data": self.data,
        }
