import logging
# import os
from types import FunctionType

from .signals_collection import SignalsCollection


class ParsedTB1Collection(dict):

    @property
    def __logs_owner(self) -> str:
        return self.__class__.__name__

    def filter(self, key: FunctionType):
        """Фильтрация сигналов в коллекции"""
        result = ParsedTB1Collection()
        try:
            if not isinstance(key, FunctionType):
                raise TypeError(f"переданный параметр 'key' не является функцией")

            for type, collection in self.items():
                if filtered_collection := SignalsCollection(
                    signal for signal in collection if key(signal)
                ):
                    result[type] = filtered_collection
            return result if len(result) else None

        except Exception as error:
            logging.error(f"{self.__logs_owner}: ошибка фильтрации сигналов: {error}")
            return

    # def __str__(self):
    #     out = []
    #     for signal_type, signals in self.items():
    #         boarder: str = f" {signal_type} ".center(
    #             os.get_terminal_size().columns, "-"
    #         )
    #         out.append(boarder + "\n".join(map(str, signals)))
    #     return "\n\n".join(out)
