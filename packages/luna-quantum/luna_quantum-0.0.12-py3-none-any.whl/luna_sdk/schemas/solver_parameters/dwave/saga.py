from typing import Any, Literal, Optional, Tuple

from pydantic import BaseModel, Field


class SAGAParameters(BaseModel):
    """
    Parameters for the Simulated Annealing Assisted Genetic Algorithm (SAGA).
    SAGA combines the principles of genetic algorithms and simulated annealing to solve optimization problems.

    Parameters
    ----------
    p_size: int
        The population size for the genetic algorithm.
    p_inc_num: int
        The increment number for the population size.
    p_max: Optional[int]
        The maximum population size.
    pct_random_states: float
        The percentage of random states in the initial population.
    mut_rate: float
        The mutation rate for the genetic algorithm. Min: 0.0, Max: 1.0
    rec_rate: int
        The recombination rate for the genetic algorithm.
    rec_method: Literal['cluster_moves', 'one_point_crossover', 'random_crossover']
        The recombination method for the genetic algorithm.
    select_method: Literal['simple', 'shared_energy']
        Method used for the selection phase in the genetic algorithm.
    num_sweeps: int
        The number of sweeps for the simulated annealing.
    num_sweeps_inc_factor: float
        The increment factor for the number of sweeps.
    num_sweeps_inc_max: Optional[int]
        The maximum increment for the number of sweeps.
    beta_range_type: Literal['default', 'percent', 'fixed', 'inc']
        The type of beta range for the simulated annealing.
    beta_range: Optional[Tuple[float, float]]
        The beta range for simulated annealing.
    target: Optional[float]
        The target solution for the optimization problem.
    atol: float
        The absolute tolerance for the optimization problem.
    rtol: float
        The relative tolerance for the optimization problem.
    timeout: float
        The timeout for the optimization problem in seconds.
    max_iter: Optional[int]
        The maximum number of iterations for the optimization problem.
    return_overhead: bool
        Whether to return the overhead of the optimization problem.
    """

    p_size: int = 20
    p_inc_num: int = 5
    p_max: Optional[int] = 160
    pct_random_states: float = 0.25
    mut_rate: float = Field(default=0.5, ge=0.0, le=1.0)
    rec_rate: int = 1
    rec_method: Literal["cluster_moves", "one_point_crossover", "random_crossover"] = (
        "random_crossover"
    )
    select_method: Literal["simple", "shared_energy"] = "simple"
    num_sweeps: int = 10
    num_sweeps_inc_factor: float = 1.2
    num_sweeps_inc_max: Optional[int] = 7_000
    beta_range_type: Literal["default", "percent", "fixed", "inc"] = "default"
    beta_range: Optional[Tuple[float, float]] = None
    target: Optional[float] = None
    atol: float = 0.0
    rtol: float = 0.0
    timeout: float = 60.0
    max_iter: Optional[int] = 100
    return_overhead: bool = False
