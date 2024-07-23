from . import param


class Optional(param.Param):
    def __init__(self, value: str, active: bool = False) -> None:
        self.value = value
        super().__init__(active)

    def get_value(self) -> str:
        return self.value
