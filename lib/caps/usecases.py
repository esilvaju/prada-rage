from lib.caps.primary_ports import BaseInputPort


# TODO: Implement usecases
class BaseUsecase(BaseInputPort):
    def __init__(self):
        pass

    def execute(self, request_model):
        pass


class AuthenticatedUsecase(BaseUsecase):
    def __init__(self):
        pass
