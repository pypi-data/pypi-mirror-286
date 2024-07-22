import urllib.parse
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Annotated, Any, TypeAlias, TypeVar

from aio_taginfo import __version__
from aio_taginfo.api.v4 import PngResponse
from aio_taginfo.error import TaginfoCallError, TaginfoValidationError, TaginfoValueError

import aiohttp
import pydantic
from aiohttp import ClientResponse, ClientSession
from pydantic import BeforeValidator, HttpUrl, StringConstraints, TypeAdapter


__all__ = (
    "NonEmptyString",
    "OptionalNonEmptyString",
    "api_params",
    "api_get_json",
    "api_get_png",
)


_URL_BASE = "https://taginfo.openstreetmap.org/api/4/"
_DEFAULT_USER_AGENT = f"aio-taginfo/{__version__} (https://github.com/timwie/aio-taginfo)"

T = TypeVar("T", bound=Any)

NonEmptyString = Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]


def _empty_str_to_none(v: str | None) -> str | None:
    if isinstance(v, str):
        return None if v.strip() == "" else v.strip()
    return v


# TODO: move somewhere public?
OptionalNonEmptyString: TypeAlias = Annotated[
    str | None,
    BeforeValidator(_empty_str_to_none),
]

# TODO: move somewhere public?
OptionalHttpUrl: TypeAlias = Annotated[
    HttpUrl | None,
    BeforeValidator(_empty_str_to_none),
]


def api_params(datacls: type[T], **kwargs: Any) -> dict:  # noqa: ANN401
    """
    Use a dataclass to validate parameters, and return them as a dict.

    Args:
        datacls: the pydantic dataclass used to validate parameters
        **kwargs: values for all fields of that dataclass

    Raises:
        TaginfoValueError

    Returns:
        ``kwargs`` with some changes, like mapping enum instances to their underlying values,
        and removing ``None`` values
    """
    try:
        # TODO: log "validating params…"
        validated = datacls(**kwargs)
        return _params_to_dict(validated)
    except pydantic.ValidationError as err:
        raise TaginfoValueError(cause=err) from err


def _params_to_dict(obj: Any) -> dict:  # noqa: ANN401
    assert is_dataclass(type(obj))

    ok = (str, int, float, bool)

    def map_value(v):  # noqa: ANN001, ANN202
        if isinstance(v, Enum):
            assert isinstance(v.value, ok)
            return v.value

        assert isinstance(v, ok)
        return v

    return {k: map_value(v) for k, v in asdict(obj).items() if v is not None}


async def api_get_json(
    path: str,
    cls: type[T],
    session: ClientSession | None = None,
    params: dict | None = None,
) -> T:
    """
    Make a GET request to the taginfo API v4, and map to the given type.

    Args:
        path: the API path after "/api/4/"
        cls: the pydantic dataclass to map to
        session: request client session
        params: parameters in the request query string

    Raises:
        TaginfoError

    Returns:
        an instance of ``cls``
    """
    type_adapter = TypeAdapter(cls)

    async with _get(
        path=path,
        session=session,
        params=params,
        content_type="application/json",
        headers=None,
    ) as response:
        payload = await response.read()
        # TODO: log "validating response…"
        return type_adapter.validate_json(payload, strict=True)
        # TODO: log "validated."


async def api_get_png(
    path: str,
    session: ClientSession | None = None,
    params: dict | None = None,
) -> "PngResponse":
    """
    Request a PNG image from the taginfo API v4.

    Args:
        path: the API path after "/api/4/"
        session: request client session
        params: parameters in the request query string

    Raises:
        TaginfoError
    """
    async with _get(
        path=path,
        params=params,
        session=session,
        content_type="image/png",
        headers=None,
    ) as response:
        payload = await response.read()
        # TODO: log "validating response…"
        return PngResponse(data=payload)
        # TODO: log "validated."


@asynccontextmanager
async def _get(
    path: str,
    content_type: str,
    session: ClientSession | None,
    params: dict | None,
    headers: dict | None,
) -> AsyncIterator[ClientResponse]:
    url = urllib.parse.urljoin(_URL_BASE, path)
    assert url.startswith(_URL_BASE), "given 'path' cannot start with a '/'"

    ephemeral_session = not session
    session = session or ClientSession()
    params = params or {}
    headers = headers or {}

    if "User-Agent" not in session.headers and "User-Agent" not in headers:
        headers["User-Agent"] = _DEFAULT_USER_AGENT

    headers["Accept"] = content_type

    # TODO: log "path"
    # TODO: log "params"
    # TODO: log "url"

    try:
        async with session.get(
            url,
            params=params,
            headers=headers,
            raise_for_status=True,
        ) as response:
            yield response
    except aiohttp.ClientError as err:
        raise TaginfoCallError(cause=err) from err
    except pydantic.ValidationError as err:
        raise TaginfoValidationError(cause=err) from err
    finally:
        if ephemeral_session:
            await session.close()


__docformat__ = "google"
