import uvicorn
from fastapi import FastAPI
from http import HTTPStatus
from starlette.requests import Request
from starlette.responses import Response
from fastapi.responses import ORJSONResponse

from src.api.v1 import files, ping, users
from src.core.config import app_settings, BLACK_LIST


app = FastAPI(
    title=app_settings.app_title,   # название приложение берём из настроек
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
)
app.include_router(ping.check_db_router, prefix='/api/v1')
app.include_router(users.router, prefix='/users')
app.include_router(files.router, prefix='/files')


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    if request.client.host in BLACK_LIST:  # type: ignore
        return Response(status_code=HTTPStatus.IM_A_TEAPOT)
    return await call_next(request)


if __name__ == '__main__':
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8080`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        'main:app',
        host=app_settings.HOST,
        port=app_settings.PORT,
    )
