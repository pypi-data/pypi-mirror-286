from collections.abc import Mapping
from logging import Logger as _Logger
from logging import root
from types import TracebackType
from typing import Callable, Type

from cacheline.typed import T

_SysExcInfoType = tuple[type[BaseException], BaseException, TracebackType | None] | tuple[None, None, None]
_ExcInfoType = None | bool | _SysExcInfoType | BaseException

_parent = _Logger
if root.manager.loggerClass is not None:  # pylint:disable=no-member
    _parent: Type[_Logger] = root.manager.loggerClass  # pylint:disable=no-member


class Logger(_parent):
    def report(
        self,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Mapping[str, object] | None = None,
    ) -> None: ...

    def set_default_extra(self, extra: Mapping[str, object]) -> None: ...

    def catch(self, func: Callable[..., T]) -> Callable[..., T]: ...