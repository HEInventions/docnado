# docnado

A rapid documentation tool to blow you away.

Docnado makes it easy to start and maintain a Markdown documentation project.  Store your own data your own way.

[![PyPI version](https://badge.fury.io/py/docnado.svg)](https://badge.fury.io/py/docnado)

# Basic Features

Docnado renders an adapted Markdown to provide:

* Images, Video, YouTube links, CSV tables.
* Code highlighting.
* File download blocks.
* Lists and Tables.
* Document defined template selection.
* Document Meta-data.
* Auto-generated index sidebar.

Docnado can:

* Output documents as insecure HTML on a localhost.
* Output documents as PDF files via the HTML server.
* Create a **static** set of HTML files that contain the documentation and related resources.

# Advanced Features

* Automatically find broken reference links in the generated HTML
* Automatically find orphan files (i.e. images) that are not referenced by generated HTML

# Usage

Basic usage with the default template:

```bash
python -m pip install docnado --upgrade
mkdir docs
vim docs/home.md # then add some documentation
docnado
```

Advanced usage with a custom templates and styles:

```bash
python -m pip install docnado --upgrade
docnado --new # copies sample style and docs into working directory
docnado # run the server
```

## Getting Started

If you are running from the script:

```bash
python docnado.py                       # start a server on localhost:5000

python docnado.py -h                    # list argument help

python docnado.py --html                # freeze the server into a static site as a set of HTML files
                                        # this will exit with -1 if there was a problem parsing any file

python docnado.py --pdf                 # generate a set of pdf files for each .md file - won't pull through
                                        # static resource files like with the --html command

python docnado.py --nav-limit           # include certain document trees only based on a comma separated list of
                                        # nav strings. e.g. Tooling,Document

python docnado.py --new                 # copy default templates and sample docs into the working directory
                                        # and update the config too, only if they don't already exist

python docnado.py --new-force           # copy default templates and sample docs into the working directory
                                        # and update the config too, this will overwrite any existing docs or
                                        # configs.

python docnado.py --dirs                # display all the different directories Docnado will use to generate
                                        # the documentation

python docnado.py --generate-meta DIR   # generate metadata for markdown files in the specified directory

python docnado.py --find-orphans        # display unreferenced media assets in the documentation

python docnado.py --find-broken-links   # display external broken links in the documentation

python docnado.py --port PORTNUMBER     # specify a port for Docnado to accept requests on

python docnado.py --host HOSTADDRESS    # set the docnado development server to listen on a specified IP address.
                                        # use '0.0.0.0' to listen on all available IPs
```

### Writing Documentation

Documents are managed using `meta-data` at the top of each document.
Documents can select which `template` they present themselves with.
Documents must end in **lowercase** `.md`. For example: `mydocument.md`.


### Environment Variables

* `DN_FLASK_DEBUG` flag for enabling or disabling flask debug. Defaults to `TRUE`.
* `DN_RELOAD_ON_CHANGES` flag for reloading the server when a file changes. Defaults to `TRUE`.
* `DN_WKHTMLTOPDF` the path to the WkHTMLtoPDF binary. Defaults to `wkhtmltopdf_0.12.5.exe`.
* `DN_DOCS_DIR` the path to the directory that contains the documents. Defaults to `docs`.
* `DN_STYLE_DIR` the path to the directory that contains the style templates and resources. Defaults to `style`.
* `DN_PROJECT_LOGO` the path to the project logo *PNG* file. Defaults to `logo.png` in the current working directory.

## Development

### Virtual Environment

```bash
python -m virtualenv env
env/Scripts/activate.bat # or the bash equivalent
pip install -r requirements.txt
```

```bash
python docnado.py # with options
```

```bash
pip install flake8
flake8 docnado.py --max-line-length=120
```

### WkHTMLtoPDF

To enable PDF output, WkHTMLtoPDF must be set in the config `DN_WKHTMLTOPDF` or `wkhtmltopdf_0.12.5.exe` placed in working directory.

This build uses version 0.12.5. Get it from here: https://wkhtmltopdf.org/downloads.html

### SCSS

The default theme is built using SCSS.

The SASSC compiler can be found here: http://libsass.ocbnet.ch/installer/
Usage: `sassc style/static/default.scss style/static/default.css`

If you want it to auto-watch, run as admin from this directory, and remember to disable your browser cache:

```bash
pip install watchdog
watchmedo shell-command --patterns="*.scss" --recursive --command='echo "${watch_src_path}" && sassc style/static/default.scss style/static/default.css' .
````

### Style

We use `flake8 docnado.py --max-line-length=110` to static check the code.

### Rebuilding the Package

PyPi

```bash
python -m pip install --user --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel

python -m twine upload dist/*
```

Executable

```bash
env\Scripts\activate.bat
pip install pyinstaller
pyinstaller docnado.py
```

## Roadmap

We are requesting pull-requests for the following features:

* [ ] Test cases and CI steps
* [ ] Responsive design in default template.
* [ ] Generate a large PDF file made from multiple documents (including table of contents with page numbers).
* [ ] Gravatar print CSS / absent internet in the default theme.
* [ ] Examples of Python extensions and SCSS extensions.
* [ ] New template themes.