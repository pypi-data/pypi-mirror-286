import json
from io import BufferedReader
from typing import Any, Dict, List, Optional, Type

from dimod import BinaryQuadraticModel, ConstrainedQuadraticModel
from httpx import Response

from luna_sdk.interfaces.optimization_repo_i import IOptimizationRepo
from luna_sdk.schemas import UseCase
from luna_sdk.schemas.create import QUBOIn
from luna_sdk.schemas.create.optimization import OptimizationUseCaseIn
from luna_sdk.schemas.enums.optimization import InputType
from luna_sdk.schemas.enums.timeframe import TimeframeEnum
from luna_sdk.schemas.optimization import (
    Optimization,
    OptimizationBQM,
    OptimizationCQM,
    OptimizationLP,
    OptimizationUseCase,
)
from luna_sdk.schemas.optimization_formats.bqm import BQMSchema
from luna_sdk.schemas.optimization_formats.cqm import CQMSchema


class OptimizationRepo(IOptimizationRepo):
    @property
    def _endpoint(self) -> str:
        return "/optimizations"

    def get_all(
        self,
        timeframe: Optional[TimeframeEnum] = None,
        input_type: Optional[InputType] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Optimization]:
        """
        Get a list of all available Models.

        Parameters
        ----------
        timeframe: Optional[TimeframeEnum]
            Only return QUBOs created within a specified timeframe. Default None.
        input_type: Optional[InputType]
            Only return optimizations of a specified input type. Default None.
        limit: int
            Limit the number of Optimizations to be returned. Default value 50.
        offset: int
            Offset the list of optimizations by this amount. Default value 0.

        Returns
        -------
        List[Model]
            List of Model instances.
        """
        params = {}
        if timeframe and timeframe != TimeframeEnum.all_time:  # no value == all_time
            params["timeframe"] = timeframe.value

        if input_type:
            params["input_type"] = input_type.value

        if limit < 1:
            # set the minimum limit to 1
            limit = 1

        params["limit"] = str(limit)
        params["offset"] = str(offset)
        response: Response = self._client.get(self._endpoint, params=params)
        response.raise_for_status()
        return [Optimization.model_validate(item) for item in response.json()]

    def get(self, optimization_id: str) -> Optimization:
        response: Response = self._client.get(f"{self._endpoint}/{optimization_id}")
        response.raise_for_status()
        response_data = response.json()

        model: Type[Optimization] = Optimization

        optimization_data = response_data.pop("optimization_data", None)
        if optimization_data:
            input_type = response_data["input_type"]

            if input_type in (InputType.bqm_spin, InputType.bqm_binary):
                model = OptimizationBQM
            elif input_type == InputType.cqm:
                model = OptimizationCQM
            elif input_type == InputType.lp:
                model = OptimizationLP
            elif input_type == InputType.qubo:
                if response_data.get("use_case_name"):
                    model = OptimizationUseCase
                else:
                    model = OptimizationBQM
            else:
                model = OptimizationBQM

            response_data.update(optimization_data)

        return model.validate(response_data)

    def create_from_qubo(
        self,
        name: str,
        matrix: List[List[float]],
        timeout: Optional[float] = 10800.0,
    ) -> Optimization:
        """
        Create an optimization from a QUBO matrix.

        Parameters
        ----------
        name: str
            Name of the optimization to be created.
        matrix: List[List[float]]
            QUBO matrix.
        timeout: Optional[float]
            Default = 10800. Timeout for the api request. If set to None,
            there won't be any timeout. Increase or disable the timeout if you face
            issues uploading big QUBO matrices.

        Returns
        -------
        Optimization:
            Created optimization.
        """
        data_in: Dict[str, Any] = QUBOIn(name=name, matrix=matrix).model_dump()

        response: Response = self._client.post(
            f"{self._endpoint}/qubo",
            json=data_in,
            timeout=timeout,
        )

        response.raise_for_status()

        return Optimization.model_validate_json(response.text)

    def create_from_use_case(
        self,
        name: str,
        use_case: UseCase,
        timeout: Optional[float] = 10800.0,
    ) -> Optimization:
        """
        Create an optimization from a use case.

        Parameters
        ----------
        name: str
            Name of the optimization to be created.
        use_case: UseCase
            Use case.
        timeout: Optional[float]
            Default = 10800.0. Timeout for the api request. If set to None,
            there won't be any timeout. Increase or disable the timeout if you face
            issues uploading big Problems.

        Returns
        -------
        Optimization:
            Created optimization.
        """
        optimization_in = OptimizationUseCaseIn(
            name=name, use_case=use_case, params=None
        )

        response: Response = self._client.post(
            f"{self._endpoint}/use_case",
            content=optimization_in.model_dump_json(),
            timeout=timeout,
        )

        response.raise_for_status()

        return Optimization.model_validate_json(response.text)

    def create_from_bqm(
        self,
        name: str,
        bqm: BinaryQuadraticModel,
        timeout: Optional[float] = 10800.0,
    ) -> Optimization:
        """
        Create an optimization from BQM.

        Parameters
        ----------
        name: str
            Name of the optimization to be created.
        bqm: BinaryQuadraticModel
            QUBO in dimod BQM format.
        timeout: Optional[float]

        Returns
        -------
        Optimization:
            Created optimization.
        """
        data_in = {"name": name, **BQMSchema.from_bqm(bqm).model_dump()}

        response: Response = self._client.post(
            f"{self._endpoint}/bqm",
            json=data_in,
            timeout=timeout,
        )

        response.raise_for_status()

        return Optimization.model_validate_json(response.text)

    def create_from_cqm(
        self,
        name: str,
        cqm: ConstrainedQuadraticModel,
        timeout: Optional[float] = 10800.0,
    ) -> Optimization:
        """
        Create an optimization from CQM.

        Parameters
        ----------
        name: str
            Name of the optimization to be created.
        cqm: ConstrainedQuadraticModel
            in dimod CQM format.
        timeout: Optional[float]

        Returns
        -------
        Optimization:
            Created optimization.
        """

        data_in = {"name": name, **CQMSchema.from_cqm(cqm).model_dump()}

        response: Response = self._client.post(
            f"{self._endpoint}/cqm",
            json=data_in,
            timeout=timeout,
        )

        response.raise_for_status()

        return Optimization.model_validate_json(response.text)

    def create_from_lp_file(
        self,
        name: str,
        lp_file: BufferedReader,
        timeout: Optional[float] = 10800.0,
    ) -> Optimization:
        """
        Create an optimization from LP file.

        Parameters
        ----------
        name: str
            Name of the optimization to be created.
        lp_file: buffer reader.
        timeout: Optional[float]
            Default = 10800. Timeout for the api request. If set to None,
            there won't be any timeout. Increase or disable the timeout if you face
            issues uploading big QUBO matrices.

        Returns
        -------
        Optimization:
            Created optimization.
        """

        response: Response = self._client.post(
            f"{self._endpoint}/lp-file",
            data={"optimization_in": json.dumps({"name": name})},
            files={"lp_file": lp_file},
            timeout=timeout,
        )

        response.raise_for_status()

        return Optimization.model_validate_json(response.text)

    def create_from_lp_string(
        self,
        name: str,
        lp_string: str,
        timeout: Optional[float] = 10800.0,
    ) -> Optimization:
        """
        Create an optimization from LP string.

        Parameters
        ----------
        name: str
            Name of the optimization to be created.
        lp_string: string.
        timeout: Optional[float]
            Default = 10800. Timeout for the api request. If set to None,
            there won't be any timeout. Increase or disable the timeout if you face
            issues uploading big QUBO matrices.

        Returns
        -------
        Optimization:
            Created optimization.
        """
        data_in = {"name": name, "lp_string": lp_string}

        response: Response = self._client.post(
            f"{self._endpoint}/lp-string",
            json=data_in,
            timeout=timeout,
        )

        response.raise_for_status()

        return Optimization.model_validate_json(response.text)

    def rename(self, optimization_id: str, name: str) -> Optimization:
        """
        Update the name of the optimization

        Parameters
        ----------
        optimization_id: str
            Id of the optimization to be updated.
        name: str
            New name of the optimization

        Returns
        -------
        Optimization:
            Updated optimization.
        """
        data: Dict[str, str] = {"name": name}

        response: Response = self._client.put(
            f"{self._endpoint}/{optimization_id}",
            content=json.dumps(data),
        )
        response.raise_for_status()

        return Optimization.model_validate_json(response.text)

    def delete(self, optimization_id: str) -> None:
        """
        Delete one QUBO by id.

        Parameters
        ----------
        optimization_id: str
            Id of the Model that should be deleted

        Returns
        -------
        """
        response: Response = self._client.delete(f"{self._endpoint}/{optimization_id}")
        response.raise_for_status()
