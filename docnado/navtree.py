""" Navigation Tree for docnado

python -m doctest .\navtree.py
"""

import re


def parse_nav_string(nav):
    """ Parse a nav string and pull out the `name` and `weight` of each nav item.

    >>> parse_nav_string('Foo>Bar>Baz')
    [('Foo', 0), ('Bar', 0), ('Baz', 0)]

    >>> parse_nav_string('Foo __99__>Bar>Baz')
    [('Foo', 99.0), ('Bar', 0), ('Baz', 0)]

    >>> parse_nav_string('Foo __-1__>Bar>Baz')
    [('Foo', -1.0), ('Bar', 0), ('Baz', 0)]

    >>> parse_nav_string(None)
    []
    """
    NAV_PARSER = r'\w+\s*__(-?\d+)__'
    if not nav:
        return []

    def _weight(chunk):
        matches = re.search(NAV_PARSER, chunk)
        return float(matches.group(1)) if matches else 0

    def _name(chunk):
        return chunk.split('__')[0].strip()

    chunks = [(_name(chunk), _weight(chunk)) for chunk in nav.split('>')]
    return chunks


class NavItem:
    """ An item (either based on a document or not) that appears in the Nav menu.

    >>> NavItem('root', 0).name
    'root'

    >>> NavItem('root', 0).weight
    0
    """

    def __init__(self, name, weight):
        self.name = name
        self.weight = weight
        self.dom_id = self.name.replace(' ', '-')
        self.children = []

    def items(self):
        """ Return pairs of names,items of the children.
        """
        return [(child.name, child) for child in self.children]

    def bind(self, meta, link):
        """ Bind a file link to the document and its associated metadata to this NavItem.
        """
        self.meta = meta
        self.link = link

    def add(self, node):
        """ Add a new child to this menu item. If a child with the same name already
        exists then return that child. If a child with the same name does not
        already exist, then add the item we pass in and return it.

        >>> a = NavItem('root', 0)
        >>> na = a.add(NavItem('A', 10))
        >>> nb = a.add(NavItem('A', 15))
        >>> nc = a.add(NavItem('C', 20))
        >>> len(a.children) == 2
        True
        >>> na.weight == 10
        True
        >>> na in a.children
        True
        >>> nb == na
        True
        >>> nc in a.children
        True
        """
        for c in self.children:
            if c.name == node.name:
                if c.weight == 0:
                    c.weight = node.weight

                return c
        self.children.append(node)
        return node

    def arrange(self):
        """ Sort all the children of this node by their weight.  Then tell them
        to sort themselves in turn.

        >>> nav = NavItem("home", 0)
        >>> n1 = nav.add(NavItem("A", 10))
        >>> nav.children[0].name
        'A'

        >>> n2 = nav.add(NavItem("C", 30))
        >>> nav.children[1].name
        'C'

        >>> n3 = nav.add(NavItem("B", 20))
        >>> nav.arrange()
        >>> nav.children[0].name
        'A'
        >>> nav.children[0].weight == 10
        True

        >>> nav.children[1].name
        'B'
        >>> nav.children[1].weight == 20
        True

        >>> nav.children[2].name
        'C'
        >>> nav.children[2].weight == 30
        True
        """
        self.children.sort(key=lambda c: c.weight, reverse=False)
        for c in self.children:
            c.arrange()

    def _debug(self, level=0):
        """ Print out the data of this objcect to the console in a nicely formatted
        output. Intended for debugging only.
        """
        print('  ' * level, self.name, self.weight)
        for c in self.children:
            c.debug(level + 1)
