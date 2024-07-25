from pydantic import BaseModel

from luna_sdk.schemas.solver_parameters.dwave import QBSOLVLike, SimulatedAnnealing


class QbSolvLikeSimulatedAnnealingParameters(BaseModel):
    """
    QBSolv Like Simulated Annealing breaks down the problem and solves the parts individually using a classic solver that uses Simulated Annealing.
    This particular implementation uses hybrid.SimulatedAnnealingSubproblemSampler
    (https://docs.ocean.dwavesys.com/projects/hybrid/en/stable/reference/samplers.html#simulatedannealingsubproblemsampler)
    as a sampler for the subproblems to achieve a QBSolv like behaviour.

    Parameters
    ----------
    qbsolv_like: QBSOLVLike
        Parameters for the QbSolveLike solver.
    simulated_annealing: SimulatedAnnealing
        Parameters for the Simulated Annealing.
    """

    qbsolv_like: QBSOLVLike = QBSOLVLike()
    simulated_annealing: SimulatedAnnealing = SimulatedAnnealing()
