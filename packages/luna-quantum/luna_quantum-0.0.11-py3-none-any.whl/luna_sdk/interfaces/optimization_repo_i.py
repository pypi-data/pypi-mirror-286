from abc import ABC, abstractmethod
from io import BufferedReader
from typing import List, Optional

from dimod import BinaryQuadraticModel, ConstrainedQuadraticModel

from luna_sdk.interfaces.repository_i import IRepository
from luna_sdk.schemas.enums.optimization import InputType
from luna_sdk.schemas.enums.timeframe import TimeframeEnum
from luna_sdk.schemas.optimization import (
    Optimization,
)
from luna_sdk.schemas.use_cases import UseCase


class IOptimizationRepo(IRepository, ABC):
    @abstractmethod
    def get(
        self,
        optimization_id: str,
    ) -> Optimization:
        """
        Retrieve a optimization by id.

        Parameters
        ----------
        optimization_id: str
            Id of the optimization to be retrieved.

        Returns
        -------
        Optimization:
            Optimization.
        """
        raise NotImplementedError

    @abstractmethod
    def get_all(
        self,
        timeframe: Optional[TimeframeEnum] = None,
        input_type: Optional[InputType] = None,
        limit: int = 50,
        offset: int = 0,
    ) -> List[Optimization]:
        """
        Retrieve a list of optimizations.

        Parameters
        ----------
        timeframe: Optional[TimeframeEnum]
            Only return optimizations created within a specified timeframe.
            Default None.
        input_type: Optional[InputType]
            Only return optimizations of a specified input type. Default None.
        limit:
            Limit the number of optimizations to be returned. Default value 50.
        offset:
            Offset the list of optimizations by this amount. Default value 0.

        Returns
        -------
        List[Optimization]:
            List of optimizations.
        """
        raise NotImplementedError

    @abstractmethod
    def create_from_qubo(
        self,
        name: str,
        matrix: List[List[float]],
        timeout: Optional[float] = 10.0,
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
            Default = 10.0. Timeout for the optimization. If set to None,
            there won't be any timeout. Increase or disable the timeout if you face
            issues uploading big QUBO matrices.

        Returns
        -------
        Optimization:
            Created optimization.
        """
        raise NotImplementedError

    @abstractmethod
    def create_from_use_case(
        self,
        name: str,
        use_case: UseCase,
        timeout: Optional[float] = 10.0,
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
            Default = 10.0. Timeout for the optimization. If set to None,
            there won't be any timeout. Increase or disable the timeout if you face
            issues uploading big Problems.

        Returns
        -------
        Optimization:
            Created optimization.
        """
        raise NotImplementedError

    @abstractmethod
    def create_from_bqm(
        self,
        name: str,
        bqm: BinaryQuadraticModel,
        timeout: Optional[float] = 10.0,
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
            Default = 10.0. Timeout for the optimization. If set to None,
            there won't be any timeout. Increase or disable the timeout if you face
            issues uploading big Problems.

        Returns
        -------
        Optimization:
            Created optimization.
        """
        raise NotImplementedError

    @abstractmethod
    def create_from_cqm(
        self,
        name: str,
        cqm: ConstrainedQuadraticModel,
        timeout: Optional[float] = 10.0,
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
        raise NotImplementedError

    @abstractmethod
    def create_from_lp_file(
        self,
        name: str,
        lp_file: BufferedReader,
        timeout: Optional[float] = 10.0,
    ) -> Optimization:
        """
        Create an optimization from LP file.

        Parameters
        ----------
        name: str
            Name of the optimization to be created.
        lp_file: buffer reader.
        timeout: Optional[float]
            Default = 10.0. Timeout for the optimization. If set to None,
            there won't be any timeout. Increase or disable the timeout if you face
            issues uploading big Problems.

        Returns
        -------
        Optimization:
            Created optimization.
        """
        raise NotImplementedError

    @abstractmethod
    def create_from_lp_string(
        self,
        name: str,
        lp_string: str,
        timeout: Optional[float] = 10.0,
    ) -> Optimization:
        """
        Create an optimization from LP file.

        Parameters
        ----------
        name: str
            Name of the optimization to be created.
        lp_string: string.
        timeout: Optional[float]
            Default = 10.0. Timeout for the optimization. If set to None,
            there won't be any timeout. Increase or disable the timeout if you face
            issues uploading big Problems.

        Returns
        -------
        Optimization:
            Created optimization.
        """
        raise NotImplementedError

    @abstractmethod
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
        raise NotImplementedError

    @abstractmethod
    def delete(
        self,
        optimization_id: str,
    ) -> None:
        """
        Delete an optimization by id.

        Parameters
        ----------
        optimization_id: str
            Id of the optimization to be deleted.
        """
        raise NotImplementedError
