import logging

from pandas import DataFrame

from ._do_sheet_parser import DoSheetParser
from ._regex_lib import TB1 as config
from .di_signal import DiSignal
from .signals_collection import SignalsCollection


class DiSheetParser(DoSheetParser):

    def __init__(self, sheet: DataFrame) -> None:
        self._logs_owner: str = self.__class__.__name__
        self._sheet = sheet

        self._result = None


    def __parse_signal(self, input_value: str) -> bool:
        return '+' in input_value

    def start(self) -> None:
        if not list(config['Di']['regex']['columns']['validate']['names'].keys()) == list(self._sheet):
            logging.error(f'{self._logs_owner}: передан неверный лист аналоговых сигналов')

        out = []

        for row in self._sheet.itertuples(False, 'Signal'):
            new = DiSignal()

            try:
                new.plc_module = self._parse_plc_module(row.plc_module)
                new.plc_channel = int(row.plc_channel)
                new.variable = self._parse_variable(row.variable)
                new.name = self._clean_name(row.name)
                # new.formated_name = self._format_signal_name(row.name)
                new.logic_value = self._parse_logic_value(row.logic_value)
                new.alarm_signal = self.__parse_signal(row.alarm_signal)
                new.warning_signal = self.__parse_signal(row.warning_signal)
                new.error_signal = self.__parse_signal(row.error_signal)
                new.tele_signal = self.__parse_signal(row.tele_signal)

                logging.info(f'{self._logs_owner}:{row.variable}: значения успешно получены')

            except Exception as error:
                logging.error(f'{self._logs_owner}:{row.variable}: ошибка парсинга - {error}')

            finally:
                out.append(new)
                
        self._result = SignalsCollection(out)
