"""Convert radiology.bib, use journal titles from fullstrings.bib.
Write sql file to newpubs.sql

"""
from bibparser.core import convert

if __name__ == "__main__":
    convert(bibfile_path="radiology.bib",
            bibstrings_path="fullstrings.bib",
            output_path="newpubs.sql")
