from dataclasses import dataclass

from transliterate import translit

from .plc_module import PLCModule


@dataclass
class Signal(object):
    
    def __init__(self) -> None:
        '''
        Дата-класс. Шаблон для наследования.
        '''
        self.variable: None | str
        self.name: None | str
        self.formated_name: None | str
        self.plc_module: None | PLCModule
        self.plc_channel: None | int

    def isused(self) -> bool:
        return translit(self.name, 'ru', reversed=True).lower() != 'rezerv'

    def isprotected(self) -> bool:
        pass  # FIXME Заглушка метода для родителя

    def set_formated_name(self, inp_name: str):
        self.formated_name = inp_name

    def __repr__(self) -> str:
        params: str = '(' + '; '.join(f'{key}: {value}' for key, value in self.__dict__.items()) + ')'
        return self.__class__.__name__ + params
