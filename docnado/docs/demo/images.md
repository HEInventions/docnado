title:      Images and Video
desc:       Quick reference and showcase for different images and video style elements.
date:       2018/07/31
version:    1.0.0
template:   document
nav:        Demos>Images and Video
percent:    100
authors:    enq@heinventions.com


This is intended as a quick reference and showcase. For complete information on Markdown please see the [Python-Markdown](https://github.com/Python-Markdown/markdown) implementation.


If you are using the [Atom](https://atom.io/) editor, the [markdown-image-assistant](https://atom.io/packages/markdown-image-assistant) plugin will enable copy and paste images into the editor.
{: .tip}

# Images

A number of image styles and tags are supported.

![Example Plugin Usage](assets/images-95cf4590.png "Example usage of the markdown-image-assistant plugin")

Images are found in the relative path to the document. The format of an include is:

`![ALT](myfolder/graphic.png "Title HTML Attribute")`.

**Avoid** using `<img>` directly. Different image styles can be added by placing a `{: .classname}` on the line directly below an image include. The following are available:

```markdown
<!-- Example -->
![ALT](myfolder/graphic.png "Title Hover Text")

<!-- A row of 3 images -->
![](assets/images-05a8fd7e.png){: .small}
![](assets/images-05a8fd7e.png){: .small}
![](assets/images-05a8fd7e.png){: .small}

<!-- Style classes can be combined. -->
![](assets/images-05a8fd7e.png){: .small .noborder}

<!-- We can put them in the middle. -->
![](assets/images-05a8fd7e.png){: .small .center}

<!-- Make them middle sized. -->
![](assets/images-05a8fd7e.png){: .medium}

<!-- The default is actual width up to a max height of the document flow, and no higher than a single A4 page. -->
![](assets/images-05a8fd7e.png)

<!-- The style class .large is the same as the default. -->
![](assets/images-05a8fd7e.png){: .large}

```

Unlike paragraphs, images are *inline* elements, so the style `{: style-class}` needs to be on the same line as the element.
{: .info}


This is an inline ![](assets/images-05a8fd7e.png){: .icon} icon.

![](assets/images-05a8fd7e.png){: .small}
![](assets/images-05a8fd7e.png){: .small}
![](assets/images-05a8fd7e.png){: .small}

![](assets/images-05a8fd7e.png){: .small .noborder}

![](assets/images-05a8fd7e.png){: .small .center}

![](assets/images-05a8fd7e.png){: .medium}

![](assets/images-05a8fd7e.png)

![](assets/images-05a8fd7e.png){: .large}


# Videos

Videos can be inserted using the same technique as images.

```markdown
![](assets/big_buck_bunny.ogv){: .small}

![](assets/big_buck_bunny.ogv){: .medium}

![](assets/big_buck_bunny.ogv)
```

<!-- Videos are *block* elements, so the style `{: style-class}` needs to be on the line below the element.
{: .info} -->

Supported formats include: `.ogv`, `.ogg`, `webm`, `mp4`, and in some browsers `avi`.
{: .info}

![](assets/big_buck_bunny.ogv){: .small}

![](assets/big_buck_bunny.ogv){: .medium}

![](assets/big_buck_bunny.ogv)



# YouTube

YouTube videos can also be embed into the document directly with the normal image and link format.

```markdown
![](https://www.youtube.com/embed/Jg48NhtIDV8){: .small}

![](https://www.youtube.com/embed/Jg48NhtIDV8){: .medium}

![](https://www.youtube.com/embed/Jg48NhtIDV8)
```

![](https://www.youtube.com/embed/Jg48NhtIDV8){: .small}

![](https://www.youtube.com/embed/Jg48NhtIDV8){: .medium}

![](https://www.youtube.com/embed/Jg48NhtIDV8)

# PDF

PDF documents can be displayed too. You can add a `{: .landscape}` property to these in order to change the aspect ratio. Only the `A4` paper aspect is currently supported.

```markdown
![](assets/example.pdf)

![](assets/example.pdf){: .landscape}

```

![](assets/example.pdf)

![](assets/example.pdf){: .landscape}
