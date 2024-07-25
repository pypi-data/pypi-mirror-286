from enum import Enum


class InputType(str, Enum):
    bqm_spin = "bqm_spin"
    bqm_binary = "bqm_binary"
    cqm = "cqm"
    lp = "lp"
    aq = "aq"
    qubo = "qubo"
