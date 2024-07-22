"""`/api/4/key/chronology` endpoint."""

import datetime

from aio_taginfo.api.v4 import Response
from aio_taginfo.api.v4._internal import NonEmptyString, api_get_json, api_params

from aiohttp import ClientSession
from pydantic import Field
from pydantic.dataclasses import dataclass


__all__ = (
    "call",
    "KeyChronology",
)


@dataclass(kw_only=True, frozen=True)
class _Params:
    key: NonEmptyString = Field(repr=True)


@dataclass(kw_only=True, frozen=True)
class KeyChronology:
    """
    Chronology of key counts relative to a previous entry.

    Attributes:
        date: Date of key counts
        nodes: Difference in number of nodes with this key, relative to the previous entry
        ways: Difference in number of ways with this key, relative to the previous entry
        relations: Difference in number of relations with this key, relative to the previous entry
    """

    date: datetime.date = Field(repr=True)
    nodes: int = Field(repr=True)
    ways: int = Field(repr=True)
    relations: int = Field(repr=True)


async def call(
    key: str,
    session: ClientSession | None = None,
) -> Response[list[KeyChronology]]:
    """
    Get chronology of key counts.

    https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_key_chronology

    Args:
        key: tag key
        session: request client session

    Raises:
        TaginfoError
    """
    return await api_get_json(
        path="key/chronology",
        cls=Response[list[KeyChronology]],
        session=session,
        params=api_params(_Params, key=key),
    )


__docformat__ = "google"
