import traceback

from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse

from dependencies.context.exception import ExceptionContext
from dependencies.context.request import RequestContext
from utils.logs import log


async def exception_middleware(request: Request, call_next):
    request.state.exceptions = []
    RequestContext.set_request(request)
    ExceptionContext.set_exceptions(request.state.exceptions)
    log_data = {
        "request_from": request.url.path + "/" + request.url.query,
        "request_method": request.method,
        "status_code": 200,
    }
    try:
        response = await call_next(request)
        if ExceptionContext.exceptions:
            for e in ExceptionContext.exceptions:
                print(f"Exception: {e}")
            log_data["detail"] = [str(e) for e in ExceptionContext.exceptions]
            log_data["status_code"] = 422
            response = JSONResponse(
                {"detail": log_data["detail"]},
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
    except Exception as exc:
        log_data["status_code"] = 500
        log_data["traceback"] = traceback.format_exc().replace("\n", "\\n")
        response = JSONResponse(
            {"detail": "Internal Server Error"}, status_code=log_data["status_code"]
        )
        print(traceback.format_exc())
    finally:
        log(log_data)
        ExceptionContext.set_exceptions(None)
        RequestContext.set_request(None)
    return response
