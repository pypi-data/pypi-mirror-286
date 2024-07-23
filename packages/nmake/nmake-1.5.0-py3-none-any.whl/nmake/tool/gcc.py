from nmake.param import command
from nmake.param.optional import Optional
from nmake.param.single_value import SingleValue
from nmake.param.multi_value import MultiValue
from nmake.param.make import make_param_list_, make_class_param_list


class GccInfo:
    def __init__(self,
                 include_dirs: list[str] = None,
                 is_static: bool = False,
                 md: bool = False,
                 debugger: bool = False,
                 optimize: str = None,
                 flag: list[str] = None,
                 nos: list[str] = None,
                 ):
        self.include_dirs: list[str] = include_dirs
        self.is_static: bool = is_static
        self.md: bool = md
        self.debugger: bool = debugger
        self.optimize: str = optimize
        self.flag: list[str] = flag
        self.nos: list[str] = nos


class Gcc:
    def __init__(self,
                 target: str = "g++",
                 info: GccInfo = None,
                 sources: list[str] = None,
                 output: str = None,
                 ):
        self.target: str = target

        info = info or GccInfo()

        self._sources: MultiValue = MultiValue(values=sources)
        self._output: SingleValue = SingleValue("-o", output, output is not None)
        self._include_dirs: MultiValue = MultiValue(prefix="-I", values=info.include_dirs)
        self._is_static: Optional = Optional("-static", info.is_static)
        self._md: Optional = Optional("-MD", info.md)
        self._debugger: Optional = Optional("-g", info.debugger)
        self._optimize: SingleValue = SingleValue("-O", info.optimize or "", info.optimize is not None)
        self._flags: dict[str, Optional] = {}
        self._nos: dict[str, Optional] = {}

        flag_no = [
            "builtin", "strict-aliasing", "omit-frame-pointers", "stack-protector", "pie", "pic", "exceptions", "rtti"
        ]
        flag = ["permissive"]
        no = ["stdlib"]
        for f in flag_no:
            self._flags[f"no-{f}"] = Optional(f"-fno-{f}")
        for f in flag:
            self._flags[f] = Optional(f"-f{f}")
        for n in no:
            self._nos[n] = Optional(f"-no{n}")

        if info.flag:
            for f in info.flag:
                if f not in self._flags:
                    continue
                self._flags[f].on()

        if info.nos:
            for n in info.nos:
                if n not in self._nos:
                    continue
                self._nos[n].on()

    def requires_extent_name(self) -> str:
        return ".cpp"

    def create_cmd(self) -> command.Command:
        result: command.Command = command.Command(self.target)
        result.option += make_class_param_list(self)
        result.option += make_param_list_([f for f in self._flags.values()])
        result.option += make_param_list_([n for n in self._nos.values()])
        return result

    def set_sources(self, sources: list[str]) -> None:
        self._sources.values = sources or []

    def set_output(self, output: str) -> None:
        self._output.set_value(output)
        self._output.on()


class CppInfo(GccInfo):
    pass

class Cpp(Gcc):
    def __init__(self,
                 target: str = "gcc",
                 info: CppInfo = None,
                 sources: list[str] = None,
                 output: str = None,
                 ):
        super().__init__(target, info, sources, output)

    def create_cmd(self) -> command.Command:
        result: command.Command = super().create_cmd()
        result.option.insert(0, "-E")
        return result

    def requires_extent_name(self) -> str:
        return ".c"
