import os
import shutil
from aiofile import async_open
from typing import Any, AnyStr, Dict, List
from starlette.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, File, UploadFile, status


from src.db.db import get_session
from src.services.base import file_crud
from src.api.v1.users import verify_token
from src.core.config import DEFAULT_FILES_FOLDER
from src.schemas.file import FileCreate, FileInDBBase


router = APIRouter()


@router.post('/upload', response_model=Dict, status_code=status.HTTP_201_CREATED)
async def upload(
    db: AsyncSession = Depends(get_session), file: UploadFile = File(...), user: bool = Depends(verify_token)
) -> Any:
    name = file.filename
    _path = os.path.join(DEFAULT_FILES_FOLDER, name)

    if not os.path.isdir(DEFAULT_FILES_FOLDER):
        os.mkdir(DEFAULT_FILES_FOLDER)
    async with async_open(_path, 'wb') as f:
        shutil.copyfileobj(file.file, f)

    obj_in = FileCreate(path=_path, name=name, size=file.size)

    created_file = await file_crud.create(db=db, obj_in=obj_in)

    response = {
        "id": created_file.id,
        "name": created_file.name,
        "created_at": created_file.created_at,
        "path": created_file.path,
        "size": created_file.size,
        "is_downloadable": created_file.is_downloadable
    }
    return response


@router.get('/download', response_model=FileInDBBase | AnyStr, status_code=status.HTTP_200_OK)
async def download(path: str = '', is_archive: bool = False, user: bool = Depends(verify_token)) -> Any:

    path_split = path.split('/')
    filename = path_split[-1]
    head_dir = path_split[0]
    last_dir = path_split[-2]
    path_dir = str()

    for _dir in path_split[:-1]:
        path_dir += _dir

    dir_items = os.listdir(head_dir)

    for item in dir_items:
        if item.endswith('.zip'):
            os.remove(os.path.join(head_dir, item))

    if not os.path.isfile(path):
        return f'The file "{filename}" on the path "{path}" does not exist'

    if is_archive:
        archive = shutil.make_archive(last_dir, 'zip', path_dir)
        response = FileResponse(
            path=archive, media_type='media', filename=last_dir + '.zip'
        )
    else:
        response = FileResponse(path, media_type='media', filename=filename)

    return response


@router.get('/', response_model=List, status_code=status.HTTP_200_OK)
async def info(
    db: AsyncSession = Depends(get_session), skip: int = 0, limit: int = 100, user: bool = Depends(verify_token)
) -> Any:

    response = await file_crud.get_multi(db=db, skip=skip, limit=limit)
    return response

