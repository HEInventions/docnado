title:      Extra Tips
desc:       Other handy tools that work with Docnado
date:       2018/11/01
version:    1.0.0
template:   document
nav:        Tooling>Extra Tips
percent:    100
authors:    enq@heinventions.com

One advantage Docnado offers over other documentation services is it's ability to be enhanced by using other tools, instead of waiting for the upstream developer to add the features you need *now* or committing the time to developing them yourself you can use any other existing software designed to handle markdown or plain text files.

This page isn't really part of the tutorial on our system, think of it more as handy cheat sheet on how to use other tools with Docnado documents an an example of the benefits of storing your documentation in plain text.

# Searching
Finding a word or phrase in your entire Docnado project can made simple with grep.
```bash
$ grep -rnw docs/*/*.md -e 'unordered list'
docs/documents/lists.md:28:+ An unordered list created with a plus.
docs/documents/lists.md:48:+ An unordered list created with a plus.
```

# Spell Cheking
There are many handy tools for spellchecking plain text documents. For example:
``` bash
aspell check docs/documents/text.md 
```
