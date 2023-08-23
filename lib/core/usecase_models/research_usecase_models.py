from typing import TypedDict

from lib.caps.models import BaseErrorResponseModel, BaseResponseModel


class ResearchRequest(TypedDict):
    pass


class ResearchResponse(BaseResponseModel):
    pass


class ResearchError(BaseErrorResponseModel):
    pass
