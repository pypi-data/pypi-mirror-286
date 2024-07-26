from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Type, Dict, Set, Any, Optional

from injector import Module, T, Binder, singleton


@dataclass(init=True, frozen=True)
class Profile:
    values: Set[str]

    def match(self, actives: Set[str]) -> bool:
        return all([name in actives for name in self.values])

    def __hash__(self):
        return hash(str(sorted([name for name in self.values])))

    def __eq__(self, other):
        if (other is None) or (not isinstance(other, Profile)):
            return False
        return self.values == other.values


class Switcher:
    ENV_NAME = "DI_PROFILE_ACTIVES"
    PROFILE_ACTIVES: Set[str] = set(os.getenv(ENV_NAME, "").split(","))

    @classmethod
    def get(cls, classes: Dict[Profile, Any], default: Optional[T]) -> Any:
        for profile, a_class in classes.items():
            if profile.match(cls.PROFILE_ACTIVES):
                return a_class
        return default


@dataclass(init=True, frozen=False, unsafe_hash=True)
class DI(Module):
    interface: Type[T]
    classes: Dict[Profile, T]
    default: Optional[T]

    @staticmethod
    def of(interface: Type[T], classes: Dict[str, T], default: Optional[T] = None) -> DI:
        return DI(
            interface,
            {Profile(set(actives.split(','))): a_class for actives, a_class in classes.items()},
            default
        )

    def configure(self, binder: Binder) -> None:
        binder.bind(self.interface, to=Switcher.get(self.classes, self.default), scope=singleton)
