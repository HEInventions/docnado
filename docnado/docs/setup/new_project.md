title:      Creating a New Project
desc:       The official docnado installation guide.
date:       2018/10/11
version:    1.0.0
template:   document
nav:        Get Setup>New Project
percent:    100
authors:    enq@heinventions.com

# Basic Project

To start a new docnado project that uses the existing style, you need to:

1. Create a new folder for your documentation. Let's call it `mydocs`.
1. Inside the `mydocs` folder, create another folder called `docs`.
1. Inside the `mydocs` folder, create a `PNG` called `logo.png`. This is used as your project logo.
1. Inside the `docs` folder create a file called `home.md`. This is the first document your users will see when visiting the documentation.
1. Create more documents and add meta-data to each one.

# Advanced Project

If you want to be able to add custom styles, you can use the `--new` command that comes with docnado. This will copy all the example documentation and styles into `docs` and `style` folders.

```bash
$ mkdir ~/documentation_project
$ cd documentation_project
$ docnado --new         # copies sample style and docs into working directory
$ docnado               # run the server
```

This will create a basic example of a documentation project using docnado, and demonstrate all of it's useful features. Just run:

```bash
$ docnado
 * Serving Flask app "docnado.docnado" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

And visit http://127.0.0.1:5000 to see docnado in action.

If you make changes to the templates and styles, you will need to rebuild the `scss` and restart docnado.
{: .tip}
