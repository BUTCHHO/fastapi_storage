from fastapi import Depends, Query, Request


from app.containers import Container
from dependency_injector.wiring import inject, Provide

from .schemas.response import GetEntitiesResponse, SearchEntitiesResponse
from .schemas.query import BrowserGetEntitiesQuery, BrowserSearchEntitiesQuery

from .router import browser_router


@browser_router.get('/_get_entities', response_model=GetEntitiesResponse)
@inject
async def get_entities_in_storage(
        request: Request,
        params: BrowserGetEntitiesQuery = Query(),
        auth_depend=Depends(Provide[Container.auth_depend]),
        browser_endpoint_handler = Depends(Provide[Container.browser_endpoint_handler])
        ):
    user = await auth_depend.auth(request)
    entities = browser_endpoint_handler.get_list_of_entities(user.storage_id, params.path_in_storage)
    return {"entities": entities,
            "path_in_storage": params.path_in_storage}

@browser_router.get('/_get_entities/search', response_model=SearchEntitiesResponse)
@inject
async def search_entities_by_pattern(
        request: Request,
        auth_depend=Depends(Provide[Container.auth_depend]),
        params: BrowserSearchEntitiesQuery = Query(),
        browser_endpoint_handler=Depends(Provide[Container.browser_endpoint_handler])
        ):
    user = await auth_depend.auth(request)
    entities = await browser_endpoint_handler.search_entities_by_pattern(user.storage_id, params.pattern, params.searching_in_path)
    return {"entities": entities}

