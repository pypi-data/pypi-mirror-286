from luna_sdk.controllers.luna_platform_client import LunaPlatformClient
from luna_sdk.interfaces import ICircuitRepo
from luna_sdk.interfaces.clients.luna_q_i import ILunaQ
from luna_sdk.interfaces.qpu_token_repo_i import IQpuTokenRepo
from luna_sdk.repositories import CircuitRepo, QpuTokenRepo


class LunaQ(LunaPlatformClient, ILunaQ):
    qpu_token: IQpuTokenRepo = None  # type: ignore
    circuit: ICircuitRepo = None  # type: ignore

    def __init__(
        self,
        email: str,
        password: str,
        timeout: float = 10.0,
    ):
        """
        LunaQ is the main entrypoint for all LunaQ related tasks.

        Parameters
        ----------
        email: str
            User's email
        password: str
            User's password
        timeout: float
            Timeout for the requests. Default value 10.

        Returns
        -------
        """
        super().__init__(email=email, password=password, timeout=timeout)

        self.circuit = CircuitRepo(self._client)
        self.qpu_token = QpuTokenRepo(self._client)
