"""`/api/4/key/combinations` endpoint."""

from enum import Enum

from aio_taginfo.api.v4 import ObjectType, Response, SortOrder
from aio_taginfo.api.v4._internal import NonEmptyString, api_get_json, api_params

from aiohttp import ClientSession
from pydantic import Field
from pydantic.dataclasses import dataclass


__all__ = (
    "call",
    "KeyCombination",
    "KeyCombinationSorting",
)


@dataclass(kw_only=True, frozen=True)
class KeyCombination:
    """
    Combination statistics for a given key with another.

    Attributes:
        other_key: Other key.
        together_count: Number of objects that have both keys.
        to_fraction: Fraction of objects with this key that also have the other key.
        from_fraction: Fraction of objects with other key that also have this key.
    """

    other_key: str = Field(min_length=1, repr=True)
    together_count: int = Field(ge=0, repr=True)
    to_fraction: float = Field(ge=0.0, le=1.0, allow_inf_nan=False, repr=True)
    from_fraction: float = Field(ge=0.0, le=1.0, allow_inf_nan=False, repr=True)


class KeyCombinationSorting(str, Enum):
    """Sort options for key combination."""

    TOGETHER_COUNT = "together_count"
    OTHER_KEY = "other_key"
    FROM_FRACTION = "from_fraction"


@dataclass(kw_only=True, frozen=True)
class _Params:
    key: NonEmptyString = Field(repr=True)
    query: NonEmptyString | None = Field(repr=True)
    sortname: KeyCombinationSorting = Field(repr=True)
    sortorder: SortOrder = Field(repr=True)
    filter: ObjectType = Field(repr=True)
    page: int = Field(gt=0, repr=True)
    rp: int = Field(ge=0, repr=True)


async def call(
    key: str,
    query: str | None = None,
    sortname: KeyCombinationSorting = KeyCombinationSorting.TOGETHER_COUNT,
    sortorder: SortOrder = SortOrder.DESC,
    filter: ObjectType = ObjectType.ALL,  # noqa: A002
    page: int = 1,
    rp: int = 0,
    session: ClientSession | None = None,
) -> Response[list[KeyCombination]]:
    """
    Find keys that are used together with a given key.

    https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_key_combinations

    Args:
        key: tag key
        query: only show results where the ``other_key`` matches this query (substring match)
        sortname: what field to sort by
        sortorder: sort order
        filter: can be used to filter only values on tags used on nodes/ways/relations
        page: page number (starting at 1)
        rp: results per page
        session: request client session

    Raises:
        TaginfoError
    """
    params = api_params(
        _Params,
        key=key,
        query=query,
        sortname=sortname,
        sortorder=sortorder,
        filter=filter,
        page=page,
        rp=rp,
    )
    return await api_get_json(
        path="key/combinations",
        cls=Response[list[KeyCombination]],
        session=session,
        params=params,
    )


__docformat__ = "google"
