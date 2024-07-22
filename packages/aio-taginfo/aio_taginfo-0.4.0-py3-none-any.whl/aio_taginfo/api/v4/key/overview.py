"""`/api/4/key/overview` endpoint."""

from aio_taginfo.api.v4 import ObjectType, PrintingDirection, Response
from aio_taginfo.api.v4._internal import NonEmptyString, api_get_json, api_params

from aiohttp import ClientSession
from pydantic import Field
from pydantic.dataclasses import dataclass


__all__ = (
    "call",
    "KeyOverview",
    "KeyDescription",
    "KeyObjectCount",
    "KeyWikiPage",
)

from aio_taginfo.api.v4.key.prevalent_values import PrevalentValue


@dataclass(kw_only=True, frozen=True)
class _Params:
    key: NonEmptyString = Field(repr=True)


async def call(
    key: str,
    session: ClientSession | None = None,
) -> Response["KeyOverview"]:
    """
    Show various data for given key.

    https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_key_overview

    Args:
        key: tag key
        session: request client session

    Raises:
        TaginfoError
    """
    return await api_get_json(
        path="key/overview",
        cls=Response[KeyOverview],
        session=session,
        params=api_params(_Params, key=key),
    )


@dataclass(kw_only=True, frozen=True)
class KeyObjectCount:
    """
    Usage statistic of a given key for a given type of object.

    Attributes:
        type: Object type
        count: Number of objects with this type and key
        count_fraction: Number of objects in relation to all objects
        values: Number of different values for this key
    """

    type: ObjectType = Field(repr=True)
    count: int = Field(ge=0, repr=True)
    count_fraction: float = Field(ge=0.0, le=1.0, allow_inf_nan=False, repr=True)
    values: int = Field(ge=0, repr=True)


@dataclass(kw_only=True, frozen=True)
class KeyDescription:
    """
    Description of a given key in some language.

    Attributes:
        text: Description text
        dir: Printing direction for this language
    """

    text: str = Field(min_length=1, repr=True)
    dir: PrintingDirection = Field(repr=False)


@dataclass(kw_only=True, frozen=True)
class KeyWikiPage:
    """
    Language code for which a wiki page about a given key are available.

    Attributes:
        lang: Language code
        english: English name of this language
        native: Native name of this language
        dir: Printing direction for native name
    """

    lang: str = Field(min_length=2, repr=True)
    english: str = Field(min_length=1, repr=True)
    native: str = Field(min_length=1, repr=True)
    dir: PrintingDirection = Field(repr=False)


@dataclass(kw_only=True, frozen=True)
class KeyOverview:
    """
    Various data for a given key.

    Attributes:
        key: The tag key that was requested
        users: Number of users last editing objects with this key
        prevalent_values: Prevalent values ordered by count from most often used down
        counts: Objects counts
        description: Description of this key (hash key is language code)
        wiki_pages: Language codes for which wiki pages about this key are available
        has_map: Is a map with the geographical distribution of this key available?
        projects: Number of projects mentioning this key
    """

    key: str = Field(min_length=1, repr=True)
    prevalent_values: list[PrevalentValue] = Field(repr=False)
    counts: list[KeyObjectCount] = Field(repr=False)
    description: dict[str, KeyDescription] = Field(repr=False)
    wiki_pages: list[KeyWikiPage] = Field(repr=False)
    has_map: bool = Field(repr=False)
    users: int = Field(default=0, ge=0, repr=True)
    projects: int = Field(default=0, ge=0, repr=False)


__docformat__ = "google"
