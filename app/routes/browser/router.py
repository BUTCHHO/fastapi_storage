from fastapi import APIRouter, Depends, Query, Request
from fastapi.templating import Jinja2Templates
from pathlib import Path

from app.singletones import storage_reader, logger, path_joiner, path_cutter, path_ensurer
from .handlers.browser_view_handler import BrowserViewHandler
from .schemas.response import ViewStorageResponse
from .schemas.query import ViewStorageQuery
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

@browser_router.get('/storage', response_model=ViewStorageResponse)
def get_entities_in_storage(params: ViewStorageQuery = Query(),
                         user=Depends(auth_depend.auth)):
    entities = browser_endpoint_handler.get_list_of_entities(user.id, params.path_in_storage)
    return {"entities": entities}

@browser_router.get('/browser')
def view_storage(request: Request, user=Depends(auth_depend.auth)):
    # html_template_response = browser_view_handler.get_html_response(request=request, user=user)
    return {"message": 'not implemented'}
