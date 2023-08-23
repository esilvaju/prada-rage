from typing import TypeVar, Literal, Generic


TRequestModel = TypeVar("TRequestModel")
rageAuthToken = TypeVar("rageAuthToken", str)


class TAuthenticatedRequestModel(TRequestModel, rageAuthToken):
    """A type that represents an authenticated request model.
    @typeparam TRequestModel The type of the request model which must include rageAuthToken key.
    @remarks
    The rageAuthToken is made available by the session
    """

    pass


class BaseResponseModel:
    """
    A base type for response models.
    @property status A string that indicates the status of the response model. Must be 'success'.
    """

    def __init__(self, status: Literal["success"]):
        self.status = status


TResponseModel = TypeVar("TResponseModel", bound=BaseResponseModel)


class BaseErrorResponseModel(Exception):
    """
    A base type for error response models.
    @property status A string that indicates the status of the error response model. Must be 'error' or 'critical', the latter indicating that the further requests in a pipeline must be canceled.
    @property message A string that provides additional information about the error.
    @property code A number that indicates the error code. This is usually passed to the Presenter to render an HTTP error.
    """

    def __init__(self, status: Literal["error"] | Literal["critical"], errorMessage: str, errorCode: int):
        self.status = status
        self.errorMessage = errorMessage
        self.errorCode = errorCode


TErrorModel = TypeVar("TErrorModel", bound=BaseErrorResponseModel)
