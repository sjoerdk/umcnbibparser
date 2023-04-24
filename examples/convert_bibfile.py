"""Convert radiology.bib, use journal titles from fullstrings.bib.
Write sql file to newpubs.sql

"""
from bibparser.core import convert

if __name__ == "__main__":
    convert(bibfile_path="/home/sjoerd/svn/literature/radiology.bib",
            bibstrings_path="/home/sjoerd/svn/literature/fullstrings.bib",
            output_path="/home/sjoerd/svn/literature/newpubs_test.sql")
