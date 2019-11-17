import abc
from typing import List, Dict, Any

from bs4 import BeautifulSoup


class FieldParser(abc.ABC):
    @property
    @abc.abstractmethod
    def output_fields(self) -> List[str]:
        raise NotImplementedError()

    @abc.abstractmethod
    def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
        raise NotImplementedError()


def _identity_parser(field_name: str) -> FieldParser:
    class _Parser(FieldParser):
        @property
        def output_fields(self) -> List[str]:
            return [field_name]

        def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
            return {field_name: field.text}
    return _Parser()


def _str_to_int_parser(field_name: str) -> FieldParser:
    class _Parser(FieldParser):
        @property
        def output_fields(self) -> List[str]:
            return [field_name]

        def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
            field_str = field.text
            return {field_name: int(field_str)}
    return _Parser()


def _nullable_str_to_int_parser(field_name: str) -> FieldParser:
    class _Parser(FieldParser):
        @property
        def output_fields(self) -> List[str]:
            return [field_name]

        def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
            field_str = field.text
            if not field_str:
                return {field_name: None}
            return {field_name: int(field_str)}
    return _Parser()


def _str_to_float_parser(field_name: str) -> FieldParser:
    class _Parser(FieldParser):
        @property
        def output_fields(self) -> List[str]:
            return [field_name]

        def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
            field_str = field.text
            return {field_name: float(field_str)}
    return _Parser()


def _nullable_str_to_float_parser(field_name: str) -> FieldParser:
    class _Parser(FieldParser):
        @property
        def output_fields(self) -> List[str]:
            return [field_name]

        def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
            field_str = field.text
            if not field_str:
                return {field_name: None}
            return {field_name: float(field_str)}
    return _Parser()


def _str_percentage_to_float_parser(field_name: str) -> FieldParser:
    class _Parser(FieldParser):
        @property
        def output_fields(self) -> List[str]:
            return [field_name]

        def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
            field_str = field.text
            percentage = float(field_str[:-1])
            return {field_name: percentage / 100.}
    return _Parser()


def _nullable_str_percentage_to_float_parser(field_name: str) -> FieldParser:
    class _Parser(FieldParser):
        @property
        def output_fields(self) -> List[str]:
            return [field_name]

        def parse(self, field: BeautifulSoup) -> Dict[str, Any]:
            field_str = field.text
            if not field_str:
                return {field_name: None}
            percentage = float(field_str[:-1])
            return {field_name: percentage / 100.}
    return _Parser()
