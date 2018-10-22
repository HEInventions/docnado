title:      Tables
desc:       Docnado Markdown Quick Reference
date:       2018/10/12
version:    1.0.0
template:   document
nav:        Document>Tables
percent:    100
authors:    enq@heinventions.com

A documentation project can often involve lots of tabular data, components with their pricing and order number, staff and their contact details etc. Luckily docnado supports tables in your document.

# Tables

Separate columns wish a pipe character (`|`) and rows with newlines. The head of the table is separated by lines of at least three dashes (`---`) in each cell of the 2nd line of a table. You can use the (`:`) character to left/right align each column.

More dashes can be used for readability.
{: .info}

```markdown
| Table Heading One               | Table Heading Two | Table Heading Three      |
|:--------------------------------|:-----------------:|-------------------------:|
|Table Item                       | Table item two    | Table item three         |
| This                            | is                | a row                    |
| Inside a table you can still use| _emphasis_        | and __strong emphasis__  |
```

| Table Heading One               | Table Heading Two | Table Heading Three      |
|:--------------------------------|:-----------------:|-------------------------:|
|Table Item                       | Table item two    | Table item three         |
| This                            | is                | a row                    |
| Inside a table you can still use| _emphasis_        | and __strong emphasis__  |

Most inline markdown syntax can still be used within a table including hyperlinks, emphasis and, inline code blocks.

Tables are not a part of the standard markdown specification, but docnado (and other markdown rendering tools) support this style as the _de facto_ standard.
{: .info}

At the moment, tables defined inside a Markdown document are **not** stylable using style classes `{: .my-table}`.
{: .warning}


# External Tables (CSV)

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
