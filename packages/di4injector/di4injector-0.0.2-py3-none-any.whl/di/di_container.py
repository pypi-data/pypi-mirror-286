from __future__ import annotations

from typing import Optional, Type

from injector import Injector, T

from di import DI


class DIContainer:
    __shared: Optional[DIContainer] = None

    def __init__(self):
        self.__injector = Injector([])

    @classmethod
    def instance(cls) -> DIContainer:
        if cls.__shared is None:
            cls.__shared = DIContainer()
        return cls.__shared

    def register(self, *di: DI) -> None:
        for e in di:
            self.__injector.binder.install(e)

    def resolve(self, interface: Type[T]) -> T:
        return self.__injector.get(interface)
