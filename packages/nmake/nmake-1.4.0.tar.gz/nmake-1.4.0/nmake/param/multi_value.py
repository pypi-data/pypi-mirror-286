from . import param


class MultiValue(param.Param):

    def __init__(self, prefix: str = "", values: list[str] = None):
        self.prefix = prefix
        self.values = values or []

    def is_active(self) -> bool:
        return len(self.values) > 0

    def get_value(self) -> str:
        return " ".join(f"{self.prefix}{value}" for value in self.values)
