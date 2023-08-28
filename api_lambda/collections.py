import os

from pydantic import BaseModel

from whiplash.whiplash import Whiplash

from basics import REGION, STAGE

DEFAULT_N_PLANES = int(os.environ.get("DEFAULT_N_PLANES", 6))
DEFAULT_BIT_START = int(os.environ.get("DEFAULT_BIT_START", 8))
DEFAULT_BIT_SCALE_FACTOR = float(os.environ.get("DEFAULT_BIT_SCALE_FACTOR", 2))

from responseutil import response_to_fastapi_response as response

class CollectionOut(BaseModel):
    name: str
    region: str
    stage: str
    project_name: str
    n_features: int
    n_planes: int
    bit_start: int
    bit_scale_factor: float
    uniform_planes: dict | None = None

class CreateCollection(BaseModel):
    collection_name: str
    n_features: int
    n_planes: int | DEFAULT_N_PLANES = None
    bit_start: int | DEFAULT_BIT_START = None
    bit_scale_factor: float | DEFAULT_BIT_SCALE_FACTOR = None

def get(project_id, collection_id):
    # Get collection
    whiplash = Whiplash(REGION, STAGE, project_name=project_id)
    collection = whiplash.get_collection(collection_id)
    if not collection:
        return response({"message": "Collection not found"}, 404)
    return response(collection.to_dict())


def all(project_id):
    # List collections
    whiplash = Whiplash(REGION, STAGE, project_name=project_id)
    collections = whiplash.get_all_collections()
    return response([collection.to_dict() for collection in collections])


def create(project_id, collection_name, n_features, n_planes, bit_start, bit_scale_factor):
    # Create project from POST body

    if not collection_name:
        return response({"message": "collection_name required"}, 400)
    if not n_features:
        return response({"message": "n_features required"}, 400)

    n_planes = n_planes or DEFAULT_N_PLANES
    bit_start = bit_start or DEFAULT_BIT_START
    bit_scale_factor = bit_scale_factor or DEFAULT_BIT_SCALE_FACTOR

    whiplash = Whiplash(REGION, STAGE, project_name=project_id)
    collection = whiplash.create_collection(
        collection_name,
        n_features=n_features,
        n_planes=int(n_planes),
        bit_start=int(bit_start),
        bit_scale_factor=float(bit_scale_factor),
    )
    return response(collection.to_dict())
