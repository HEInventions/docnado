title:      Environment Variables
desc:       Docnado Tooling Quick Reference
date:       2018/07/20
version:    1.0.0
template:   document
nav:        Tooling>Environment Variables
percent:    100
authors:    enq@heinventions.com

You can set these environment variables to configure docnado.

* `DN_FLASK_DEBUG` flag for enabling or disabling flask debug. Defaults to `TRUE`.
* `DN_RELOAD_ON_CHANGES` flag for reloading the server when a file changes. Defaults to `TRUE`.
* `DN_WKHTMLTOPDF` the path to the WkHTMLtoPDF binary. Defaults to `wkhtmltopdf_0.12.5.exe`.
* `DN_DOCS_DIR` the path to the directory that contains the documents. Defaults to `docs`.
* `DN_STYLE_DIR` the path to the directory that contains the style templates and resources. Defaults to `style`.
* `DN_PROJECT_LOGO` the path to the project logo *PNG* file. Defaults to `logo.png` in the current working directory.
