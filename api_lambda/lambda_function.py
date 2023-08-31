import boto3
import os
import json
import traceback
from mangum import Mangum

from fastapi import FastAPI, APIRouter, Depends, Request, HTTPException, Header, status, Body, Path, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.api_key import APIKeyHeader
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.exceptions import ExceptionMiddleware

from aws_lambda_powertools import Logger

from basics import initialize as api_initialize
from whip_collections import CollectionOut, \
    get as api_get_collection, all as api_list_collections_for_project, \
    create as api_create_collection, CreateCollection
from items import CreateItem, create as api_create_item, \
    CreateSuccess, get as api_get_item, SearchItems, SearchItemsOut, \
    ItemOut, search as api_search_items, BatchCreate, create_batch as api_batch_create_items
from projects import get as api_get_project, all as api_list_projects, \
    ProjectOut, ProjectsOut


logger = Logger(service="whiplash-api")


API_KEY_HEADER = APIKeyHeader(name="x-api-key", auto_error=False)

def get_api_key(api_key_header: str = Security(API_KEY_HEADER)):
    if api_key_header == os.environ.get("API_KEY"):
        return api_key_header
    else:
        raise HTTPException(status_code=401, detail="Unauthorized, invalid or missing API Key")

app = FastAPI(
    title="Whiplash API",
    summary="CloudKommand-deployed standalone API that provides an easy-to-use api interface for self-hosted Whiplash, a serverless vector store.",
    description="""
        The fundamental units in Whiplash are collections and items, where an item is a vector, and a collection is a set of items that are indexed for fast search. Default settings for collections are set during deployment, but all settings can be changed when creating a collection.
    """,
    docs_url="/docs",
    root_path="/live",
    version=os.environ.get("VERSION", "1.0.0"),
    dependencies=[Depends(get_api_key)]
)
app.add_middleware(ExceptionMiddleware, handlers=app.exception_handlers)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


project_router = APIRouter()

@logger.inject_lambda_context(log_event=True)
def lambda_handler(event, context):
    return Mangum(app, api_gateway_base_path="/live")(event, context)

@app.exception_handler(Exception)
async def unhandled_exception_handler(request, err):
    logger.exception(f"Unhandled exception in {request.url.path}: {err}")
    return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})



    
@project_router.get("/", tags=["Projects"])
def get_projects() -> ProjectsOut:
    return api_list_projects()

@project_router.get("/{project_name}", tags=["Projects"])
def get_project(project_name: str) -> ProjectOut:
    return api_get_project(project_name)


@project_router.get("/{project_name}/collections", tags=["Collections"])
def list_collections_for_project(project_name: str) -> list[CollectionOut]:
    return api_list_collections_for_project(project_name)

@project_router.get("/{project_name}/collections/{collection_name}", tags=["Collections"])
def get_collection(project_name: str, collection_name: str) -> CollectionOut:
    return api_get_collection(project_name, collection_name)

@project_router.post("/{project_name}/collections", tags=["Collections"])
def create_collection(project_name: str, item: CreateCollection) -> CollectionOut:
    item = item.dict()
    return api_create_collection(project_name, item["collection_name"], item["n_features"], item["n_planes"], item["bit_start"], item["bit_scale_factor"])

@project_router.post("/{project_name}/collections/{collection_name}/items", tags=["Items"])
def create_item(project_name: str, collection_name: str, item: CreateItem) -> CreateSuccess:
    item=item.dict()
    return api_create_item(project_name, collection_name, item["id"], item["vector"])

@project_router.get("/{project_name}/collections/{collection_name}/items/{item_id}", tags=["Items"])
def get_item(project_name: str, collection_name: str, item_id: str) -> ItemOut:
    return api_get_item(project_name, collection_name, item_id)

@project_router.post("/{project_name}/collections/{collection_name}/search", tags=["Items"])
def search_items(project_name: str, collection_name: str, search: SearchItems) -> list[SearchItemsOut]:
    search = search.dict()
    return api_search_items(project_name, collection_name, search["query"], search["limit"])

@project_router.post("/{project_name}/collections/{collection_name}/batch", tags=["Items"])
def batch_create_items(project_name: str, collection_name: str, batch: BatchCreate) -> CreateSuccess:
    batch = batch.dict()
    return api_batch_create_items(project_name, collection_name, batch["vectors"])

# @app.post("/initialize", tags=["Initialize"])
# def initialize() -> CreateSuccess:
#     return api_initialize()

app.include_router(project_router, prefix="/projects")

