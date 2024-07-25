from abc import ABC, abstractmethod
from functools import partial
from typing import Tuple, List

import dimod
from dimod import ConstrainedQuadraticModel
from dimod.constrained.constrained import CQMToBQMInverter
from docplex.mp.model import Model as DOCplexModel  # type: ignore
from qiskit_optimization import QuadraticProgram

from luna_sdk.interfaces import IRepository  # type: ignore


class ILPRepo(IRepository, ABC):
    @staticmethod
    def inverter(sample, var_indices, inverter_bqm) -> CQMToBQMInverter:
        sample_list = list(sample.values())
        var_sample = {name: sample_list[index] for name, index in var_indices.items()}
        return inverter_bqm(var_sample)

    @abstractmethod
    def to_qubo_qiskit(self, lp_string: str) -> QuadraticProgram:
        """
        Transform LP to QUBO Qiskit

        Parameters
        ----------
        lp_string: str
            LP problem description

        Returns
        -------
        QuadraticProgram
            QUBO Qiskit representation
        """
        raise NotImplementedError

    @abstractmethod
    def to_docplex(self, lp_string: str) -> DOCplexModel:
        """
        Transform LP to DOCplex

        Parameters
        ----------
        lp_string: str
            LP problem description

        Returns
        -------
        DOCplexModel
            DOCplex representation
        """
        raise NotImplementedError

    @abstractmethod
    def to_qubo_matrix(self, lp_string: str) -> Tuple[List[List[float]], partial]:
        """
        Transform LP to QUBO matrix

        Parameters
        ----------
        lp_string: str
            LP problem description

        Returns
        -------
        Tuple[List[List[float]], partial]
            QUBO matrix representation and inverter
        """
        raise NotImplementedError

    @abstractmethod
    def to_bqm(
        self, lp_string: str
    ) -> Tuple[dimod.BinaryQuadraticModel, CQMToBQMInverter]:
        """
        Transform LP to BQM model

        Parameters
        ----------
        lp_string: str
            LP problem description

        Returns
        -------
        Tuple[dimod.BinaryQuadraticModel, CQMToBQMInverter]
            BQM representation and inverter
        """
        raise NotImplementedError

    @abstractmethod
    def to_cqm(self, lp_string: str) -> ConstrainedQuadraticModel:
        """
        Transform LP to CQM model

        Parameters
        ----------
        lp_string: str
            LP problem description

        Returns
        -------
        ConstrainedQuadraticModel
            CQM representation
        """
        raise NotImplementedError
