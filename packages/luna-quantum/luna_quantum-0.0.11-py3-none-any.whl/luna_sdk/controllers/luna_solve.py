from luna_sdk.controllers.luna_platform_client import LunaPlatformClient
from luna_sdk.interfaces import ISolutionsRepo
from luna_sdk.interfaces.clients.luna_solve_i import ILunaSolve
from luna_sdk.interfaces.info_repo_i import IInfoRepo
from luna_sdk.interfaces.optimization_repo_i import IOptimizationRepo
from luna_sdk.interfaces.qpu_token_repo_i import IQpuTokenRepo
from luna_sdk.repositories.info_repo import InfoRepo
from luna_sdk.repositories.optimization_repo import OptimizationRepo
from luna_sdk.repositories.qpu_token_repo import QpuTokenRepo
from luna_sdk.repositories.solutions_repo import SolutionsRepo


class LunaSolve(LunaPlatformClient, ILunaSolve):
    optimization: IOptimizationRepo = None  # type: ignore
    solution: ISolutionsRepo = None  # type: ignore
    qpu_token: IQpuTokenRepo = None  # type: ignore
    info: IInfoRepo = None  # type: ignore

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

        self.optimization = OptimizationRepo(self._client)
        self.solution = SolutionsRepo(self._client)
        self.qpu_token = QpuTokenRepo(self._client)
        self.info = InfoRepo(self._client)
