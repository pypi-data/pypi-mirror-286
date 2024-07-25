import logging
import os
from time import sleep
from typing import Dict, List, Optional, Union

from pydantic import BaseModel

from luna_sdk.exceptions.encryption_exception import EncryptionNotSetException
from luna_sdk.interfaces.solutions_repo_i import ISolutionsRepo
from luna_sdk.schemas.create.solution import SolutionIn
from luna_sdk.schemas.enums.solution import SenseEnum
from luna_sdk.schemas.enums.status import StatusEnum
from luna_sdk.schemas.enums.timeframe import TimeframeEnum
from luna_sdk.schemas.qpu_token import TokenProvider
from luna_sdk.schemas.rest.qpu_token.token_provider import RestAPITokenProvider
from luna_sdk.schemas.solution import (
    Result,
    Solution,
    UseCaseRepresentation,
    UseCaseResult,
)
from luna_sdk.utils.qpu_tokens import extract_qpu_tokens_from_env


class SolutionsRepo(ISolutionsRepo):
    _endpoint = "/solutions"

    def get(
        self,
        solution_id: str,
    ) -> Solution:
        """
        Retrieve one solution by id.

        Parameters
        ----------
        solution_id: str
            Id of the solution that should be retrieved

        Returns
        -------
        Solution
            Solution instance
        """
        response = self._client.get(
            f"{self._endpoint}/{solution_id}",
        )

        response.raise_for_status()

        return Solution.model_validate_json(response.text)

    def get_all(
        self,
        timeframe: Optional[TimeframeEnum] = None,
        limit: int = 50,
        offset: int = 0,
        optimization_id: Optional[str] = None,
    ) -> List[Solution]:
        """
        Get list of available optimizations.

        Parameters
        ----------
        timeframe: Optional[TimeframeEnum]
            Only return Solutions created within a specified timeframe. Default None.
        limit:
            Limit the number of Optimizations to be returned. Default value 10.
        offset:
            Offset the list of solutions by this amount. Default value 0.
        optimization_id: Optional[str]
            Show solutions for only this optimization id. Default None.

        Returns
        -------
        List[SolutionOut]
            List of SolutionOut instances.
        """
        params = {}
        if timeframe and timeframe != TimeframeEnum.all_time:  # no value == all_time
            params["timeframe"] = timeframe.value

        if limit < 1:
            # set the minimum limit to 1
            limit = 1

        if optimization_id is not None:
            params["optimization_id"] = str(optimization_id)

        params["limit"] = str(limit)
        params["offset"] = str(offset)
        response = self._client.get(
            self._endpoint,
            params=params,
        )

        response.raise_for_status()

        return [Solution.model_validate(i) for i in response.json()]

    def delete(self, solution_id: str) -> None:
        """
        Delete one optimization by id.

        Parameters
        ----------
        solution_id: str
            Id of the optimization that should be deleted

        Returns
        -------
        """
        self._client.delete(
            f"{self._endpoint}/{solution_id}",
        )

    def create(
        self,
        optimization_id: str,
        solver_name: str,
        provider: str,
        qpu_tokens: Optional[TokenProvider] = None,
        solver_parameters: Optional[Union[Dict, BaseModel]] = None,
        encryption_key: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Solution:
        """
        Create a solution for an optimization

        Parameters
        ----------
        optimization_id: str
            The id of the optimization for which solution should be created
        solver_name: str
            The name of the solver to use.
        provider: str
            The name of the QPU provider to use.
        qpu_tokens: Optional[TokenProvider]
            The tokens to be used for the QPU.
        solver_parameters: Optional[Dict]
            Parameters to be passed to the solver.
        encryption_key: Optional[str]
            Encryption key to be used for encryption of QPU tokens.
        name: Optional[str]
            Default: None, The name of the solution to create.

        Returns
        -------
        SolutionOut
            Returns the location where the solution can be found once solving is complete.
        """
        if solver_parameters is None:
            solver_parameters = {}
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
        solution_in = SolutionIn(
            optimization=optimization_id,
            solver_name=solver_name,
            provider=provider,
            parameters=(
                solver_parameters.model_dump()
                if isinstance(solver_parameters, BaseModel)
                else solver_parameters
            ),
            qpu_tokens=rest_qpu_tokens,
            encryption_key=encryption_key,
            name=name,
        )
        response = self._client.post(
            self._endpoint, content=solution_in.model_dump_json()
        )
        response.raise_for_status()

        return Solution.model_validate_json(response.text)

    def create_blocking(
        self,
        optimization_id: str,
        solver_name: str,
        provider: str,
        qpu_tokens: Optional[TokenProvider] = None,
        solver_parameters: Optional[Union[Dict, BaseModel]] = None,
        sleep_time_max: float = 60.0,
        sleep_time_increment: float = 5.0,
        sleep_time_initial: float = 5.0,
        encryption_key: Optional[str] = None,
        name: Optional[str] = None,
    ) -> Solution:
        """
        Create a solution for optimization. This method will block your code until the solution is ready.
        Depending on the problem size, this can take a long time.

        Parameters
        ----------
        optimization_id: str
            The id of the optimization for which solution should be created
        solver_name: str
            The name of the solver to use.
        provider: str
            The name of the provider to use.

        qpu_tokens: Optional[TokenProvider] = None
            The tokens to be used for the QPU.
        solver_parameters: Optional[Dict]
            Parameters to be passed to the solver.

        sleep_time_max: float
            Maximum time to sleep between requests.
        sleep_time_increment: float
            Increment of sleep time between requests. Initial sleep time will be
        sleep_time_initial: float
            Initial sleep time.
        encryption_key: Optional[str]
            Encryption key to be used for encryption of QPU tokens.
        name: Optional[str]
            Default: None, The name of the solution to create.
        Returns
        -------
        SolutionOut
            Returns the location where the solution can be found once solving is complete.
        """
        # First create the solution

        params: Optional[Union[Dict, BaseModel]] = None
        if solver_parameters is not None:
            params = solver_parameters
        if isinstance(solver_parameters, BaseModel):
            params = solver_parameters.dict()

        solution: Solution = self.create(
            optimization_id=optimization_id,
            solver_name=solver_name,
            provider=provider,
            solver_parameters=params,
            qpu_tokens=qpu_tokens,
            encryption_key=encryption_key,
            name=name,
        )
        # times are in sec

        cur_sleep_time: float

        if sleep_time_initial > 0.0:
            cur_sleep_time = sleep_time_initial
        else:
            cur_sleep_time = 5.0
            logging.warning(
                f"Invalid sleep_time_initial: {sleep_time_initial}, setting it to default value {cur_sleep_time}"
            )

        while (
            solution.status == StatusEnum.REQUESTED
            or solution.status == StatusEnum.IN_PROGRESS
        ):
            logging.info(
                f"Waiting for solution {solution.id} to complete, "
                f"current status: {solution.status}"
                f", sleeping for {cur_sleep_time} seconds."
            )
            sleep(cur_sleep_time)
            cur_sleep_time += sleep_time_increment
            if cur_sleep_time > sleep_time_max:
                cur_sleep_time = sleep_time_max

            solution = self.get(solution_id=solution.id)

        return solution

    def get_use_case_representation(self, solution_id: str) -> UseCaseRepresentation:
        """
        Get the use-case-specific representation of a solution.

        Parameters
        ----------
        solution_id: str
            Id of the solution that should be retrieved

        Returns
        -------
        UseCaseRepresentation
            The use-case-specific representation
        """
        response = self._client.get(f"{self._endpoint}/{solution_id}/representation")
        response.raise_for_status()
        return UseCaseRepresentation.model_validate_json(response.text)

    def get_best_result(self, solution: Solution) -> Optional[Result]:
        """
        Retrieves the best result from a solution.

        Parameters
        ----------
        solution : Solution
            The solution received via `solutions.get` or `solutions.get_all`.

        Returns
        -------
        Result | None
            The best result of the solution. If there are several best solutions with
            the same objective value, return only the first. If the solution results are
            not (yet) available or no the solution sense is `None`, return `None`.
        """
        if solution.results is None or solution.sense is None:
            return None

        agg = min if solution.sense == SenseEnum.MIN else max
        best_result = agg(solution.results, key=lambda x: x.obj_value)

        return best_result

    def get_best_use_case_result(
        self, use_case_representation: UseCaseRepresentation
    ) -> Optional[UseCaseResult]:
        """
        Retrieves the best result from a solution's use case representation.

        Parameters
        ----------
        use_case_representation : UseCaseRepresentation
            A solution's use case representation.

        Returns
        -------
        UseCaseResult | None
            The best result of the solution. If there are several best solutions with
            the same objective value, return only the first. If the solution results are
            not (yet) available or no the solution sense is `None`, return `None`.
        """
        if (
            use_case_representation.results is None
            or use_case_representation.sense is None
        ):
            return None

        agg = min if use_case_representation.sense == SenseEnum.MIN else max
        best_result = agg(use_case_representation.results, key=lambda x: x.obj_value)

        return best_result
