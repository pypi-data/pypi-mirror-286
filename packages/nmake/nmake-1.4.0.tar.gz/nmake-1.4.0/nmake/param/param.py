from abc import ABC, abstractmethod


class Param(ABC):

    def __init__(self, active: bool = False) -> None:
        self._active: bool = active

    def is_active(self) -> bool:
        return self._active

    def set_active(self, value: bool) -> None:
        self._active = value

    def on(self):
        self.set_active(True)

    def off(self) -> None:
        self.set_active(False)

    @abstractmethod
    def get_value(self) -> str:
        pass
