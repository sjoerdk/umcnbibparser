"""Functions to write bibfile contents to MYSQL file.

Notes
-----
Functions here are not meant to be generic. Mysql db format is specific to the
radboud research websites db
"""
from typing import Dict

from jinja2.environment import Environment
from jinja2.loaders import PackageLoader

GENERIC_ENTRY_TYPES = {
    "article": "1_Article",
    "inproceedings": "2_Inproceedings",
    "abstract": "3_Abstract",
    "phdthesis": "4_PHDThesis",
    "book": "",
    "incollection": "",
}


def enrich_parsed(parsed_bib: Dict) -> Dict:
    """Add legacy items to each bib entry needed in db for historical reasons

    Notes
    -----
    Modifies input dict
    """
    for key in parsed_bib.keys():
        try:
            parsed_bib[key]["genericentrytype"] = GENERIC_ENTRY_TYPES[
                parsed_bib[key]["type"].lower()
            ]
        except KeyError as e:
            raise (KeyError(f"Error in bib entry '{key}'")) from e

    return parsed_bib


def to_research_db_mysql(enriched_bib) -> str:
    """Render parsed and enriched bib file to a mysql command that will create
    the research db research from scratch
    """

    loader = PackageLoader(package_name="bibparser", package_path="templates")
    template_env = Environment(loader=loader, autoescape=True)
    template = template_env.get_template("newpubs.sql.j2")
    return template.render(entries=enriched_bib)
