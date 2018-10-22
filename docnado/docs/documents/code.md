title:      Code Highlighting
desc:       Docnado Markdown Quick Reference
date:       2018/10/12
version:    1.0.0
template:   document
nav:        Document>Code Highlighting
percent:    100
authors:    enq@heinventions.com

What if you're documenting a software product, or writing up a coding tutorial? Docnado has you covered. Create blocks of example code with syntax highlighting.

Use three backticks (` ``` `) followed by the language you wish to use.

```markdown
 ```C
#include <stdio.h>

main() {
        printf("Hello, World\n");
}
 ```
```
```C
#include <stdio.h>

main() {
        printf("Hello, World\n");
}
```

For complete information on highlighter used please see the [Highlight.js](https://highlightjs.org) implementation.

This is some **Python** code:

```python
def foo(bar):
    pass
```

This is some **JavaScript** code:

```javascript
function look(where) {
    if (where == 'here') {
        alert('woo');
    }
}
```

We can even highlight **markdown** code:

```markdown
# H1
I am **bold** and I am *italic*.
```

The [Atom](https://atom.io/) editor applies the syntax highlighting in the editor.
{: .tip}

Code blocks can also be used in an inline style, by putting a single backtick before and after your code sample, but remember docnado does not support highlighting in this mode.

```markdown
This is an example of how to use inline code blocks `C = map(lambda x: (float(5)/9)*(x-32), Fahrenheit)`.
```

This is an example of how to use inline code blocks `C = map(lambda x: (float(5)/9)*(x-32), Fahrenheit)`.
