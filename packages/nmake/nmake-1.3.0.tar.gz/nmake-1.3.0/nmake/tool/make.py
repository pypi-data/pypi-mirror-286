import os
from ..param import command
from . import utility


def make(sources: list[str], output: str, *tools) -> list[str]:
    if len(tools) == 0:
        raise Exception("")
    if len(sources) == 0:
        raise Exception("")

    cmds: list[command.Command] = list()
    temp_file: list[str] = []

    if hasattr(tools[0], "requires_extent_name"):
        tools = (utility.Copy(),) + tools

    current_sources = sources
    for first, second in zip(tools, tools[1:]):
        extent_name = "" if not hasattr(second, "requires_extent_name") else second.requires_extent_name()
        os.makedirs(os.path.dirname(os.path.abspath(output)), exist_ok=True)
        step_output = os.path.join(os.path.dirname(output), os.path.basename(current_sources[
                                                                                 0]) + extent_name)  # os.path.splitext(os.path.basename(current_sources[0]))[0] + extent_name)
        first.set_sources(current_sources)
        first.set_output(step_output)
        current_sources = [step_output]
        cmds.append(first.create_cmd())
        temp_file.append(step_output)

    if len(tools) > 1:
        tools[-1].set_sources(current_sources)
        tools[-1].set_output(output)
        cmds.append(tools[-1].create_cmd())

    command.run(cmds)
    return temp_file
