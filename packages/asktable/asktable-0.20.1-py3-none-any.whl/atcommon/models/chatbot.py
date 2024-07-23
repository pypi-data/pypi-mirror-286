from typing import Union
from atcommon.models.base import BaseCoreModel
from datetime import datetime


class BotCore(BaseCoreModel):
    tenant_id: str
    id: str
    name: str
    datasource_ids: str
    extapi_ids: str
    max_rows: int
    debug: int
    sample_questions: list
    magic_input: str
    created_at: Union[str, datetime]
    color_theme: str
    welcome_message: str

    __properties_init__ = [
        "tenant_id",
        "id",
        "name",
        "datasource_ids",
        "extapi_ids",
        "max_rows",
        "debug",
        "sample_questions",
        "magic_input",
        "created_at",
        "color_theme",
        "welcome_message",
    ]

    def __repr__(self):
        return f"[{self.name}]<{self.id}>"
