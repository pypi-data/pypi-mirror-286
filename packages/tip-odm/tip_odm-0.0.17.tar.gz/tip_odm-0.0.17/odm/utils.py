import time
import uuid
import hashlib
import asyncio
from typing import Callable
from .logger import log_info


def create_uuid_from_string(val: str):
    """
    Konvertiert einen Text in eine reproduzierbare Guid
    :param val: Text
    :return: Guid als Text
    """

    hex_string = hashlib.md5(val.encode("UTF-8")).hexdigest()
    return str(uuid.UUID(hex=hex_string))


async def timer(text: str, func: Callable):
    start = time.time()
    result = func()

    if asyncio.iscoroutine(result):
        result = await result

    end = time.time()
    diff = round((end - start) * 1000, 0)

    log_info(f"{text}: {diff}ms")
    return result
