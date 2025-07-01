from fastapi import APIRouter, Depends, Query, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path
from fastapi.responses import HTMLResponse

from app.singletones import storage_reader, logger, path_joiner, path_cutter, path_ensurer
from .handlers.browser_view_handler import BrowserViewHandler
from .schemas.response import GetEntitiesResponse, SearchEntitiesResponse
from .schemas.query import BrowserGetEntitiesQuery, BrowserSearchEntitiesQuery
from .handlers import BrowserEndpointHandler
from app.routes.dependencies import auth_depend

templates_dir = Path(__file__).parent / 'templates'
global_templates_dir = Path(__file__).parent.parent.parent / 'templates'
static_dir = Path(__file__).parent / 'static'
global_static_dir = Path(__file__).parent.parent.parent / 'static'



browser_router = APIRouter()

templates = Jinja2Templates(directory=[templates_dir, global_templates_dir])


browser_endpoint_handler = BrowserEndpointHandler(storage_reader, logger, path_joiner, path_cutter, path_ensurer)
browser_view_handler = BrowserViewHandler(templates)

@browser_router.get('/_get_entities', response_model=GetEntitiesResponse)
def get_entities_in_storage(params: BrowserGetEntitiesQuery = Query(),
                            user=Depends(auth_depend.auth)):
    entities = browser_endpoint_handler.get_list_of_entities(user.id, params.path_in_storage)
    return {"entities": entities}

@browser_router.get('/_get_entities/search', response_model=SearchEntitiesResponse)
def search_entities_by_pattern(user=Depends(auth_depend.auth), params: BrowserSearchEntitiesQuery = Query()):
    entities = browser_endpoint_handler.search_entities_by_pattern(str(user.id), params.pattern, params.searching_in_path)
    return {"entities": entities}

@browser_router.get('/browser', response_class=HTMLResponse)
def view_storage(request: Request, user=Depends(auth_depend.auth_allow_unauthorized)):
    html_template_response = browser_view_handler.get_html_response(request=request, user=user)
    return html_template_response
