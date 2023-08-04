class BasePresenter:
    def __init__(self, view):
        self.view = view

    def presentSuccess(self, responseModel: BaseResponseModel):
        raise NotImplementedError("Should have implemented this")
    
    def presentError(self, responseModel: BaseErrorResponseModel):
        raise NotImplementedError("Should have implemented this")