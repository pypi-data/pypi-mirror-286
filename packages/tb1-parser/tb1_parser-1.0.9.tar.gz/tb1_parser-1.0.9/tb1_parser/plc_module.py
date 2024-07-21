from dataclasses import dataclass


@dataclass
class PLCModule:

    def __init__(self) -> None:
        self.type: str
        self.channels_count: int
        self.some_num: int # FIXME Переименовать аргумент
        self.module: str

    def __repr__(self) -> str:
        return f'{self.type}-{self.channels_count}k{self.some_num} ({self.module})'
