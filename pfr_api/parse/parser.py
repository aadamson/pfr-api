import abc
from datetime import date, datetime, time
from typing import Any, Dict, List, Type

from bs4 import BeautifulSoup


class RowParser(abc.ABC):
    @property
    @abc.abstractmethod
    def output_fields(self) -> List[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
        raise NotImplementedError()


class UnaryFieldParser(RowParser):
    def __init__(self, field_name: str):
        self.field_name = field_name

    @property
    def output_fields(self) -> List[str]:
        return [self.field_name]


class DateStringParser(UnaryFieldParser):
    def __init__(self, field_name: str, fmt: str = '%Y-%m-%d'):
        super().__init__(field_name)
        self.fmt = fmt

    def parse(self, field: BeautifulSoup) -> Dict[str, date]:
        date_string = field.text
        return {
            self.field_name: datetime.strptime(date_string, self.fmt).date()
        }


class TimeParser(UnaryFieldParser):
    def __init__(self, field_name: str, fmt: str = '%H:%M%p %Z'):
        super().__init__(field_name)
        self.fmt = fmt

    def parse(self, field: BeautifulSoup) -> Dict[str, time]:
        date_string = field.text
        return {
            self.field_name: datetime.strptime(date_string, self.fmt).time()
        }


class IdentityParser(UnaryFieldParser):
    def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
        return {self.field_name: field.text}


class StrToIntParser(UnaryFieldParser):
    def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
        field_str = field.text
        return {self.field_name: int(field_str)}


class NullableStrToIntParser(UnaryFieldParser):
    def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
        field_str = field.text
        if not field_str:
            return {self.field_name: None}
        return {self.field_name: int(field_str)}


class StrToFloatParser(UnaryFieldParser):
    def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
        field_str = field.text
        return {self.field_name: float(field_str)}


class NullableStrToFloatParser(UnaryFieldParser):
    def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
        field_str = field.text
        if not field_str:
            return {self.field_name: None}
        return {self.field_name: float(field_str)}


class StrPercentageToFloatParser(UnaryFieldParser):
    def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
        field_str = field.text
        percentage = float(field_str[:-1])
        return {self.field_name: percentage / 100.}


class NullableStrPercentageToFloatParser(UnaryFieldParser):
    def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
        field_str = field.text
        if not field_str:
            return {self.field_name: None}
        percentage = float(field_str[:-1])
        return {self.field_name: percentage / 100.}


class PlayerRowParser(RowParser):
    @property
    def output_fields(self):
        return ['player_id', 'player_csk',  'player_name']

    def parse(self, field: BeautifulSoup):
        player_id = field['data-append-csv']
        player_csk = field['csk']
        player_name = field.text
        return {
            'player_id': player_id,
            'player_csk': player_csk,
            'player_name': player_name
        }
