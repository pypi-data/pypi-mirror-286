from src.nmake.param import command


class Copy:

    def __init__(self):
        self.output = None
        self.sources = None

    def set_sources(self, sources: list[str]) -> None:
        self.sources = sources

    def set_output(self, output: str) -> None:
        self.output = output

    def create_cmd(self) -> command.Command:
        result = command.Command("cp")
        result.option += self.sources
        result.option.append(self.output)
        return result
