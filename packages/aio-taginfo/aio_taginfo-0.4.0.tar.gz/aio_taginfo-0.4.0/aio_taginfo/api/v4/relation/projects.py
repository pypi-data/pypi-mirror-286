"""`/api/4/relation/projects` endpoint."""

from enum import Enum

from aio_taginfo.api.v4 import Response, SortOrder
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
    "RelationProject",
    "RelationProjectSorting",
)


@dataclass(kw_only=True, frozen=True)
class RelationProject:
    """
    TODO: https://wiki.openstreetmap.org/wiki/Taginfo/Projects.

    Attributes:
        project_id: Project ID
        project_name: Project name
        project_icon_url: Project icon URL
        rtype: Relation type
        description: Description
        doc_url: Documentation URL
        icon_url: Icon URL
    """

    project_id: str = Field(min_length=1, repr=True)
    project_name: str = Field(min_length=1, repr=True)
    project_icon_url: OptionalHttpUrl = Field(repr=False)
    rtype: str = Field(min_length=1, repr=True)
    description: OptionalNonEmptyString = Field(repr=False)
    doc_url: OptionalHttpUrl = Field(repr=False)
    icon_url: OptionalHttpUrl = Field(repr=False)


class RelationProjectSorting(str, Enum):
    """Sort options for relation projects."""

    PROJECT_NAME = "project_name"


@dataclass(kw_only=True, frozen=True)
class _Params:
    rtype: NonEmptyString = Field(repr=True)
    query: NonEmptyString | None = Field(repr=True)
    sortname: RelationProjectSorting = Field(repr=True)
    sortorder: SortOrder = Field(repr=True)
    page: int = Field(gt=0, repr=True)
    rp: int = Field(ge=0, repr=True)


async def call(
    rtype: str,
    query: str | None = None,
    sortname: RelationProjectSorting = RelationProjectSorting.PROJECT_NAME,
    sortorder: SortOrder = SortOrder.ASC,
    page: int = 1,
    rp: int = 0,
    session: ClientSession | None = None,
) -> Response[list[RelationProject]]:
    """
    Get projects using a given relation type.

    https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_relation_projects

    Args:
        rtype: Relation type
        query: Only show results where the value matches this query (substring match)
        sortname: what field to sort by
        sortorder: sort order
        page: page number (starting at 1)
        rp: results per page
        session: request client session

    Raises:
        TaginfoError
    """
    params = api_params(
        _Params,
        rtype=rtype,
        query=query,
        sortname=sortname,
        sortorder=sortorder,
        page=page,
        rp=rp,
    )
    return await api_get_json(
        path="relation/projects",
        cls=Response[list[RelationProject]],
        session=session,
        params=params,
    )


__docformat__ = "google"
