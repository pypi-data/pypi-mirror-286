"""Error types."""

from dataclasses import dataclass

import aiohttp
import pydantic


class TaginfoError(Exception):
    """Base class for taginfo API errors."""


@dataclass(kw_only=True, frozen=True)
class TaginfoValueError(Exception):
    """Failed to validate given parameters; did not call the taginfo API."""

    cause: pydantic.ValidationError


@dataclass(kw_only=True, frozen=True)
class TaginfoCallError(Exception):
    """Failed HTTP call to the taginfo API."""

    cause: aiohttp.ClientError


@dataclass(kw_only=True, frozen=True)
class TaginfoValidationError(Exception):
    """
    Failed to validate the response of the taginfo API.

    This should usually indicate a bug in this library.
    """

    cause: pydantic.ValidationError


__docformat__ = "google"
