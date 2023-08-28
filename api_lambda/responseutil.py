from fastapi import HTTPException

def response_to_fastapi_response(some_json, status_code=200):
    if status_code >= 400:
        raise HTTPException(status_code, some_json)
    return some_json

def error_response_to_fastapi_response(some_json, status_code=400):
    return response_to_fastapi_response(some_json, status_code)
