from luna_sdk.schemas.solver_parameters.dwave import SAGAParameters


class QAGAParameters(SAGAParameters):
    """
    Parameters for the Quantum Assisted Genetic Algorithm (QAGA).
    QAGA combines the principles of genetic algorithms and quantum annealing to solve optimization problems.

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
