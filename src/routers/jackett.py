import json
from json.decoder import JSONDecodeError

from fastapi import APIRouter, Request, Response
from requests import exceptions

from src.modules.jackett_api.jackett import JackettApi

jackett = JackettApi()

router = APIRouter(
    prefix="/api/v1/jackett",
    tags=["Jackett API"]
)


@router.post("/{full_path:path}")
async def post(
        request: Request,
        full_path: str
):
    try:
        body = await request.json()
    except JSONDecodeError:
        body = None

    params = dict(request.query_params)
    if params == {}:
        params = None

    j = jackett.post(
        endpoint=f"/{full_path}",
        params=params,
        json=body
    )

    try:
        content = j.json()
    except exceptions.JSONDecodeError:
        content = None

    headers = dict(request.headers)

    try:
        headers['Content-Type'] = j.headers["Content-Type"]
    except KeyError:
        pass

    try:
        headers['Location'] = j.headers["Location"]
    except KeyError:
        pass

    return Response(
        content=content, headers=headers,
        status_code=j.status_code
    )


@router.get("/{full_path:path}")
async def get(
        request: Request,
        full_path: str
):
    j = jackett.get(
        endpoint=f"/{full_path}",
        params=request.url.query
    )
    try:
        content = json.dumps(j.json())
    except exceptions.JSONDecodeError:
        content = None

    headers = dict(request.headers)

    try:
        headers['Content-Type'] = j.headers["Content-Type"]
    except KeyError:
        pass

    try:
        headers['Location'] = j.headers["Location"]
    except KeyError:
        pass

    return Response(
        content=content, headers=headers,
        status_code=j.status_code
    )
