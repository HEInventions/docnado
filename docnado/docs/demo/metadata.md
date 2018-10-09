title:      Meta-Data
desc:       Quick reference and showcase for how to define meta-data in a document.
date:       2018/07/20
version:    1.0.0
template:   document
nav:        Demos>Meta-Data
percent:    100
authors:    support@heinventions.com
            enq@heinventions.com


The [Python-Markdown Metadata Extension](https://python-markdown.github.io/extensions/meta_data/) extension is used to read information set out at the top of each document.  This data describes what the document is and how it should be presented.

As an example, the meta-data at the top of a `.md` document file might look like this:

```text
title:      Meta-Data
desc:       Quick reference and showcase for how to define meta-data in a document.
date:       2018/07/20
version:    1.0.0
template:   assembly
nav:        Demos>Meta-Data
percent:    100
authors:    support@heinventions.com
            enq@heinventions.com
```

You can add additional meta-data entries with your own names.  These will be accessible in the template HTML so you can use them to create custom styles.
{ .tip }

**title** defines the document name.

**desc** is a short punchy description of the document.

**date** defines in `YYYY/MM/DD` format the time of the last document update.

**version** contains the document version.  We recommend using [semantic versioning](https://semver.org/).

**template** says which `HTML` page should be used to render the content.  You can make your own `HTML` templates for different styles of documentation.

**nav** defines where the document should appear in the menu structure.  For instance `Folder A>Folder B>Doc Name` would put our document inside `Folder B` which is inside `Folder A`.  These folders are fake and you can put in whatever makes sense.

**percent** is a number between `0` and `100`.  If this is left out or is set to `100` then nothing happens.  However, if you are working on a document then setting this will put a progress bar in the document header.

**authors** defines a list of people (via email address) that have contributed to the document.  Each entry is on its own new line.
