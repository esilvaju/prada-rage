from typing import Optional, TypeVar, Literal, Generic, TypedDict

TRequestModel = TypeVar("TRequestModel")

class AuthenticatedRequestModel(Generic[TRequestModel]):
    """
    A generic model for authenticated requests.

    @ivar authToken: The authentication token for the request.
    @type authToken: str
    """
    authToken: str

class BaseResponseModel(TypedDict):
    """
    A base model for successful responses.

    @ivar status: The status of the response.
    @type status: Literal["success"]
    """
    status: Literal["success"]

class BaseErrorResponseModel(TypedDict):
    """
    A base model for error responses.

    @ivar status: The status of the response.
    @type status: Literal["error"]
    @ivar errorCode: The error code of the response.
    @type errorCode: Optional[int]
    @ivar errorMessage: The error message of the response.
    @type errorMessage: Optional[str]
    @ivar errorName: The name of the error.
    @type errorName: Optional[str]
    @ivar errorType: The type of the error.
    @type errorType: Optional[Literal["gateway_endpoint_error"] | str]
    """
    status: Literal["error"]
    errorCode: Optional[int]
    errorMessage: Optional[str]
    errorName: Optional[str]
    errorType: Optional[Literal["gateway_endpoint_error"] | str]