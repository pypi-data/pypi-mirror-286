import logging
import re

from pandas import DataFrame
from transliterate import translit

from ._regex_lib import PARSER as config
from .plc_module import PLCModule
from .signals_collection import SignalsCollection


class SheetParser:

    def __init__(self, sheet: DataFrame) -> None:
        self._logs_owner: str = self.__class__.__name__
        self._sheet = sheet

        self._result = None

    def _clean_name(self, raw_name: str) -> str:
        return re.sub(r'[\n\t]|\s{2,}', '', raw_name.strip())

    def _parse_variable(self, raw_variable: str) -> str:
        return translit(raw_variable, 'ru', reversed=True)
    
    def _parse_plc_module(self, raw_string: str) -> str:
        try:
            raw_string = translit(raw_string, 'ru', reversed=True)
            params = re.findall(config['signals']['find_plc_module'], raw_string)[0]

            if len(params) != 4:
                raise ValueError('ошибка сопоставления с шаблоном')
            
            out = PLCModule()
            out.type, out.module = params[::3]
            out.channels_count, out.some_num = map(int, params[1:3])
            
        except Exception as error:
            logging.error(f'{self._logs_owner}: ошибка парсинга "{raw_string.replace('\n', '')}" модуля плк - {error}')
            out = None

        finally:
            return out

    def _get_result(self) -> SignalsCollection | None:
        if out := self._result:
            return out
        else:
            logging.error(f'{self._logs_owner}: перед получением результатов парсинга воспользуйтесь методом start()')
            raise IndentationError
