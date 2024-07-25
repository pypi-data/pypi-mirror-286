import os
from typing import Any, Dict, Optional

from luna_sdk.exceptions.encryption_exception import EncryptionNotSetException
from luna_sdk.interfaces.circuit_repo_i import ICircuitRepo
from luna_sdk.schemas.circuit import CircuitJob, CircuitResult
from luna_sdk.schemas.create.circuit import CircuitIn
from luna_sdk.schemas.enums.circuit import CircuitProviderEnum
from luna_sdk.schemas.qpu_token import TokenProvider, QpuToken, QpuTokenSource
from luna_sdk.schemas.rest.qpu_token.token_provider import RestAPITokenProvider
from luna_sdk.utils.qpu_tokens import extract_qpu_tokens_from_env


class CircuitRepo(ICircuitRepo):
    _endpoint = "/circuits"

    def create(
        self,
        circuit: str,
        provider: CircuitProviderEnum,
        params: Dict[str, Any] = {},
        qpu_tokens: Optional[TokenProvider] = None,
        timeout: Optional[float] = 10800.0,
        encryption_key: Optional[str] = None,
    ) -> CircuitJob:
        """
        Create a circuit solution.

        Parameters
        ----------
        circuit: str
            The circuit which to create a solution for.
        provider: CircuitProviderEnum
            Which provider to use to solve the circuit.
        params: Dict[str, Any]
            Additional parameters of the circuit.
        qpu_tokens: Optional[TokenProvider]
            The tokens to be used for the QPU.
        timeout: Optional[float]
            Default = 10800.0. Timeout for the api request. If set to None,
            there won't be any timeout. Increase or disable the timeout if you face
            issues uploading big Problems.
        encryption_key: Optional[str]
            Encryption key to be used for encryption of QPU tokens.
        Returns
        -------
        CircuitJob
            The created circuit job.
        """
        if qpu_tokens is not None:
            rest_qpu_tokens = RestAPITokenProvider.from_sdk_token_provider(qpu_tokens)
        else:
            rest_qpu_tokens = None

        # try to retrieve qpu tokens from env variables
        if rest_qpu_tokens is None:
            rest_qpu_tokens = extract_qpu_tokens_from_env()

        encryption_key = encryption_key or os.environ.get("LUNA_ENCRYPTION_KEY")
        if encryption_key is None:
            raise EncryptionNotSetException
        circuit_in: CircuitIn = CircuitIn(
            provider=provider,
            circuit=circuit,
            params=params,
            qpu_tokens=rest_qpu_tokens,
            encryption_key=encryption_key,
        )

        response = self._client.post(
            self._endpoint, content=circuit_in.model_dump_json(), timeout=timeout
        )

        response.raise_for_status()
        return CircuitJob(id=response.json(), provider=provider, params=params)

    def get(
        self, job: CircuitJob, encryption_key: Optional[str] = None
    ) -> CircuitResult:
        """
        Retrieve a circuit result from a job.

        Parameters
        ----------
        job: CircuitJob
            The job received upon circuit creation.
        encryption_key: Optional[str]
            The encryption key to be used for the QPU.
        Returns
        -------
        CircuitResult
            The result of solving the circuit.
        """
        url = f"{self._endpoint}/{job.id}/{job.provider.value}"
        encryption_key = encryption_key or os.environ.get("LUNA_ENCRYPTION_KEY")
        if encryption_key is None:
            raise EncryptionNotSetException
        if job.params is None:
            job.params = {}
        job.params["encryption_key"] = encryption_key
        response = self._client.get(url, params=job.params, timeout=60)

        response.raise_for_status()
        return CircuitResult.model_validate(response.json())
