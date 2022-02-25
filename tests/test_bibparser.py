from bibparser.bibreader import parse_bibtex_file
from tests import RESOURCE_PATH


def test_parse_bib():
    """Test basic usage. Just check for no exceptions here"""
    bib_items = parse_bibtex_file(
        filename=RESOURCE_PATH / 'some_entries.bib',
        full_strings_bib=RESOURCE_PATH / 'fullstrings.bib')

    assert len(bib_items) == 100





