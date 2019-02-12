title:      Text Links
desc:       Docnado Markdown Quick Reference
date:       2018/10/12
version:    1.0.0
template:   document
nav:        Document>Text Links
percent:    100
authors:    enq@heinventions.com


# Links

Linking to other pages of your documentation or to pages on the wider web uses the hyperlink syntax.

Creating a link to a web-page or other document is achieved by surrounding the word or phrase you want to make into a link with square brackets (`[` and `]`) and following it with the location of the website you want to link to, surrounded by parentheses (`(` and `)`). Alt-text can be added by using speech marks (`"`) after the web address, but this is optional.

For example:
```markdown
This is a sentence with a link to the [Google Homepage](http://www.google.co.uk "Google Search Homepage") in it.
```

This is a sentence with a link to the [Google Homepage](http://www.google.co.uk "Google Search Homepage") in it.

# Relative and Web Links
This is an [inline-style](assets/relative_link.md) relative link within the directory structure.

This is an [inline-style](https://github.com/boltdb/raw/blob/master/README.md) absolute link to another site.

```markdown
This is an [inline-style](assets/relative_link.md) relative link within the directory structure.

This is an [inline-style](https://github.com/boltdb/raw/blob/master/README.md) absolute link to another site.
```

Be sure to check out our [tooling](../tooling/broken_links.md) section to see how you can automatically check for broken references.
{: .tip}

# Reference Style Linking
Another useful feature is reference style linking. You can create a list of web links anywhere within your document (we recommend at the end) and re-use them throughout your document.

```markdown
[Google]: http://www.google.co.uk
[Twitter]: http://www.twitter.com
[Wikipedia]: http://en.wikipedia.org

These links go to [Google], [Twitter's Homepage][Twitter], and [Wikipedia]
```

[Google]: https://www.google.co.uk
[Twitter]: https://twitter.com
[Wikipedia]: https://en.wikipedia.org/wiki/Main_Page

These links go to [Google], [Twitter's Homepage][Twitter], and [Wikipedia]