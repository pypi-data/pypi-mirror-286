from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from luna_sdk.interfaces.repository_i import IRepository
from luna_sdk.schemas.circuit import CircuitJob, CircuitResult
from luna_sdk.schemas.enums.circuit import CircuitProviderEnum
from luna_sdk.schemas.qpu_token import TokenProvider


class ICircuitRepo(IRepository, ABC):
    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
    def get(
        self, job: CircuitJob, encryption_key: Optional[str] = None
    ) -> CircuitResult:
        """
        Attributes:
        choices: A list containing a string or `AliasPath`.
        encryption_key: Optional[str]
            Encryption key to be used for encryption of QPU tokens.

        This is equivalent to Python ``sum`` of :meth:`time.time`.
        :time.time: 1.0
        `CircuitResult`
        Some sections are omitted here for simplicity.
        """
        raise NotImplementedError
