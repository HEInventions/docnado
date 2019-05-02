title:      Meta-Data
desc:       Quick reference for how to define meta-data in a document.
date:       2019/03/07
version:    1.0.1
template:   document
nav:        Get Setup>Metadata
percent:    100
authors:    enq@heinventions.com

As you may have seen already, docnado uses [`markdown`](https://en.wikipedia.org/wiki/Markdown) (with our own extensions) to style your documentation, but how do we create our navigation menu, and page heading? The secret sauce is our metadata tags.

Docserve uses [Python-Markdown Metadata Extension](https://python-markdown.github.io/extensions/meta_data/) to read information at the top of every document so it can know what the document is about and how it should be presented. A typical example of our metadata would be:

```text
title:      Meta-Data
desc:       Quick reference for how to define meta-data in a document.
date:       2018/07/20
version:    1.0.0
template:   document
nav:        Get Setup>Metadata
percent:    100
authors:    support@heinventions.com
            enq@heinventions.com
```

title
: Defines the document name.

desc
: Is a short punchy description of the document.

date
: Defines in `YYYY/MM/DD` format the time of the last update to this document.

version
: Contains the document version. We recommend using [semantic versioning](https://semver.org/).

template
: Says which `HTML` page should be used to render the content. You can make your own `HTML` templates for different styles of documentation.

nav
: Defines where the document should appear in the menu structure. For instance `Folder A>Folder B>Doc Name` would put our document inside `Folder B` which is inside `Folder A`. These directories are artificial and you can put in whatever makes sense. You can also use `Folder A __99__>Folder B __-1__>Doc Name __12__` to apply weights that order the nav menu.

percent
: Is a number between `0` and `100`. If this is left out or is set to `100` then nothing happens. However, if you are working on a document then setting this will put a progress bar in the document header.

authors
: Defines a list of people (via email address) that have contributed to the document. Each entry is on its own new line.

Need more metadata? These aren't the only tags you can use, feel free to invent your own to tailor docnado to your own project.
The tags will be available in your template `HTML` and can be used to create your own templates and styles.
{ .tip }
