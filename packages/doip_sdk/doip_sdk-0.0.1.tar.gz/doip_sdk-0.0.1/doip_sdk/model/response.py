from typing import Any

from pydantic import BaseModel

from doip_sdk.constant import ResponseStatus


class DOIPResponse(BaseModel):
    requestId: str | None = None
    status: ResponseStatus
    attributes: list = None
    output: Any | None = None
