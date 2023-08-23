from abc import ABC, abstractmethod

# from stream import PassThrough, Transform

from .dto import BaseDTO
from .usecase_models import TRequestModel, TAuthenticatedRequestModel, TResponseModel, TErrorModel

# from .postprocessing_pipeline_elements import BaseStreamingPostProcessingPipelineElement
from .web import TWebResponse
from .view_models import BaseViewModel


class BaseInputPort(ABC):
    """
    A base interface for input ports.
    @typeparam TRequestModel The type of the request model for the input port.
    """

    @abstractmethod
    def execute(self, request_model: TRequestModel) -> None:
        raise NotImplementedError


class BaseAuthenticatedInputPort(BaseInputPort):
    """
    A base interface for authenticated input ports.
    @typeparam AuthenticatedRequestModel The type of the authenticated request model for the input port.
    """

    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def execute(self, auth_request_model: TAuthenticatedRequestModel) -> None:
        raise NotImplementedError


class BaseOutputPort(ABC):
    """
    A base interface for output ports.
    @typeparam TResponseModel The type of the response model for the output port.
    @typeparam TErrorModel The type of the error model for the output port.
    """

    def __init__(self, response: TWebResponse) -> None:
        super().__init__()
        self.response = response

    @abstractmethod
    def presentSuccess(self, response_model: TResponseModel) -> None:
        pass

    @abstractmethod
    def presentError(self, error_model: TErrorModel) -> None:
        pass
