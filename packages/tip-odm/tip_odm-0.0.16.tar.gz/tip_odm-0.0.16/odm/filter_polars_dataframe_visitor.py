import polars as pl
from datetime import datetime
import re
from .models_definition import Definition
from .enums import FilterBinaryOperator, FilterBetweenOperator, FilterListOperator, FilterGroupOperator
from .models_query import FilterBinary, FilterBetween, FilterList, FilterGroup, FilterImpossible
from .filter_visitor import FilterVisitor
from .utils import convert_value


class FilterPolarsDataframeVisitor(FilterVisitor):
    def __init__(self, d: Definition, df: pl.DataFrame):
        super().__init__()
        self.d = d
        self.df = df
        self.property_dict = {p.key: p for p in self.d.properties}

    def visit_binary(self, f: FilterBinary) -> any:
        match f.operator:
            case FilterBinaryOperator.equals:
                return pl.col(self.__get_alias(f.key)) == self.__get_filter_value(f.value)
            case FilterBinaryOperator.not_equals:
                return ~(pl.col(self.__get_alias(f.key)) == self.__get_filter_value(f.value))
            case FilterBinaryOperator.greater_than:
                return pl.col(self.__get_alias(f.key)) > self.__get_filter_value(f.value)
            case FilterBinaryOperator.greater_than_or_equals:
                return pl.col(self.__get_alias(f.key)) >= self.__get_filter_value(f.value)
            case FilterBinaryOperator.less_than:
                return pl.col(self.__get_alias(f.key)) < self.__get_filter_value(f.value)
            case FilterBinaryOperator.less_than_or_equals:
                return pl.col(self.__get_alias(f.key)) <= self.__get_filter_value(f.value)
            case FilterBinaryOperator.like:
                return pl.col(self.__get_alias(f.key)).str.contains(r"(?i)" + re.escape(f.value))
            case FilterBinaryOperator.not_like:
                return ~pl.col(self.__get_alias(f.key)).str.contains(r"(?i)" + re.escape(f.value))

    def visit_between(self, f: FilterBetween) -> any:
        match f.operator:
            case FilterBetweenOperator.between:
                return pl.col(self.__get_alias(f.key)).is_between(
                    self.__get_filter_value(f.value1),
                    self.__get_filter_value(f.value2))
            case FilterBetweenOperator.not_between:
                return ~pl.col(self.__get_alias(f.key)).is_between(
                    self.__get_filter_value(f.value1),
                    self.__get_filter_value(f.value2))

    def visit_list(self, f: FilterList) -> any:
        match f.operator:
            case FilterListOperator.value_in:
                return pl.col(self.__get_alias(f.key)).is_in(list(map(lambda x: self.__get_filter_value(x, True, f.key), f.values)))
            case FilterListOperator.value_not_in:
                return ~pl.col(self.__get_alias(f.key)).is_in(list(map(lambda x: self.__get_filter_value(x, True, f.key), f.values)))

    def visit_group(self, f: FilterGroup) -> any:
        r = None

        for i in f.filters:
            x = i.visit(self)

            if r is None:
                r = x
                continue

            if f.operator == FilterGroupOperator.group_and:
                r = (r & x)
            else:
                r = (r | x)

        return r

    def visit_impossible(self, f: FilterImpossible) -> any:
        return False

    def __get_alias(self, key: str) -> str:
        return self.property_dict[key].alias

    def __get_filter_value(self, value, ignore_string=False, check_data_type_for_key: str = None):
        if isinstance(value, datetime):
            return value
        if not ignore_string and isinstance(value, str):
            return pl.lit(value)

        if check_data_type_for_key is not None:
            alias = self.__get_alias(check_data_type_for_key)
            data_type = self.df.collect_schema()[alias]
            return convert_value(value, data_type)

        return value
