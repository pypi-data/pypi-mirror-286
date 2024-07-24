from dataclasses import dataclass
from typing import Generic

from nshrunner import Runner as _Runner
from typing_extensions import Concatenate, TypeVar, TypeVarTuple, Unpack, override

from .model.config import BaseConfig

TConfig = TypeVar("TConfig", bound=BaseConfig, infer_variance=True)
TArguments = TypeVarTuple("TArguments")
TReturn = TypeVar("TReturn", infer_variance=True)


@dataclass(frozen=True)
class Runner(
    _Runner[Unpack[tuple[TConfig, Unpack[TArguments]]], TReturn],
    Generic[TConfig, Unpack[TArguments], TReturn],
):
    @override
    def default_validate_fn():
        pass
