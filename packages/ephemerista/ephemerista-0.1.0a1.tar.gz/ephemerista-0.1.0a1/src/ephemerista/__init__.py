from pathlib import Path

import lox_space as lox
import pydantic
from pydantic import ConfigDict
from pydantic.alias_generators import to_camel


class BaseModel(pydantic.BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


UT1Provider = lox.UT1Provider

_UT1_PROVIDER: UT1Provider | None = None


def init_provider(eop_file: str | Path):
    if isinstance(eop_file, Path):
        eop_file = str(eop_file)
    global _UT1_PROVIDER  # noqa: PLW0603
    _UT1_PROVIDER = lox.UT1Provider(eop_file)


def get_provider() -> UT1Provider:
    if _UT1_PROVIDER is None:
        msg = "UT1 provider not initialized. Call `init_provider` first."
        raise ValueError(msg)
    return _UT1_PROVIDER


type Vec3 = tuple[float, float, float]
