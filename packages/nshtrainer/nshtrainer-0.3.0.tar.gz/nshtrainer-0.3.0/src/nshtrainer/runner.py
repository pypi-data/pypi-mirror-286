from typing import Generic

from nshrunner import RunInfo
from nshrunner import Runner as _Runner
from typing_extensions import TypeVar, TypeVarTuple, Unpack, override

from .model.config import BaseConfig

TConfig = TypeVar("TConfig", bound=BaseConfig, infer_variance=True)
TArguments = TypeVarTuple("TArguments", default=Unpack[tuple[()]])
TReturn = TypeVar("TReturn", infer_variance=True)


class Runner(
    _Runner[TReturn, TConfig, Unpack[TArguments]],
    Generic[TReturn, TConfig, Unpack[TArguments]],
):
    @override
    @classmethod
    def default_validate_fn(cls, config: TConfig, *args: Unpack[TArguments]) -> None:
        super().default_validate_fn(config, *args)

    @override
    @classmethod
    def default_info_fn(cls, config: TConfig, *args: Unpack[TArguments]) -> RunInfo:
        run_info = super().default_info_fn(config, *args)
        return {
            **run_info,
            "id": config.id,
            "base_dir": config.directory.project_root,
        }
