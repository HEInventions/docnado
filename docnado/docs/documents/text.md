title:      Text Styles
desc:       Docnado Markdown Quick Reference
date:       2018/10/12
version:    1.0.0
template:   document
nav:        Document>Text Styles
percent:    100
authors:    enq@heinventions.com

# Headings

Mark the start of section, subsection, or paragraph with the *header* tag. This is a hash symbol `#` followed by a space, the text you want to use.

```markdown
# H1
## H2
### H3
#### H4
##### H5
###### H6
```

# H1
## H2
### H3
#### H4
##### H5
###### H6


Please note that Docnado will render `# Heading 1` as a `<h2>` element. This way, `<h1>` is reserved for document titles and the PDF bookmark index / table of contents will generate correctly.
{: .info}

# Text Styles

**Sometimes** you need to be _emphatic_ in your documentation, luckily markdown has tools to do this for you.


**This text is bold**.

*This text is italic*.

`This text is referenced`.

~~This text is strike through~~.

```markdown
**This text is bold**.

*This text is italic*.

`This text is referenced`.

~~This text is strike through~~.
```

# Block Quotes

Blockquotes are a text block that is generally used for showing quotations. They are useful for any discussion on a project, email or other document quotations, or for just being motivational.

You declare them by simply using a greater-than symbol followed by a space (`> `)  at the start of each line and end them with a new line.

```markdown
> "Do not meddle in the affairs of wizards, for they are subtle and quick to anger!" - J.R.R Tolkien
```

> "Do not meddle in the affairs of wizards, for they are subtle and quick to anger!" - J.R.R Tolkien

Quote break.

```markdown
> This is a long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a block-quote.
```

> This is a long line that will still be quoted properly when it wraps. Oh boy let's keep writing to make sure this is long enough to actually wrap for everyone. Oh, you can *put* **Markdown** into a block-quote.


# Text Styles

You can also include <kbd>Ctrl</kbd>+<kbd>P</kbd> user input using the `<kbd>Alt</kbd>` HTML5 tag.

```markdown
You can also include <kbd>Ctrl</kbd>+<kbd>P</kbd> user input using the `<kbd>Alt</kbd>` HTML5 tag.
```

# Horizontal Rules

Horizontal Rules are great for creating a visual horizontal separation in your documentation, use them to separate logical sections of a document. They are created by creating three consecutive hyphens (`---`), asterisks (`***`), or underscores (`___`) at the start of a new line.

```markdown
This text is followed by a horizontal rule.
___
So is this one
---
And this one is too!
***
```
This text is followed by a horizontal rule.
___

So is this one
---
And this one is too!
***
