from luna_sdk.controllers.luna_platform_client import LunaPlatformClient
from luna_sdk.interfaces.clients.luna_transform_i import ILunaTransform
from luna_sdk.interfaces.cplex_repo_i import ICplexRepo
from luna_sdk.interfaces.lp_repo_i import ILPRepo
from luna_sdk.repositories.cplex_repo import CplexRepo
from luna_sdk.repositories.lp_repo import LPRepo


class LunaTransform(LunaPlatformClient, ILunaTransform):
    cplex: ICplexRepo = None  # type: ignore
    lp: ILPRepo = None  # type: ignore

    def __init__(
        self,
        email: str,
        password: str,
        timeout: float = 10.0,
    ):
        """
        LunaSolve is the main entrypoint for all LunaSolve related tasks.

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
        super().__init__(
            email=email,
            password=password,
            timeout=timeout,
        )

        self.cplex = CplexRepo(self._client)
        self.lp = LPRepo(self._client)
