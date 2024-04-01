# FIXME: need >=0.14 and HA depends on 0.13.1 right now

from typing import Any, Callable, List

class Schema:
    def __init__(self, config: dict, extra: int | None = None) -> None: ...

class Required:
    def __init__(self, name: str) -> None: ...

class All:
    def __init__(
        self, *args: List[Callable[[Any], Any]] | Callable[[Any], Any]
    ) -> None: ...

ALLOW_EXTRA: int = ...
