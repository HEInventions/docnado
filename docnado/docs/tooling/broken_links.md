title:      Finding Broken Links
desc:       Docnado Tooling Quick Reference
date:       2018/07/20
version:    1.0.0
template:   document
nav:        Tooling __3__>Broken Links
percent:    100
authors:    enq@heinventions.com

What happens when your markdown links to a local file or web page that doesn't exist? Did somebody delete a file that another document in another part of the project referenced?

Not controlling this is the fastest way to let documentation become messy.

Open a terminal and navigate to your documentation directory.

```bash
$ cd ~/my_project
$ ls
docs  logo.png  style
```

Then run the tool:

```bash
$ docnado --find-broken-links
/home/user/my_project/docs/home.md
	/home/user/my_project/docs/assets/this_does_not_exist.pdf
/home/user/my_project/docs/demo/text.md
	https://github.com/boltdb/raw/blob/master/README.md
```

Each line that is not intended is the file that is currently being analysed. Each indented link is the referenced file.

This tool will even check online to verify that the link returns a `200 OK` HTTP response.
