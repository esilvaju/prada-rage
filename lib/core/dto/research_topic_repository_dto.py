from typing import Literal, Optional, TypeVar
from lib.caps.dto import BaseDTO


class RegisterSourceDocDTO(BaseDTO):
    def __init__(
        self,
        status: Literal["success", "error"],
        errorCode: int | None = None,
        errorMessage: str | None = None,
        errorName: str | None = None,
        errorType: str | None = None,
    ) -> None:
        super().__init__(status, errorCode, errorMessage, errorName, errorType)


TRegisterSourceDocDTO = TypeVar("TRegisterSourceDocDTO", bound=RegisterSourceDocDTO)


class RegisterSourceDocDTOEncoder:
    pass
