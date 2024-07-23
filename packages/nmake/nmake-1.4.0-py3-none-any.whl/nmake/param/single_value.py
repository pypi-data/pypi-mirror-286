from . import param


class SingleValue(param.Param):

    def __init__(self, prefix: str, value: str = "", active: bool = False):
        self.prefix = prefix
        self.value = value
        super().__init__(active)

    def set_value(self, new_value: str):
        self.value = new_value

    def get_value(self) -> str:
        return self.prefix + self.value

