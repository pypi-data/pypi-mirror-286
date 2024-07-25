from enum import Enum
from typing import Optional

from pydantic import BaseModel, Extra


class QpuTokenSource(str, Enum):
    # token currently passed in from the API call (not stored by us)
    INLINE = "inline"
    # stored token in user account
    PERSONAL = "personal"
    # stored token in group account
    ORGANIZATION = "organization"


class QpuToken(BaseModel):
    source: QpuTokenSource
    # A unique name for a stored token
    name: Optional[str] = None
    # This could be a QPU token, an API key or any token key for a QPU provider.
    # If the token is not passed from this API call, one stored in the user's
    # account will be used.
    token: Optional[str] = None


class TokenProvider(BaseModel):
    dwave: Optional[QpuToken] = None
    ibm: Optional[QpuToken] = None
    fujitsu: Optional[QpuToken] = None
    qctrl: Optional[QpuToken] = None
    aws_access_key: Optional[QpuToken] = None
    aws_secret_access_key: Optional[QpuToken] = None

    class Config:
        extra = Extra.forbid


class QpuTokenOut(BaseModel):
    """
    Pydantic model for QPU token OUT.
    It contains the data received from the API call.

    Attributes
    ----------
    id: str
        Id of the QPU token
    name: Optional[str]
        Name of the QPU token
    provider: ProviderEnum
        Name of provider: dwave | ibm
    """

    id: str

    name: str
    provider: str

    class Config:
        extra = Extra.ignore
        from_attributes = True
