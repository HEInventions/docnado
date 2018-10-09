title:      Text Demo
desc:       Quick reference and showcase for how to use different text elements.
date:       2018/07/20
version:    1.0.0
template:   document
nav:        Demos>Text
percent:    100
authors:    enq@heinventions.com


This is intended as a quick reference and showcase. For more information on Markdown please see the [Python-Markdown](https://github.com/Python-Markdown/markdown) implementation.

# Headings

```markdown
# H1
## H2
### H3
#### H4
##### H5
###### H6
```

Please note that the software renders `# Heading 1` as a `<h2>` element. This way, `<h1>` is reserved for document titles and the PDF bookmark index / table of contents will generate correctly.
{: .info}

## Heading 2

Here is some text in a sub-heading.

# Text

**This text is bold**.

*This text is italic*.

`This text is referenced`.

```markdown
**This text is bold**.

*This text is italic*.

`This text is referenced`.
```

# Links

This is an [inline-style](assets/relative-link.md) relative link within the directory structure.

This is an [inline-style](https://github.com/boltdb/raw/blob/master/README.md) absolute link to another site.

```markdown

```

# Block Quotes

> Blockquotes can be handy in email to emulate reply text.
> This line is part of the same quote.

Quote break.

> This is a long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote.

```markdown
> This is a long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a blockquote.
```

# Callouts

Callouts are designed to draw attention to a particular class of information. This is a long information callout with **bold** text and *italic* text too. It is designed to span multiple lines so that you can see how the paragraph will break across the info callout.
{: .info}

Warning style callouts can be added too. Keep them punchy.
{: .warning}

Dangerous warnings go here.
{: .danger}

Take a look at the Markdown file to see how these are implemented.
{: .tip}


```markdown
Callouts are designed to draw attention to a particular class of information. This is a long information callout with **bold** text and *italic* text too. It is designed to span multiple lines so that you can see how the paragraph will break across the info callout.
{: .info}

Warning style callouts can be added too. Keep them punchy.
{: .warning}

Dangerous warnings go here.
{: .danger}

Take a look at the Markdown file to see how these are implemented.
{: .tip}
```

# Text Styles

You can also include <kbd>Ctrl</kbd>+<kbd>P</kbd> user input using the `<kbd>Alt</kbd>` HTML5 tag.

```markdown
You can also include <kbd>Ctrl</kbd>+<kbd>P</kbd> user input using the `<kbd>Alt</kbd>` HTML5 tag.
```
