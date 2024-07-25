from typing import Optional

from pydantic import BaseModel


class SolverInfo(BaseModel):
    full_name: str
    short_name: str
    available: bool
    params: dict
    description: Optional[str]
