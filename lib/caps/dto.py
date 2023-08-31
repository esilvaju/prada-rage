from typing import Optional, Literal, TypeVar, TypedDict


class BaseDTO(TypedDict):
    status: Literal["success", "error"]
    errorCode: Optional[int]
    errorMessage: Optional[str]
    errorName: Optional[str]
    errorType: Optional[Literal["gateway_endpoint_error"] | str]

TBaseDTO = TypeVar("TBaseDTO", bound=BaseDTO)

