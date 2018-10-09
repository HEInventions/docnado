title:      Tables
desc:       Quick reference and showcase for how to define and use tables.
date:       2018/07/31
version:    1.0.0
template:   document
nav:        Demos>Tables
percent:    100
authors:    enq@heinventions.com


This is intended as a quick reference and showcase. For complete information on Markdown please see the [Python-Markdown](https://github.com/Python-Markdown/markdown) implementation.

# Basic Table

Tables are not part of the core Markdown spec, but they are supported.


```markdown
| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

There must be at least 3 dashes separating each header cell.
The outer pipes `|` are optional but recommended for consistently.
The raw Markdown does not need to line up neatly and you can use inline Markdown.

Markdown | Less | Pretty
--- | --- | ---
*Still* | `renders` | **nicely**
1 | 2 | 3

```

| Tables        | Are           | Cool  |
| ------------- |:-------------:| -----:|
| col 3 is      | right-aligned | $1600 |
| col 2 is      | centered      |   $12 |
| zebra stripes | are neat      |    $1 |

At the moment, tables defined in Markdown are **not** stylable using style classes `{: .my-table}`.
{: .warning}

<!-- | A  | B  | C  |
| -- | -- | -- |
| C1 | C2 | C3 |
| C1 | C2 | C3 |
| C1 | C2 | C3 |
| C1 | C2 | C3 |{: .full-width} -->

# External CSV Tables

You can include tables from CSV files. These will be loaded and inserted into the Markdown.

```markdown
![](assets/example.csv)
```

![](assets/example.csv)

Tables included from a `.csv` file can have styles applied. For example, `.full-width` makes the table stretch to fill the entire area.

```markdown
![](assets/example.csv){: .full-width}
```

![](assets/example.csv){: .full-width}
