import os

from pydantic import BaseModel
from typing import List

# from whiplash.responses import error_response, response
from whiplash.whiplash import Whiplash

from basics import REGION, STAGE
from whip_collections import CollectionOut
from responseutil import response_to_fastapi_response as response


class ProjectOut(BaseModel):
    project_name: str
    collections: list[CollectionOut]

class ProjectListOut(BaseModel):
    projects: list[ProjectOut] | None = None



def get(project_id):
    # Get project metadata
    whiplash = Whiplash(
        REGION, STAGE, project_name=project_id
    )
    collections = [
        collection.to_dict()
        for collection in whiplash.get_all_collections()
        if collection.config.project_name == project_id
    ]

    if not collections or len(collections) == 0:
        return response(f"Project {project_id} not found", 404)

    return response({
        "project_name": project_id,
        "collections": collections,
    })


def all():
    # List projects
    whiplash = Whiplash(REGION, STAGE)
    collections = whiplash.get_all_collections()
    projects = {}
    for collection in collections:
        project_name = collection.config.project_name
        if project_name not in projects:
            projects[project_name] = {
                "project_name": project_name,
                "collections": [],
            }
        projects[project_name]["collections"].append(collection.to_dict())
    return response({"projects": projects})
