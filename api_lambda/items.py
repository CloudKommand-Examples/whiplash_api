import os
from typing import Optional
from venv import logger

import numpy as np
from pydantic import BaseModel

from whiplash.collection import Collection
# from whiplash.responses import error_response, parse_body, response
from whiplash.vector import Vector
from whiplash.whiplash import Whiplash

from basics import REGION, STAGE
from responseutil import response_to_fastapi_response as response, \
    error_response_to_fastapi_response as error_response


class CreateItem(BaseModel):
    id: str
    vector: list[float]

class CreateSuccess(BaseModel):
    message: str = "success"

class SearchItems(BaseModel):
    query: list[float]
    limit: int = 5

class SearchItemsOut(BaseModel):
    id: str
    vector: list[float]
    dist: float

class ItemOut(BaseModel):
    id: str
    vector: list[float]

class BatchCreate(BaseModel):
    vectors: list[CreateItem]


def _get_collection(project_id, collection_id) -> Optional[Collection]:
    whiplash = Whiplash(REGION, STAGE, project_name=project_id)
    return whiplash.get_collection(collection_id)


def get(project_id, collection_id, item_id):
    # Get item
    collection = _get_collection(project_id, collection_id)
    if not collection:
        return error_response("Collection not found", 404)

    try:
        item = collection.get_item(item_id)
    except Exception as e:
        logger.info(f"Error getting item: {e}")
        item = None

    if not item:
        return error_response("Item not found", 404)

    return response(item.to_dict())


def search(project_id, collection_id, query, limit=5):
    # Search collection
    collection = _get_collection(project_id, collection_id)

    if not collection:
        return error_response("Collection not found", 404)

    # The rest of the validation is done by FastAPI
    if len(query) != collection.config.n_features:
        return error_response(
            f"query must be a {collection.config.n_features} length list of floats"
        )

    query = np.array(query, dtype=np.float32)

    # Unnecessary with FastAPI
    # limit = int(limit)

    results = collection.search(query, k=limit)
    return response([result.to_dict() for result in results])


def create(project_id, collection_id, vector_id, vector):
    # Create item from POST body
    collection = _get_collection(project_id, collection_id)

    if not collection:
        return error_response("Collection not found", 404)

    if len(vector) != collection.config.n_features:
        return error_response(f"query must be a {collection.config.n_features} length list of floats for collection {collection_id}")
    
    vector = Vector(vector_id, np.array(vector, dtype=np.float32))
    collection.insert(vector)
    return response({"message": "success"})


def create_batch(project_id, collection_id, vectors):
    # Create items from POST body
    collection = _get_collection(project_id, collection_id)

    if not collection:
        return error_response("Collection not found", 404)

    for vector in vectors:
        vector_id = vector.get("id", None)
        if not vector_id:
            return error_response("'id' required")
        vec = vector.get("vector", None)
        if not vec or len(vec) != collection.config.n_features:
            return error_response(
                "'vector' required and must match 'n_features' in size"
            )

        collection.insert(Vector(vector_id, np.array(vec, dtype=np.float32)))

    return response({"message": "success"})
