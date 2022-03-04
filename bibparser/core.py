from bibparser.bibreader import parse_bibtex_file
from bibparser.mysql import enrich_for_db, to_research_db_mysql


def convert(bibfile_path, bibstrings_path, output_path):
    print(f"Parsing {bibfile_path}")
    print(f"Using journal strings from  {bibstrings_path}")
    with open(output_path, 'w') as handle:
        convert_and_write_to_handle(bibfile_path, bibstrings_path, handle)
    print(f"Done. Written to {output_path}")


def convert_and_write_to_handle(bibfile_path, bibstrings_path, handle):
    parsed = parse_bibtex_file(filename=bibfile_path,
                               full_strings_bib=bibstrings_path)
    print(f"Parsed {len(parsed)} bib entries from {bibfile_path}")
    enriched = enrich_for_db(parsed)
    print(f"Using {len(enriched)}, skipped {len(parsed) - len(enriched)}")
    handle.write(to_research_db_mysql(enriched))
