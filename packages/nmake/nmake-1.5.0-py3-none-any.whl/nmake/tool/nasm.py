from nmake.param import command
from nmake.param.optional import Optional
from nmake.param.multi_value import MultiValue
from nmake.param.single_value import SingleValue
from nmake.param.make import make_class_param_list

class NasmInfo:
    def __init__(self,
                 is_static: bool = False,
                 md: bool = False,
                 debugger: str = None,
                 format: str = None,
                 ):
        self.is_static: bool = is_static
        self.md: bool = md
        self.debugger: str = debugger
        self.format: str = format

class Nasm:

    def __init__(self,
                 target: str = "nasm",
                 info: NasmInfo = None,
                 sources: list[str] = None,
                 output: str = None,
                 ):
        self.target: str = target

        info = info or NasmInfo()

        self._sources: MultiValue = MultiValue(values=sources)
        self._output: SingleValue = SingleValue(prefix="-o", value=output, active=output is not None)
        self._is_static: Optional = Optional("-static", info.is_static)
        self._1_md: Optional = Optional("-MD", info.md)
        self._2_debugger: SingleValue = SingleValue("-g", info.debugger, info.debugger is not None)
        self._format: SingleValue = SingleValue("-f ", info.format, info.format is not None)

    def create_cmd(self) -> command.Command:
        return command.Command(self.target, make_class_param_list(self))

    def set_sources(self, sources: list[str]) -> None:
        self._sources.values = sources or []

    def set_output(self, output: str) -> None:
        self._output.set_value(output)
        self._output.on()

    def requires_extent_name(self) -> str:
        return ".asm"