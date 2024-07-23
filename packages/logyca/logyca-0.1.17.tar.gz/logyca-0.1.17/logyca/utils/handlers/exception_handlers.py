from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from logyca.schemas.output.apIresultdto import APIResultDTO
from logyca.utils.constants.logycastatusenum import LogycaStatusEnum
from logyca.utils.handlers.logger import ConstantsLogger
from logyca.utils.helpers.parse_functions import parse_bool
import json, traceback
import logging

"""
This event handler is tested in fastapi to catch all exceptions and give the result in APIResult

Example:

from fastapi import FastAPI
from fastapi.exceptions import HTTPException, RequestValidationError
from logyca.utils.handlers.exception_handlers import http_exception_handler_async, unhandled_exception_handler_async,validation_exception_handler_async

app = FastAPI()

app.add_exception_handler(RequestValidationError, validation_exception_handler_async)
app.add_exception_handler(HTTPException, http_exception_handler_async)
app.add_exception_handler(Exception, unhandled_exception_handler_async)

"""

logger = logging.getLogger(ConstantsLogger.NAME)

def api_result_builder(
    detail: str, status_code: int, logyca_status: LogycaStatusEnum
) -> APIResultDTO:
    api_result_dto = APIResultDTO()
    api_result_dto.dataError = True
    api_result_dto.apiException.isError = True
    api_result_dto.apiException.status = status_code
    api_result_dto.apiException.logycaStatus = logyca_status
    api_result_dto.apiException.message = detail
    api_result_dto.apiException.detail = detail
    api_result_dto.resultMessage = detail
    return api_result_dto

async def validation_exception_handler_async(_: Request, exc: RequestValidationError):
    errors = []
    for error in exc.errors():
        if "type" in error and error["type"] == "json_invalid":
            errors.append({"field": "body", "msg": error["msg"]})
        elif len(error["loc"]) > 1:
            errors.append({"field": error["loc"][1], "msg": error["msg"]})
        elif len(error["loc"]) > 0:
            errors.append({"field": error["loc"][0], "msg": error["msg"]})
    api_result_dto = api_result_builder(
        detail=f"{errors}",
        status_code=LogycaStatusEnum.Invalid_Argument.mappingHttpStatusCode,
        logyca_status=LogycaStatusEnum.Invalid_Argument,
    )
    return JSONResponse(
        status_code=LogycaStatusEnum.Invalid_Argument.mappingHttpStatusCode,
        content=api_result_dto.model_dump(),
    )

async def http_exception_handler_async(_: Request, exc: HTTPException):
    if isinstance(exc.detail,str):
        api_result_dto = api_result_builder(
            detail=exc.detail,
            status_code=LogycaStatusEnum.Internal.mappingHttpStatusCode,
            logyca_status=LogycaStatusEnum.Internal,
        )
        return JSONResponse(
            status_code=LogycaStatusEnum.Internal.mappingHttpStatusCode,
            content=api_result_dto.model_dump(),
        )
    else:
        findValue = exc.detail["dataError"]
        if parse_bool(findValue) is not None:
            return JSONResponse(
                status_code=exc.status_code,
                content=exc.detail,
            )
        else:
            api_result_dto = api_result_builder(
                detail=exc.detail,
                status_code=exc.status_code,
                logyca_status=LogycaStatusEnum.from_http_status_code(exc.status_code),
            )
            return JSONResponse(
                status_code=exc.status_code,
                content=api_result_dto.model_dump(),
            )

async def unhandled_exception_handler_async(_: Request, exc: Exception):
    exception_info = {
        "error_type": type(exc).__name__,
        "message": str(exc),
        "traceback": traceback.format_exc(),
    }
    json_data: str = json.dumps(exception_info)
    logger.critical(json_data)
    api_result_dto = api_result_builder(
        detail=str(exc),
        status_code=LogycaStatusEnum.Internal.mappingHttpStatusCode,
        logyca_status=LogycaStatusEnum.Unknown,
    )
    return JSONResponse(
        status_code=LogycaStatusEnum.Internal.mappingHttpStatusCode,
        content=api_result_dto.model_dump(),
    )
