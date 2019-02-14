title:      Command Line Interface
desc:       Docnado Tooling Quick Reference
date:       2018/07/20
version:    1.0.5
template:   document
nav:        Tooling>CLI
percent:    100
authors:    enq@heinventions.com


Docnado offers the following command line interface options:

```
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
