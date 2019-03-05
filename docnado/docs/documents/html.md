title:      HTML Embedding
desc:       Docnado Markdown Quick Reference
date:       2019/05/19
version:    1.1.0
template:   document
inject:     custom.css.html
nav:        Document>HTML Embedding
percent:    100
authors:    enq@heinventions.com

Docnado supports the ability to embed HTML, CSS and JavaScript snippets. This allows you to extend Docnado's functionality and tailor it to your own projects.

## Inline Snippets
If you need to add a text input field to your document you can inject HTML snippets in-place by creating a document called `text_input.html`.

``` html
<textarea class="form-control" rows=4</textarea>
```

This can then be referenced within your documentation to inject it in-place.

```markdown
This text will be followed by a form.
![INJECT](text_input.html)
```

This text will be followed by a form.
![INJECT](text_input.html)

Docnado is built using bootstrap and supports it's use in snippets.
{: .tip}

Code injection also supports all of the same features you have when creating your own templates including Jinja2, with the addition of passing of named arguments. Your arguments should be surrounded by `"`, should be separated by a double-pipe `||` and are assigned with `=`.

It is important to remember that when using in-line code injection all of your code must be surrounded by a single tag!

``` html
<span>
  {%if label%}
    <label>{{label|safe}}</label>
  {% endif %}
  <textarea class="form-control" rows="{{form_rows|safe}}" {%if placeholder %} placeholder="{{placeholder|safe}}"{% endif %}></textarea>
</span>
```
```markdown
This text will be followed by a customised form.
![INJECT](custom_text_box.html "rows=2||placeholder=Your Text Here||label=Your Form Title")
```

This text will be followed by a customised form.

![INJECT](custom_text_box.html "form_rows=10||placeholder=Your Text Here||label=Your Form Title")

## Page-Wide Snippets

There is also the ability to import code snippets on a page-wide scale. This is most useful for injecting custom CSS stylesheets and JavaScript libraries.

Files can be added using the `inject:" element in a page's metadata. This is the metadata for the page you're looking at.

```markdown
title:      HTML Embedding
desc:       Docnado Markdown Quick Reference
date:       2019/05/19
version:    1.1.0
template:   document
inject:     custom.css.html
nav:        Document>HTML Embedding
percent:    100
authors:    enq@heinventions.com
```

Notice that although we are injecting CSS data, we are injecting an `html` document, this is because in in order to import into docnado we must use HTML semantics. `custom.css.html` contains the following code:

```html
<style>
 .blue {
    background-color: powderblue;
  }
</style>
```

This defines a page-wide CSS rule that makes elements with the `id #light-blue-background` render with a a background that is `powderblue`.

```html
<p class="blue">
  This paragraph has a powder blue background. It has been injected using an inline HTML injection and styled with a page-wide HTML injection.
</p>
```

![INJECT](blue_paragraph.html)

## Raw HTML

Embedding HTML within Docnado documents is also supported if you need it, but it is not a reccomended practice. It is hard to maintain and can cause unnessecary code duplication, but if you need it it's there!

```markdown
<marquee>This is a Docnado document with embedded HTML.</marquee>
```

<marquee>This is a Docnado document with embedded RAW HTML.</marquee>
