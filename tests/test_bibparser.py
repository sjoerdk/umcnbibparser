import pytest as pytest

from bibparser.bibreader import parse_bibtex_file
from bibparser.mysql import enrich_parsed, to_research_db_mysql
from tests import RESOURCE_PATH


@pytest.fixture
def a_parsed_bibfile():
    """A parsed bib file with 100 entries"""
    return parse_bibtex_file(
        filename=RESOURCE_PATH / "some_entries.bib",
        full_strings_bib=RESOURCE_PATH / "fullstrings.bib",
    )


def test_parse_bib():
    """Test basic usage. Just check for no exceptions here"""
    bib_items = parse_bibtex_file(
        filename=RESOURCE_PATH / "some_entries.bib",
        full_strings_bib=RESOURCE_PATH / "fullstrings.bib",
    )

    assert len(bib_items) == 100


def test_mysql_enrich(a_parsed_bibfile):
    for item in a_parsed_bibfile.values():
        assert "genericentrytype" not in item

    enriched = enrich_parsed(a_parsed_bibfile)
    for item in enriched.values():
        assert "genericentrytype" in item


def test_to_mysql_db_file(a_parsed_bibfile):
    """Render a bibfile to a mysql file that creates the bibfiles content"""
    mysql = to_research_db_mysql(enrich_parsed(a_parsed_bibfile))

    assert mysql.count("INSERT") == 100  # one insert for each item
    assert mysql.count("{{") == 0  # no jinja tags unreplaced
