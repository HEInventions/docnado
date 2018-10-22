title:      Finding Unused Assets
desc:       Docnado Tooling Quick Reference
date:       2018/07/20
version:    1.0.0
template:   document
nav:        Tooling>Unused Assets
percent:    100
authors:    enq@heinventions.com


Unused assets (aka orphan files) are files in a project that are not linked to or referenced by any other part of a project.

Perhaps you have updated your project over time and they are no longer needed? Reminents of an earlier version now just taking up space? Or perhaps (even worse) they are important parts of your documentation that you've forgotten to include!

Luckily docnado has a handy tool for finding them.

Open a terminal and navigate to your documentation directory.

```bash
$ cd ~/my_project
$ ls
docs  logo.png  style
```

Then type:

```bash
docnado --find-orphans
3 Unused assets (orphans):
	/home/username/my_project/docs/this_page_is_not_used.md
	/home/username/my_project/docs/demo/assets/this_is_and_unused_picture.jpeg
	/home/username/my_project/docs/demo/assets/this_pdf_is_not_linked_to.pdf
```

Each line is a file in the `docs` folder that is either not in the `nav` menu or not linked to by an: image, pdf, video, wiki link, etc.
