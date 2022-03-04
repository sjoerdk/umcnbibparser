===============
UMCN bib parser
===============

lateX bib format parser for department of medical imaging research websites


* Free software: Apache license


Features
--------

* Parse lateX.bib bibliography entries into python dictionaries
* Additional mysql export functions for specific database structures

Installation
------------

* Install `python <https://www.python.org/downloads/>`_ and `git <https://git-scm.com/downloads>`_
* In a console, type::

    pip install git+https://github.com/sjoerdk/umcnbibparser.git

Upgrade
-------
* In a console, type::

    pip install --upgrade git+https://github.com/sjoerdk/umcnbibparser.git

Usage
-----
* create a file called `convert.py` with the following content (alter paths to fit your system)::

    from bibparser.core import convert

    if __name__ == "__main__":
        convert(bibfile_path="radiology.bib",
                bibstrings_path="fullstrings.bib",
                output_path="newpubs.sql")

* from console, run::

    python convert.py


Credits
-------

* Core parsing code written by members https://github.com/DIAGNijmegen
* Packaged by Sjoerd Kerkstra
