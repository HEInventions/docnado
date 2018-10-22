title:      Images
desc:       Docnado Markdown Quick Reference
date:       2018/10/12
version:    1.0.0
template:   document
nav:        Document>Images
percent:    100
authors:    enq@heinventions.com

Embedding images in your docnado documents follows a similar syntax to [links](links.md), but should be preceded by an exclamation mark (`!`). In this case the text within square brackets functions as image alt-text.

```markdown
Inline
![docnado](assets/logo.png "docnado, blow your documentation away!")

![alt text][logo]

[logo]: /assets/logo.png "Logo Title Text 2"
```

![docnado](assets/logo.png "docnado, blow your documentation away!")

[logo]: assets/logo.png "docnado, blow your documentation away!"

![docnado Image 2 ][logo]

Docnado also supports the styling of images, this can be done by adding an inline style tag after your image.

```markdown
<!-- Example -->
<!-- A row of 3 images -->
![](assets/logo.png){: .small}
![](assets/logo.png){: .small}
![](assets/logo.png){: .small}
```

![](assets/logo.png){: .small}
![](assets/logo.png){: .small}
![](assets/logo.png){: .small}


```markdown
<!-- Style classes can be combined. -->
![](assets/logo.png){: .small .noborder}
```

![](assets/logo.png){: .small .noborder}


```markdown
<!-- We can put them in the middle. -->
![](assets/logo.png){: .small .center}
```

![](assets/logo.png){: .small .center}

```markdown
<!-- Make them middle sized. -->
![](assets/logo.png){: .medium}
```

![](assets/logo.png){: .medium}

```markdown
<!-- The default is actual width up to a max height of the document flow, and no higher than a single A4 page. -->
![](assets/logo.png)

<!-- The style class .large is the same as the default. -->
![](assets/logo.png){: .large}
```

![](assets/logo.png)

![](assets/logo.png){: .large}

Unlike paragraphs, images are *inline* elements, so the style `{: .style-class}` needs to be on the same line as the element.
{: .info}

```markdown
This is an inline ![](assets/logo.png){: .icon} icon.
```

This is an inline ![](assets/logo.png){: .icon} icon.
