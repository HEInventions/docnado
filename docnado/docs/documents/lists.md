title:      Lists
desc:       Docnado Markdown Quick Reference
date:       2018/10/12
version:    1.0.0
template:   document
nav:        Document>Lists
percent:    100
authors:    enq@heinventions.com

Markdown can be used to create lists of items, both ordered and unordered. These lists can also have ordered and unordered sublets.

An ordered list item can be simply created by tying a number, followed by a period (`.`), and ended with a new line. Unordered lists are created in much the same way but instead of a number you must use an asterisk (`*`), a dash (`-`), or a plus (`+`).

You can also format paragraphs within lists by beginning a new line below a list item with a tab.

```markdown
1. The first item in an ordered list.
	* Unordered sub-list item one.
	* Unordered sub-list item two.

2. The second item in an ordered list.

	A new line in the paragraph that runs on from the second item in the ordered list.  
	A second new line in the paragraph. The preceding line must end in a double space to avoid starting a new paragraph.

3. The third item in an ordered list.

+ An unordered list created with a plus.
	1. Ordered sub-list item one.
	2. Ordered sub-list item two.

* Unordered list item two created with an asterisk.

- Unordered list item three created with a dash.
```

1. The first item in an ordered list.
	* Unordered sub-list item one.
	* Unordered sub-list item two.

2. The second item in an ordered list.

	A new line in the paragraph that runs on from the second item in the ordered list.  
	A second new line in the paragraph. The preceding line must end in a double space to avoid starting a new paragraph.

3. The third item in an ordered list.

+ An unordered list created with a plus.
	1. Ordered sub-list item one.
	2. Ordered sub-list item two.

* Unordered list item two created with an asterisk.

- Unordered list item three created with a dash.

Usefully, docnado also supports other list styles:

# Progress Lists
A progress list is a list of check boxes:

* [ ] This is one.
* [X] This is two. It happens to be a long list item designed to test how the styling copes with the multiples lines generated.
* [ ] This is three.
```markdown
* [ ] This is one.
* [X] This is two. It happens to be a long list item designed to test how the styling copes with the multiples lines generated.
* [ ] This is three.
```

# Definition Lists
Glossary-style definition lists are achieved as follows:

Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.

```markdown
Apple
:   Pomaceous fruit of plants of the genus Malus in
    the family Rosaceae.

Orange
:   The fruit of an evergreen tree of the genus Citrus.
```
