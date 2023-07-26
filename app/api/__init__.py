# -*- coding: utf-8 -*-
import json
from pathlib import Path
from typing import Any, Literal

import orjson
from fastapi import APIRouter
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel
from starlette.responses import JSONResponse

from app.models.business import BusinessModel

router = APIRouter()
P = Path(__file__).parent / ".." / ".." / "data"


def _load(file: str):
    return json.load(open(P / file))


DATA = {
    "1kb": _load("data_1kb.json"),
    "10kb": _load("data_10kb.json"),
    "100kb": _load("data_100kb.json"),
    "1mb": _load("data_1mb.json"),
}

DATA_OBJ = {
    "1kb": BusinessModel.parse_obj(_load("data_1kb.json")),
    "10kb": BusinessModel.parse_obj(_load("data_10kb.json")),
    "100kb": BusinessModel.parse_obj(_load("data_100kb.json")),
    "1mb": BusinessModel.parse_obj(_load("data_1mb.json")),
}

files = Literal["1kb", "10kb", "100kb", "1mb"]


def orjson_dumps(v, *, default):
    # orjson.dumps returns bytes, to match standard json.dumps we need to decode
    return orjson.dumps(v, default=default, option=orjson.OPT_NON_STR_KEYS).decode()


class PydanticJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        if content is None:
            return b""
        if isinstance(content, bytes):
            return content
        if isinstance(content, BaseModel):
            return content.json(by_alias=True).encode(self.charset)
        return content.encode(self.charset)


@router.get("/1_return__dict__none__none")
def return__dict__none__none(file: files):
    return DATA[file]


@router.get("/2_return__dict__pydantic__none", response_model=BusinessModel)
def return__dict__pydantic__none(file: files):
    return DATA[file]


@router.get("/3_return__pydantic__pydantic__none", response_model=BusinessModel)
def return_pydantic_pydantic_none(file: files):
    return DATA_OBJ[file]

@router.get("/4_return__dict__pydantic__json", response_model=BusinessModel)
def return__dict__none__json(file: files):
    return JSONResponse(DATA[file])

@router.get("/5_return__dict__none__orjson")
def return__dict__none__json(file: files):
    return ORJSONResponse(DATA[file])


@router.get("/6_return__dict__pydantic__orjson", response_model=BusinessModel)
def return__dict__none__orjson(file: files):
    return ORJSONResponse(DATA[file])

@router.get("/7_return__pydantic__pydantic__orjson", response_model=BusinessModel)
def return__pydantic__pydantic__orjson(file: files):
    return ORJSONResponse(DATA_OBJ[file].dict())

@router.get("/8_return__pydantic__pydantic__pydantic_json_response", response_model=BusinessModel)
def return__dict__pydantic__orjson(file: files):
    return PydanticJSONResponse(DATA_OBJ[file])