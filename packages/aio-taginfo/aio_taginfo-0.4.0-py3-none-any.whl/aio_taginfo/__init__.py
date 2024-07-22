"""
Typed async client for the taginfo API.

## Modules
The `api` package structure is in large parts derived from the endpoint path segments:

* ``aio_taginfo.error``
* ``aio_taginfo.api.v4``
* ``aio_taginfo.api.v4.key.distribution.nodes``
* ``aio_taginfo.api.v4.key.distribution.ways``
* ``aio_taginfo.api.v4.key.chronology``
* ``aio_taginfo.api.v4.key.combinations``
* ``aio_taginfo.api.v4.key.overview``
* ``aio_taginfo.api.v4.key.prevalent_values``
* ``aio_taginfo.api.v4.key.projects``
* ``aio_taginfo.api.v4.key.similar``
* ``aio_taginfo.api.v4.key.stats``
* ``aio_taginfo.api.v4.key.values``
* ``aio_taginfo.api.v4.key.wiki_pages``
* ``aio_taginfo.api.v4.keys.all``
* ``aio_taginfo.api.v4.keys.similar``
* ``aio_taginfo.api.v4.keys.wiki_pages``
* ``aio_taginfo.api.v4.keys.without_wiki_page``
* ``aio_taginfo.api.v4.languages``
* ``aio_taginfo.api.v4.project.icon``
* ``aio_taginfo.api.v4.project.tags``
* ``aio_taginfo.api.v4.projects.all``
* ``aio_taginfo.api.v4.projects.keys``
* ``aio_taginfo.api.v4.projects.tags``
* ``aio_taginfo.api.v4.relation.projects``
* ``aio_taginfo.api.v4.relation.roles``
* ``aio_taginfo.api.v4.relation.stats``
* ``aio_taginfo.api.v4.relation.wiki_pages``
* ``aio_taginfo.api.v4.relations.all``
* ``aio_taginfo.api.v4.search.by_key_and_value``
* ``aio_taginfo.api.v4.search.by_keyword``
* ``aio_taginfo.api.v4.search.by_role``
* ``aio_taginfo.api.v4.search.by_value``
* ``aio_taginfo.api.v4.site.config.geodistribution``
* ``aio_taginfo.api.v4.site.info``
* ``aio_taginfo.api.v4.site.sources``
* ``aio_taginfo.api.v4.tag.chronology``
* ``aio_taginfo.api.v4.tag.distribution.nodes``
* ``aio_taginfo.api.v4.tag.distribution.ways``
* ``aio_taginfo.api.v4.tag.overview``
* ``aio_taginfo.api.v4.tag.projects``
* ``aio_taginfo.api.v4.tag.stats``
* ``aio_taginfo.api.v4.tag.wiki_pages``
* ``aio_taginfo.api.v4.tags.list``
* ``aio_taginfo.api.v4.tags.popular``
* ``aio_taginfo.api.v4.unicode.characters``
* ``aio_taginfo.api.v4.wiki.languages``
* ``aio_taginfo.api.v4.wikidata.all``
* ``aio_taginfo.api.v4.wikidata.errors``

## Call functions
All the calls are re-exported here at the top level for convenience:
"""

import importlib.metadata


__version__: str = importlib.metadata.version("aio-taginfo")

# we add this to all modules for pdoc;
# see https://pdoc.dev/docs/pdoc.html#use-numpydoc-or-google-docstrings
__docformat__ = "google"

# we also use __all__ in all modules for pdoc; this lets us control the order
__all__ = (
    "__version__",
    "TaginfoError",
    "api",  # pyright: ignore[reportUnsupportedDunderAll]
    "error",  # pyright: ignore[reportUnsupportedDunderAll]
    "key_chronology",
    "key_combinations",
    "key_distribution_nodes",
    "key_distribution_ways",
    "key_overview",
    "key_prevalent_values",
    "key_projects",
    "key_similar",
    "key_stats",
    "relation_projects",
    "site_config_geodistribution",
    "tag_projects",
    "tags_popular",
)

from aio_taginfo.api.v4.key.chronology import call as key_chronology
from aio_taginfo.api.v4.key.combinations import call as key_combinations
from aio_taginfo.api.v4.key.distribution.nodes import call as key_distribution_nodes
from aio_taginfo.api.v4.key.distribution.ways import call as key_distribution_ways
from aio_taginfo.api.v4.key.overview import call as key_overview
from aio_taginfo.api.v4.key.prevalent_values import call as key_prevalent_values
from aio_taginfo.api.v4.key.projects import call as key_projects
from aio_taginfo.api.v4.key.similar import call as key_similar
from aio_taginfo.api.v4.key.stats import call as key_stats
from aio_taginfo.api.v4.relation.projects import call as relation_projects
from aio_taginfo.api.v4.site.config.geodistribution import call as site_config_geodistribution
from aio_taginfo.api.v4.tag.projects import call as tag_projects
from aio_taginfo.api.v4.tags.popular import call as tags_popular
from aio_taginfo.error import TaginfoError
