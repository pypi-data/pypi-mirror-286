from typing import Optional

from pydantic import BaseModel, Extra

from luna_sdk.schemas import QpuToken, TokenProvider


class AWSQpuTokens(BaseModel):
    aws_access_key: QpuToken
    aws_secret_access_key: QpuToken


class RestAPITokenProvider(BaseModel):
    dwave: Optional[QpuToken] = None
    ibm: Optional[QpuToken] = None
    fujitsu: Optional[QpuToken] = None
    qctrl: Optional[QpuToken] = None
    aws: Optional[AWSQpuTokens] = None

    @classmethod
    def from_sdk_token_provider(
        cls, token_provider: TokenProvider
    ) -> "RestAPITokenProvider":
        aws: Optional[AWSQpuTokens] = None
        if (
            token_provider.aws_access_key is not None
            or token_provider.aws_secret_access_key is not None
        ):
            # Ignoring mypy here to receive validation error, because we always need 2 tokens for aws
            aws = AWSQpuTokens(
                aws_access_key=getattr(token_provider, "aws_access_key", None),  # type: ignore[arg-type]
                aws_secret_access_key=getattr(  # type: ignore[arg-type]
                    token_provider, "aws_secret_access_key", None
                ),
            )
        return cls(
            dwave=token_provider.dwave,
            ibm=token_provider.ibm,
            fujitsu=token_provider.fujitsu,
            qctrl=token_provider.qctrl,
            aws=aws,
        )

    class Config:
        extra = Extra.forbid
