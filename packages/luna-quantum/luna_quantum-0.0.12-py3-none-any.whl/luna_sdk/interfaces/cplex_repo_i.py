from abc import ABC, abstractmethod
from functools import partial
from typing import Tuple, List

import dimod
from dimod import ConstrainedQuadraticModel
from docplex.mp.model import Model as DOCplexModel  # type: ignore
from qiskit_optimization import QuadraticProgram

from luna_sdk.interfaces import IRepository  # type: ignore
from dimod.constrained.constrained import CQMToBQMInverter


class ICplexRepo(IRepository, ABC):
    @staticmethod
    def inverter(sample, var_indices, inverter_bqm) -> CQMToBQMInverter:
        sample_list = list(sample.values())
        var_sample = {name: sample_list[index] for name, index in var_indices.items()}
        return inverter_bqm(var_sample)

    @abstractmethod
    def to_qubo_qiskit(self, docplex_model: DOCplexModel) -> QuadraticProgram:
        """
        Transform DOCplex model to QUBO Qiskit

        Parameters
        ----------
        docplex_model: docplex.mp.model.Model
            DOCplex problem description

        Returns
        -------
        QuadraticProgram
            QUBO Qiskit representation
        """
        raise NotImplementedError

    @abstractmethod
    def to_lp_file(self, docplex_model: DOCplexModel, filepath: str) -> None:
        """
        Transform DOCplex to LP representation

        Parameters
        ----------
        docplex_model: docplex.mp.model.Model
            DOCplex problem description
        filepath: str
            .lp file path where result should be stored
        """
        raise NotImplementedError

    @abstractmethod
    def to_lp_string(self, docplex_model: DOCplexModel) -> str:
        """
        Transform DOCplex to LP representation

        Parameters
        ----------
        docplex_model: docplex.mp.model.Model
            DOCplex problem description
        Returns
        -------
        str
            LP representation
        """
        raise NotImplementedError

    @abstractmethod
    def to_qubo_matrix(
        self, docplex_model: DOCplexModel
    ) -> Tuple[List[List[float]], partial]:
        """
        Transform DOCplex model to QUBO matrix

        Parameters
        ----------
        docplex_model: docplex.mp.model.Model
            DOCplex problem description

        Returns
        -------
        Tuple[List[List[float]], partial]
            QUBO matrix representation and inverter
        """
        raise NotImplementedError

    @abstractmethod
    def to_bqm(
        self, docplex_model: DOCplexModel
    ) -> Tuple[dimod.BinaryQuadraticModel, CQMToBQMInverter]:
        """
        Transform DOCplex model to BQM model

        Parameters
        ----------
        docplex_model: docplex.mp.model.Model
            DOCplex problem description

        Returns
        -------
        Tuple[dimod.BinaryQuadraticModel, CQMToBQMInverter]
            BQM representation and inverter
        """
        raise NotImplementedError

    @abstractmethod
    def to_cqm(self, docplex_model: DOCplexModel) -> ConstrainedQuadraticModel:
        """
        Transform DOCplex model to CQM model

        Parameters
        ----------
        docplex_model: docplex.mp.model.Model
            DOCplex problem description

        Returns
        -------
        ConstrainedQuadraticModel
            CQM representation
        """
        raise NotImplementedError
