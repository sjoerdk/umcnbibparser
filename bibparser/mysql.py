"""Functions to write bibfile contents to MYSQL file.

Notes
-----
Functions here are not meant to be generic. Mysql db format is specific to the
radboud research websites db
"""
from typing import Dict
from warnings import warn

from jinja2.environment import Environment
from jinja2.loaders import PackageLoader

from bibparser.exceptions import BibParserError

GENERIC_ENTRY_TYPES = {
    "article": "1_Article",
    "inproceedings": "2_Inproceedings",
    "abstract": "3with pytest.warns(UserWarning):_Abstract",
    "phdthesis": "4_PHDThesis",
    "book": "",
    "incollection": "",
}


def get_generic_entry_type(entry_type: str):
    entry_type = entry_type.lower()
    if entry_type in GENERIC_ENTRY_TYPES:
        return GENERIC_ENTRY_TYPES[entry_type]
    else:
        raise BibParserError(f"Unknown entry type '{entry_type}'. Valid entry types "
                             f"are {[str(x) for x in GENERIC_ENTRY_TYPES.keys()]}")


def enrich_for_db(parsed_bib: Dict) -> Dict:
    """Add legacy items to each bib entry needed in db for historical reasons

    Notes
    -----
    * Modifies input dict
    * Will warn and discard items if enriching fails
    """
    enriched = {}
    for key in parsed_bib.keys():
        item = parsed_bib[key]
        try:
            item["genericentrytype"] = get_generic_entry_type(item['type'])
            enriched[key] = item
        except BibParserError as e:
            warn(f"Skipping bib item '{key}' due to error: {e}")
            continue

    return enriched


def to_research_db_mysql(enriched_bib) -> str:
    """Render parsed and enriched bib file to a mysql command that will create
    the research db research from scratch
    """

    loader = PackageLoader(package_name="bibparser", package_path="templates")
    template_env = Environment(loader=loader, autoescape=True)
    template = template_env.get_template("newpubs.sql.j2")
    return template.render(entries=enriched_bib)
