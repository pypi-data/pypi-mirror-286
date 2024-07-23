import os
from ..param import command
from . import utility
import os


class Info:
    def __init__(self,
                 sources: list[str],
                 output: str,
                 tools: list,
                 cwd: str = os.path.dirname(os.path.abspath(__file__)),
                 ):
        self.sources: list[str] = sources
        self.output: str = output
        self.cwd: str = cwd
        self.tools = tools


class Context:
    def __init__(self, cmds: list[command.Command], temp_file=None):
        if temp_file is None:
            temp_file = list()
        self.cmds: list[command.Command] = cmds
        self.temp_file: list[str] = temp_file


def build_context(info: Info) -> Context:
    if len(info.tools) == 0:
        raise Exception("")
    if len(info.sources) == 0:
        raise Exception("")

    cmds: list[command.Command] = list()
    temp_file: list[str] = []

    if hasattr(info.tools[0], "requires_extent_name"):
        info.tools = [utility.Copy(), ] + info.tools

    current_sources = info.sources
    for first, second in zip(info.tools, info.tools[1:]):
        extent_name = "" if not hasattr(second, "requires_extent_name") else second.requires_extent_name()
        os.makedirs(os.path.dirname(os.path.abspath(info.output)), exist_ok=True)
        step_output = os.path.join(os.path.dirname(info.output), os.path.basename(current_sources[
                                                                                      0]) + extent_name)  # os.path.splitext(os.path.basename(current_sources[0]))[0] + extent_name)
        first.set_sources(current_sources)
        first.set_output(step_output)
        current_sources = [step_output]
        cmds.append(first.create_cmd())
        temp_file.append(step_output)

    if len(info.tools) > 1:
        info.tools[-1].set_sources(current_sources)
        info.tools[-1].set_output(info.output)
        cmds.append(info.tools[-1].create_cmd())

    for cmd in cmds:
        cmd.cwd = info.cwd

    return Context(cmds, temp_file)


def make(info: Info) -> list[str]:
    context = build_context(info)
    command.run(context.cmds)
    return context.temp_file
