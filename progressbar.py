import shutil
from typing import Iterable


class SingleProgressBar:
    def __init__(self, lst: Iterable, name: str = ''):
        self.index = 0
        self.list = list(lst)
        self.name = name

    def __iter__(self):
        return self

    def __next__(self):
        self.length = shutil.get_terminal_size()[0]
        dash = '\u2501'
        right_dash = '\u2578'
        name = f"{self.name}: " if self.name else ''
        length = self.length - 2 * len(str(len(self.list))) - 2 - len(name)
        progress = int(self.index / len(self.list) * length)
        print(f"\r{name}\033[1;34m{progress * dash}{'' if self.index == len(self.list) else right_dash}\033[90m"
              f"{max(0, length - progress - 1) * dash}\033[0m"
              f"{' ' *  (len(str(len(self.list))) - len(str(self.index)) + 1)}\033[1;34m{self.index}\033[90m/\033"
              f"[1;32m{len(self.list)}\033[0m", end='')
        if self.index == len(self.list):
            raise StopIteration
        self.index += 1
        return self.list[self.index - 1]