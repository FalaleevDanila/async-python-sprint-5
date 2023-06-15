from _socket import gaierror

import asyncpg
from fastapi import APIRouter, HTTPException

from src.core.config import app_settings

check_db_router = APIRouter()


@check_db_router.get('/ping', description='Check database connection.')
async def ping_db():
    try:
        conn = await asyncpg.connect(dsn=app_settings.database_dsn.replace('+asyncpg', ''))
    except ConnectionRefusedError as e:
        raise HTTPException(status_code=404, detail=f'Database not found. {e}')
    except gaierror:
        raise HTTPException(status_code=404, detail=f'Credentials not correct.')
    else:
        result = await conn.fetchval('SELECT 1')
        await conn.close()
        return {'status_db': result}
