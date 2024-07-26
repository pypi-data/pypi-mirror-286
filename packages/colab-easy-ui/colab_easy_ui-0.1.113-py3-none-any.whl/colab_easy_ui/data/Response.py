from pydantic import BaseModel
from typing import TypeAlias, Literal, Dict, Optional


RESPONSE_STATUS: TypeAlias = Literal[
    "OK",
    "NG",
]


class ColabEasyUIResponse(BaseModel):
    status: RESPONSE_STATUS
    message: str


class EasyFileUploaderResponse(ColabEasyUIResponse):
    allowed_filenames: Optional[Dict[str, str]] = None
