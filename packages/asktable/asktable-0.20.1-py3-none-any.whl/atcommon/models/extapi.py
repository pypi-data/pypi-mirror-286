from typing import Union
from atcommon.models.base import BaseCoreModel
from datetime import datetime


class ExtAPICore(BaseCoreModel):
    tenant_id: str
    id: str
    name: str
    base_url: str
    headers: dict
    created_at: Union[str, datetime]

    __properties_init__ = [
        "tenant_id",
        "id",
        "name",
        "base_url",
        "headers",
        "created_at",
        "updated_at",
    ]

    def __repr__(self):
        return f"[{self.name}]<{self.id}>"


class ExtAPIRouteCore(BaseCoreModel):
    tenant_id: str
    extapi_id: str
    id: str
    name: str
    path: str
    method: str
    path_params_desc: str
    query_params_desc: str
    body_params_desc: str
    created_at: Union[str, datetime]

    __properties_init__ = [
        "tenant_id",
        "extapi_id",
        "id",
        "name",
        "path",
        "method",
        "path_params_desc",
        "query_params_desc",
        "body_params_desc",
        "created_at",
        "updated_at",
    ]

    def __repr__(self):
        return f"[{self.name}]<{self.id}>"
