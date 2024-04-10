from typing import List

from fastapi import APIRouter, Depends
from fastapi_pagination import Page, add_pagination
from fastapi_pagination.async_paginator import paginate

from apps.placeholder.schemas.dummy_filter import DummyFilter
from apps.placeholder.schemas.dummy_request import DummyRequest
from apps.placeholder.schemas.dummy_response import DummyResponse
from apps.placeholder.services.dummy import DummyService
from dependencies.auth import RequestPermission, get_current_user, permission_required
from dependencies.database import get_db
from utils.schemas import MessageResponse

sales_router = APIRouter()


@sales_router.post("/", response_model=DummyResponse)
async def create(item: DummyRequest, db=Depends(get_db), user=Depends(get_current_user)):
    # service layer (return entity instance)
    dummy = await DummyService().create(item)
    # response validation (transform to response schema)
    return await DummyResponse.model_validate(dummy)


@sales_router.put("/{id}", response_model=DummyResponse)
async def update(
    id: int,
    item: DummyRequest,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    dummy = await DummyService().update(id, item)
    return await DummyResponse.model_validate(dummy)


@sales_router.get("/{id}", response_model=DummyResponse)
async def get_by_id(id: int, db=Depends(get_db), user=Depends(get_current_user)):
    dummy = await DummyService().get(id)
    return await DummyResponse.model_validate(dummy)


@sales_router.get(
    "/",
    response_model=Page[DummyResponse],
    dependencies=[Depends(RequestPermission("grupos__consultar_todos"))],
)
async def get_all(
    params: DummyFilter = Depends(),
    db=Depends(get_db),
    current_user=Depends(permission_required),
):
    query = params.get_query()
    dummies = await DummyService().get_all(**query)
    return await paginate(dummies, transformer=DummyResponse.transformer)  # type: ignore


@sales_router.delete("/{id}", response_model=DummyResponse)
async def delete_by_id(
    id: int, db=Depends(get_db), current_user=Depends(get_current_user)
):
    dummy = await DummyService().delete(id)
    return await DummyResponse.model_validate(dummy)


@sales_router.put("/upsert/{id}", response_model=DummyResponse)
async def upsert(
    id: int,
    item: DummyRequest,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    dummy = await DummyService().upsert(defaults=item.dict(), id=id)
    return await DummyResponse.model_validate(dummy)


@sales_router.put("/getorcreate/{id}", response_model=DummyResponse)
async def get_or_create(
    id: int,
    item: DummyRequest,
    db=Depends(get_db),
    user=Depends(get_current_user),
):
    dummy = await DummyService().get_or_create(defaults=item.dict(), id=id)
    return await DummyResponse.model_validate(dummy)


add_pagination(sales_router)
