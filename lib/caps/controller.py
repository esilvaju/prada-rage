# from typing import Dict, Any, Optional
from fastapi import APIRouter, Request, Response
from fastapi.responses import JSONResponse
from .usecases import BaseUseCase, AuthenticatedUseCase

# from .usecase_models import AuthenticatedRequestModel

# TODO: check: This is not being used anywhere?
# router = APIRouter()


class BaseController:
    def __init__(self, use_case: BaseUseCase):
        self.use_case = use_case

    def execute(self, request: Request, response: Response) -> JSONResponse:
        request_model = request.json()
        result = self.use_case.execute(request_model)


# TODO: fix this later
# class AuthenticatedController(BaseController):
# def __init__(self, use_case: AuthenticatedUseCase):
# super().__init__(use_case)

# async def execute(self, request: Request, response: Response, session) -> JSONResponse:
# request_model = AuthenticatedRequestModel(
# rucio_auth_token=session.get("rucio_auth_token"),
# **await request.json()
# )
# result = await self.use_case.execute(request_model)
# return JSONResponse(content=result)
