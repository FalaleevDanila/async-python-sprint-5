import secrets
from starlette import status
from typing import Any, Dict

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, Request


from src.db.db import get_session
from src.services.base import user_crud
from src.schemas.user import UserCreate, UserGet


router = APIRouter()


async def verify_token(db: AsyncSession = Depends(get_session), request: Request = None):
    token = request.headers.get('Authorization')
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')

    user = await user_crud.get_token(db=db, token=token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Unauthorized')

    return user


@router.post('/register', response_model=Dict, status_code=status.HTTP_201_CREATED)
async def register(db: AsyncSession = Depends(get_session), obj: UserCreate = None) -> Any:
    response = dict()
    try:
        user = await user_crud.create(db=db, obj_in=obj)
        response['name'] = user.name
        response['password'] = user.password

    except IntegrityError:
        response[obj.name] = 'Данное имя уже занято.'

    return response


@router.post('/auth', response_model=Dict, status_code=status.HTTP_200_OK)
async def authentication(db: AsyncSession = Depends(get_session), obj: UserGet = None) -> Any:

    response = dict()

    user = await user_crud.get(db=db, name=obj.name, password=obj.password)

    if user is None:
        response['name'] = 'Not correct username.'
        return response

    new_token = secrets.token_hex(100)
    await user_crud.update(db=db, name=user.name, token=new_token)
    response['token'] = new_token

    return response
