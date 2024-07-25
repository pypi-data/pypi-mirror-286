from typing import Optional, List

from pydantic import BaseModel


class QaoaParameters(BaseModel):
    """
    The Quantum Approximate Optimization Algorithm ([QAOA](https://arxiv.org/abs/1411.4028))
    solves combinatorial optimization problems by approximating the solution.

    The Quantum Approximate Optimization Algorithm (QAOA) belongs to the class of hybrid quantum algorithms
    (leveraging both classical as well as quantum compute), that are widely believed to be the working horse
    for the current NISQ (noisy intermediate-scale quantum) era. In this NISQ era QAOA is also an emerging
    approach for benchmarking quantum devices and is a prime candidate for demonstrating a practical
    quantum speed-up on near-term NISQ device.
    """

    aws_provider: str = ""
    aws_device: str = ""
    seed: Optional[int] = 385920
    reps: Optional[int] = 1
    initial_values: Optional[List[float]] = None
    shots: Optional[int] = 1024
    optimizer_params: Optional[dict] = None
