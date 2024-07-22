"""`/api/4/tag/projects` endpoint."""

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
    "TagProject",
    "TagProjectSorting",
)


@dataclass(kw_only=True, frozen=True)
class TagProject:
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
    value: str | None = Field(min_length=1, repr=True)  # TODO: surprised this can be None
    on_node: bool = Field(repr=False)
    on_way: bool = Field(repr=False)
    on_relation: bool = Field(repr=False)
    on_area: bool = Field(repr=False)
    description: OptionalNonEmptyString = Field(repr=False)
    doc_url: OptionalHttpUrl = Field(repr=False)
    icon_url: OptionalHttpUrl = Field(repr=False)


class TagProjectSorting(str, Enum):
    """Sort options for tag projects."""

    PROJECT_NAME = "project_name"
    TAG = "tag"


@dataclass(kw_only=True, frozen=True)
class _Params:
    key: NonEmptyString = Field(repr=True)
    value: NonEmptyString = Field(repr=True)
    query: NonEmptyString | None = Field(repr=True)
    sortname: TagProjectSorting = Field(repr=True)
    sortorder: SortOrder = Field(repr=True)
    filter: ObjectType = Field(repr=True)
    page: int = Field(gt=0, repr=True)
    rp: int = Field(ge=0, repr=True)


async def call(
    key: str,
    value: str,
    query: str | None = None,
    sortname: TagProjectSorting = TagProjectSorting.PROJECT_NAME,
    sortorder: SortOrder = SortOrder.ASC,
    filter: ObjectType = ObjectType.ALL,  # noqa: A002
    page: int = 1,
    rp: int = 0,
    session: ClientSession | None = None,
) -> Response[list[TagProject]]:
    """
    Get projects using a given tag.

    https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_tag_projects

    Args:
        key: tag key
        value: tag value
        query: Only show results where the project name matches this query (substring match)
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
        value=value,
        query=query,
        sortname=sortname,
        sortorder=sortorder,
        filter=filter,
        page=page,
        rp=rp,
    )
    return await api_get_json(
        path="tag/projects",
        cls=Response[list[TagProject]],
        session=session,
        params=params,
    )


__docformat__ = "google"
