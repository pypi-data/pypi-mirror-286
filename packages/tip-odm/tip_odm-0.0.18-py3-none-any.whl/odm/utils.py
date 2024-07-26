import time
import uuid
import hashlib
import asyncio
import polars as pl
from typing import ForwardRef
from typing import Callable
from .enums import DataType
from .logger import log_info

type Definition = ForwardRef("odm_models_query.Definition")


def create_uuid_from_string(val: str):
    """
    Konvertiert einen Text in eine reproduzierbare Guid
    :param val: Text
    :return: Guid als Text
    """

    hex_string = hashlib.md5(val.encode("UTF-8")).hexdigest()
    return str(uuid.UUID(hex=hex_string))


def fix_data_types(d: Definition, df: pl.DataFrame | pl.LazyFrame):
    """
    Passt die Daten-Typen an
    :param d: Definition
    :param df: DataFrame
    """

    for prop in d.properties:
        data_type = __get_data_type(prop.type)
        if data_type is None:
            continue

        df = df.with_columns(pl.col(prop.alias).cast(data_type).alias(prop.alias))

    return df


async def timer(text: str, func: Callable):
    start = time.time()
    result = func()

    if asyncio.iscoroutine(result):
        result = await result

    end = time.time()
    diff = round((end - start) * 1000, 0)

    log_info(f"{text}: {diff}ms")
    return result


def __get_data_type(data_type: DataType):
    match data_type:
        case DataType.int:
            return pl.Int32
        case DataType.decimal:
            return pl.Float32
        case _:
            return None
