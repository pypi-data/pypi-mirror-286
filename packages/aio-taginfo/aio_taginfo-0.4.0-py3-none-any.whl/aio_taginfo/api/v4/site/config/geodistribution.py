"""`/api/4/site/geodistribution` endpoint."""

from aio_taginfo.api.v4._internal import api_get_json

from aiohttp import ClientSession
from pydantic import Field
from pydantic.dataclasses import dataclass


__all__ = (
    "call",
    "SiteConfigGeodistribution",
)


async def call(session: ClientSession | None = None) -> "SiteConfigGeodistribution":
    """
    Get information about the background map for distribution charts.

    https://taginfo.openstreetmap.org/taginfo/apidoc#api_4_site_config_geodistribution

    Args:
        session: request client session

    Raises:
        TaginfoError
    """
    return await api_get_json(
        path="/api/4/site/config/geodistribution",
        cls=SiteConfigGeodistribution,
        session=session,
    )


@dataclass(kw_only=True, frozen=True)
class SiteConfigGeodistribution:
    """
    Information about the background map for distribution charts.

    Attributes:
        width: width of background image
        height: height of background image
        scale_image: scale factor for images
        scale_compare_image: scale factor for comparison images
        background_image: URL of background image
        image_attribution: map attribution for comparison background
    """

    width: int = Field(gt=0, repr=True)
    height: int = Field(gt=0, repr=True)
    scale_image: float = Field(gt=0.0, allow_inf_nan=False, repr=True)
    scale_compare_image: float = Field(gt=0.0, allow_inf_nan=False, repr=True)
    background_image: str = Field(repr=True)
    image_attribution: str = Field(repr=True)


__docformat__ = "google"
