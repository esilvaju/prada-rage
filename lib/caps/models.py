from typing import Optional, TypedDict

class BaseResponseModel(TypedDict):
    pass

class BaseErrorResponseModel(TypedDict):
    errorCode: Optional[int]
    errorName: str
    errorType: str
    errorMessage: str

class BaseDTO(TypedDict):
    status: bool
    code: Optional[int]
    message: Optional[str]


class BaseViewModel(TypedDict):
    status: bool
    content: BaseErrorResponseModel | BaseResponseModel

