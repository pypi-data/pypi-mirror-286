"""`/api/4/key/stats` endpoint."""

from aio_taginfo.api.v4 import ObjectType, Response
from aio_taginfo.api.v4._internal import NonEmptyString, api_get_json, api_params

from aiohttp import ClientSession
from pydantic import Field
from pydantic.dataclasses import dataclass


__all__ = (
    "KeyStats",
    "call",
)


@dataclass(kw_only=True, frozen=True)
class KeyStats:
    """
    Database statistics for given key.

    Attributes:
        type: Object type.
        count: Number of objects with this type and key.
        count_fraction: Number of objects in relation to all objects.
        values: Number of different values for this key.
    """

    type: ObjectType = Field(repr=True)
    count: int = Field(ge=0, repr=True)
    count_fraction: float = Field(ge=0.0, le=1.0, allow_inf_nan=False, repr=True)
    values: int = Field(ge=0, repr=True)


@dataclass(kw_only=True, frozen=True)
class _Params:
    key: NonEmptyString = Field(repr=True)


async def call(
    key: str,
    session: ClientSession | None = None,
) -> Response[list[KeyStats]]:
    """
    Show some database statistics for given key.

    https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_key_stats

    Args:
        key: tag key
        session: request client session

    Raises:
        TaginfoError
    """
    return await api_get_json(
        path="key/stats",
        cls=Response[list[KeyStats]],
        session=session,
        params=api_params(_Params, key=key),
    )


__docformat__ = "google"
