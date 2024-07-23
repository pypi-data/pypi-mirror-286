import subprocess


class Command:

    def __init__(self, target: str, option=None, cwd: str = None):
        self.target: str = target
        self.option: list[str] = option or []
        self.cwd: str = cwd

    def as_list(self) -> list[str]:
        return [self.target] + self.option

    def run(self) -> None:
        print(self.as_list())
        subprocess.run(self.as_list(), cwd=self.cwd)


def run(*cmds):
    if len(cmds) == 1 and isinstance(cmds[0], list):
        for cmd in cmds[0]:
            cmd.run()
    else:
        for cmd in cmds:
            cmd.run()
