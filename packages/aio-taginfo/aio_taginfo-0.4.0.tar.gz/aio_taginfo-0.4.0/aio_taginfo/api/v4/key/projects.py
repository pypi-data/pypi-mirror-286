"""`/api/4/key/projects` endpoint."""

from enum import Enum

from aio_taginfo.api.v4 import ObjectType, Response, SortOrder
from aio_taginfo.api.v4._internal import (
    NonEmptyString,
    OptionalHttpUrl,
    OptionalNonEmptyString,
    api_get_json,
    api_params,
)

from aiohttp import ClientSession
from pydantic import Field
from pydantic.dataclasses import dataclass


__all__ = (
    "call",
    "KeyProject",
    "KeyProjectSorting",
)


@dataclass(kw_only=True, frozen=True)
class KeyProject:
    """
    TODO: https://wiki.openstreetmap.org/wiki/Taginfo/Projects.

    Attributes:
        project_id: Project ID
        project_name: Project name
        project_icon_url: Project icon URL
        key: Key
        value: Value
        on_node: For nodes?
        on_way: For ways?
        on_relation: For relations?
        on_relation: For areas?
        description: Description
        doc_url: Documentation URL
        icon_url: Icon URL
    """

    project_id: str = Field(min_length=1, repr=True)
    project_name: str = Field(min_length=1, repr=True)
    project_icon_url: OptionalHttpUrl = Field(repr=False)
    key: str = Field(min_length=1, repr=True)
    value: OptionalNonEmptyString = Field(repr=True)
    on_node: bool = Field(repr=False)
    on_way: bool = Field(repr=False)
    on_relation: bool = Field(repr=False)
    on_area: bool = Field(repr=False)
    description: OptionalNonEmptyString = Field(repr=False)
    doc_url: OptionalHttpUrl = Field(repr=False)
    icon_url: OptionalHttpUrl = Field(repr=False)


class KeyProjectSorting(str, Enum):
    """Sort options for key projects."""

    PROJECT_NAME = "project_name"
    TAG = "tag"


@dataclass(kw_only=True, frozen=True)
class _Params:
    key: NonEmptyString = Field(repr=True)
    query: NonEmptyString | None = Field(repr=True)
    sortname: KeyProjectSorting = Field(repr=True)
    sortorder: SortOrder = Field(repr=True)
    filter: ObjectType = Field(repr=True)
    page: int = Field(gt=0, repr=True)
    rp: int = Field(ge=0, repr=True)


async def call(
    key: str,
    query: str | None = None,
    sortname: KeyProjectSorting = KeyProjectSorting.PROJECT_NAME,
    sortorder: SortOrder = SortOrder.ASC,
    filter: ObjectType = ObjectType.ALL,  # noqa: A002
    page: int = 1,
    rp: int = 0,
    session: ClientSession | None = None,
) -> Response[list[KeyProject]]:
    """
    Get projects using a given key.

    https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_key_projects

    Args:
        key: tag key
        query: only show results where the project name or tag value matches this query
               (substring match)
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
        path="key/projects",
        cls=Response[list[KeyProject]],
        session=session,
        params=params,
    )


__docformat__ = "google"
