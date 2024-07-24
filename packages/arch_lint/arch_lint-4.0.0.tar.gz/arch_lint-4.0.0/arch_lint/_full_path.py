from __future__ import (
    annotations,
)

from . import (
    _utils,
)
from dataclasses import (
    dataclass,
    field,
)
from importlib.util import (
    find_spec,
)
from typing import (
    NoReturn,
    Optional,
    Union,
)


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class FullPathModule:
    "Represents a full path module that exist"
    _inner: _Private = field(repr=False, hash=False, compare=False)
    module: str

    @staticmethod
    def from_raw(raw: str) -> Union[FullPathModule, Exception]:
        try:
            module = find_spec(raw)
            if module is not None:
                return FullPathModule(_Private(), raw)
            return ModuleNotFoundError(raw)
        except ValueError as err:
            return err

    @classmethod
    def assert_module(cls, raw: str) -> Union[FullPathModule, NoReturn]:
        result = cls.from_raw(raw)
        return _utils.raise_or_value(result)

    @property
    def name(self) -> str:
        return self.module.split(".")[-1]

    @property
    def parent(self) -> Optional[FullPathModule]:
        parent = ".".join(self.module.split(".")[:-1])
        result = self.from_raw(parent)
        if isinstance(result, Exception):
            return None
        return result

    def new_child(self, module: str) -> Optional[FullPathModule]:
        joined = ".".join([self.module, module])
        result = self.from_raw(joined)
        if isinstance(result, Exception):
            return None
        return result

    def assert_child(self, module: str) -> Union[FullPathModule, Exception]:
        result = self.new_child(module)
        if result:
            return result
        return ModuleNotFoundError(f"Children of {self} i.e. {module}")

    def is_descendant_of(self, module: FullPathModule) -> bool:
        if self != module:
            return self.module.startswith(module.module)
        return False

    def __repr__(self) -> str:
        return self.module
