from typing import Optional
from lib.caps.dto import BaseDTO


class RegisterSourceDocDTO(BaseDTO):
    def __init__(self, status: bool, errorCode: int | None = None, errorMessage: str | None = None, errorName: str | None = None, errorType: str | None = None) -> None:
        super().__init__(status, errorCode, errorMessage, errorName, errorType)
        
