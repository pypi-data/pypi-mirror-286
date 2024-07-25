from typing import Any, Dict, Literal, Optional, Union

from pydantic import BaseModel, ConfigDict


class ServiceConfig(BaseModel):
    channel: Optional[Literal["ibm_cloud", "ibm_quantum"]] = "ibm_quantum"
    url: Optional[str] = None
    name: Optional[str] = None
    instance: Optional[str] = None
    proxies: Optional[dict] = None
    verify: Optional[bool] = None
    channel_strategy: Optional[str] = None

    model_config = ConfigDict(extra="forbid")


class StandardParameters(BaseModel):
    backend: Optional[Union[str, Dict[str, Any]]] = "AerSimulator"
    shots: int = 1024
    dynamical_decoupling: Dict[str, Any] = {}
    optimizer: str = "COBYLA"
    maxiter: int = 10
    optimization_level: int = 2
    service_config: ServiceConfig = ServiceConfig()

    model_config = ConfigDict(extra="forbid")
