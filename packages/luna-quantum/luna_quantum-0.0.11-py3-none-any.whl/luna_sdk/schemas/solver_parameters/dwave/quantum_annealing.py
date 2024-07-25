from pydantic import BaseModel

from luna_sdk.schemas.solver_parameters.dwave import Embedding, SamplingParams


class QuantumAnnealingParameters(BaseModel):
    """
    Parameters for the Quantum Annealing solver.

    Parameters
    ----------
    embedding: Embedding
        Parameters for the auto embedding.
    sampling_params: SamplingParams
        Parameters for the sampling. See https://docs.dwavesys.com/docs/latest/c_solver_parameters.html
        for more details.
    """

    embedding: Embedding = Embedding()
    sampling_params: SamplingParams = SamplingParams()
