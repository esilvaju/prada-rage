from lib.caps.models import BaseResponseModel, BaseAPIError


class BasePresenter:
    def __init__(self, view):
        self.view = view

    def presentSuccess(self, responseModel: BaseResponseModel):
        raise NotImplementedError("Should have implemented this")
    
    def presentError(self, responseModel: BaseAPIError):
        raise NotImplementedError("Should have implemented this")