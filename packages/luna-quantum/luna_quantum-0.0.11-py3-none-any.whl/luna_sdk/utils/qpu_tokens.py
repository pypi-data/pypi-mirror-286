import os

from luna_sdk.schemas import QpuToken, QpuTokenSource
from luna_sdk.schemas.rest.qpu_token.token_provider import (
    RestAPITokenProvider,
    AWSQpuTokens,
)


def extract_qpu_tokens_from_env() -> RestAPITokenProvider:
    ibm_token = os.environ.get("LUNA_IBM_TOKEN")
    dwave_token = os.environ.get("LUNA_DWAVE_TOKEN")
    qctrl_token = os.environ.get("LUNA_QCTRL_TOKEN")
    fujitsu_token = os.environ.get("LUNA_FUJITSU_TOKEN")
    aws_access_key = os.environ.get("LUNA_AWS_ACCESS_KEY")
    aws_access_secret_key = os.environ.get("LUNA_AWS_SECRET_ACCESS_KEY")
    return RestAPITokenProvider(
        ibm=QpuToken(
            source=QpuTokenSource.INLINE,
            token=ibm_token,
        )
        if ibm_token
        else None,
        dwave=QpuToken(
            source=QpuTokenSource.INLINE,
            token=dwave_token,
        )
        if dwave_token
        else None,
        qctrl=QpuToken(
            source=QpuTokenSource.INLINE,
            token=qctrl_token,
        )
        if qctrl_token
        else None,
        fujitsu=QpuToken(
            source=QpuTokenSource.INLINE,
            token=fujitsu_token,
        )
        if fujitsu_token
        else None,
        aws=AWSQpuTokens(
            aws_access_key=QpuToken(
                source=QpuTokenSource.INLINE,
                token=aws_access_key,
            ),
            aws_secret_access_key=QpuToken(
                source=QpuTokenSource.INLINE,
                token=aws_access_secret_key,
            ),
        ),
    )
