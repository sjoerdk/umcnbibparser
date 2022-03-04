from io import StringIO
from unittest.mock import Mock

import pytest as pytest

from bibparser.bibreader import parse_bibtex_file
from bibparser.core import convert_and_write_to_handle
from bibparser.mysql import enrich_for_db, to_research_db_mysql
from tests import RESOURCE_PATH


@pytest.fixture
def a_parsed_bibfile():
    """A parsed bib file with 100 entries"""
    return parse_bibtex_file(
        filename=RESOURCE_PATH / "some_entries.bib",
        full_strings_bib=RESOURCE_PATH / "fullstrings.bib",
    )


@pytest.fixture
def a_parsed_ill_formed_bibfile():
    """Short bib file with one entry without type and one with"""
    return parse_bibtex_file(
        filename=RESOURCE_PATH / "an_entry_ill_formed.bib",
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

    enriched = enrich_for_db(a_parsed_bibfile)
    for item in enriched.values():
        assert "genericentrytype" in item


def test_mysql_enrich_errors(a_parsed_ill_formed_bibfile):
    """Recreates error in issue #1"""
    # Extract only the first dict item for
    assert len(a_parsed_ill_formed_bibfile) == 2
    with pytest.warns(UserWarning, match='.*Skipping bib item.*'):
        enriched = enrich_for_db(a_parsed_ill_formed_bibfile)

    assert len(enriched) == 1


def test_to_mysql_db_file(a_parsed_bibfile):
    """Render a bibfile to a mysql file that creates the bibfiles content"""
    mysql = to_research_db_mysql(enrich_for_db(a_parsed_bibfile))

    assert mysql.count("INSERT") == 100  # one insert for each item
    assert mysql.count("{{") == 0  # no jinja tags unreplaced


def test_core_convert():
    file = StringIO()
    convert_and_write_to_handle(bibfile_path=RESOURCE_PATH / "some_entries.bib",
                                bibstrings_path=RESOURCE_PATH / "fullstrings.bib",
                                handle=file)
    file.seek(0)
    contents = file.read()



