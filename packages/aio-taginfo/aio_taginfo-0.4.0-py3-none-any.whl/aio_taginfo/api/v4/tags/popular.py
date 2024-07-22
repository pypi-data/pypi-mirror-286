"""`/api/4/tags/popular` endpoint."""

from enum import Enum
from typing import Any

from aio_taginfo.api.v4 import Response, SortOrder

from aiohttp import ClientSession
from pydantic import Field, field_validator
from pydantic.dataclasses import dataclass


__all__ = (
    "call",
    "PopularTag",
    "PopularTagSorting",
)

from aio_taginfo.api.v4._internal import NonEmptyString, api_get_json, api_params


@dataclass(kw_only=True, frozen=True)
class PopularTag:
    """
    A tag and its usage statistics.

    Attributes:
        key: Tag key name, the left side of the ``key=value`` pair
        value: Tag value, the right side of the ``key=value`` pair
        in_wiki: ``True`` if there is at least one wiki page for this tag
        count_all: Number of objects in the OSM database with this tag
        count_all_fraction: Number of objects with this tag as percentage of all objects
        count_nodes: Number of nodes in the OSM database with this tag
        count_nodes_fraction: Number of nodes with this tag as percentage of all tagged nodes
        count_ways: Number of ways in the OSM database with this tag
        count_ways_fraction: Number of ways with this tag as percentage of all ways
        count_relations: Number of relations in the OSM database with this tag
        count_relations_fraction: Number of relations with this tag as percentage of all relations
        projects: Number of projects using this tag
    """

    key: str = Field(min_length=1, repr=True)
    value: str = Field(min_length=1, repr=True)
    in_wiki: bool = Field(repr=True)
    count_all: int = Field(ge=0, repr=True)
    count_all_fraction: float = Field(ge=0.0, le=1.0, allow_inf_nan=False, repr=False)
    count_nodes: int = Field(ge=0, repr=True)
    count_nodes_fraction: float = Field(ge=0.0, le=1.0, allow_inf_nan=False, repr=False)
    count_ways: int = Field(ge=0, repr=True)
    count_ways_fraction: float = Field(ge=0.0, le=1.0, allow_inf_nan=False, repr=False)
    count_relations: int = Field(ge=0, repr=True)
    count_relations_fraction: float = Field(ge=0.0, le=1.0, allow_inf_nan=False, repr=False)
    projects: int = Field(default=0, ge=0, repr=False)

    # expected "in_wiki: bool = Field(strict=False, …)" to also work,
    # but it does not override strict mode
    @field_validator("in_wiki", mode="before")
    def _convert_in_wiki(cls, input_value: Any) -> bool:  # noqa: ANN401, N805
        if input_value == 0:
            return False
        if input_value == 1:
            return True
        return input_value


class PopularTagSorting(str, Enum):
    """Sort options for popular tags."""

    TAG = "tag"
    COUNT_ALL = "count_all"
    COUNT_NODES = "count_nodes"
    COUNT_WAYS = "count_ways"
    COUNT_RELATIONS = "count_relations"


@dataclass(kw_only=True, frozen=True)
class _Params:
    query: NonEmptyString | None = Field(repr=True)
    sortname: PopularTagSorting = Field(repr=True)
    sortorder: SortOrder = Field(repr=True)
    page: int = Field(gt=0, repr=True)
    rp: int = Field(ge=0, repr=True)


async def call(
    query: str | None = None,
    sortname: PopularTagSorting = PopularTagSorting.COUNT_ALL,
    sortorder: SortOrder = SortOrder.DESC,
    page: int = 1,
    rp: int = 0,
    session: ClientSession | None = None,
) -> Response[list[PopularTag]]:
    """
    Get list of most often used tags.

    https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_tags_popular

    Args:
        query: only show results where ``key`` or ``value`` matches this query (substring match)
        sortname: what field to sort by
        sortorder: sort order
        page: page number (starting at 1)
        rp: results per page
        session: request client session

    Raises:
        TaginfoError
    """
    params = api_params(
        _Params, query=query, sortname=sortname, sortorder=sortorder, page=page, rp=rp
    )
    return await api_get_json(
        path="tags/popular",
        cls=Response[list[PopularTag]],
        session=session,
        params=params,
    )


__docformat__ = "google"
