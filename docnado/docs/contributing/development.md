title:      Development
desc:       Docnado Tooling Quick Reference
date:       2018/07/20
version:    1.0.0
template:   document
nav:        Contributing __4__>Development
percent:    100
authors:    enq@heinventions.com


## Virtual Environment

A virtual environment allows you to iscolate your development from the rest of your Python installation. If this doesn't bother you, then you can probably skip this.

```python
python -m virtualenv env
env/Scripts/activate.bat # or the bash equivalent
pip install -r requirements.txt
```

```python
python docnado.py # with options
```

```python
pip install flake8
flake8 docnado.py --max-line-length=120
```

## SCSS

The default theme is built using SCSS.

The SASSC compiler can be found here: http://libsass.ocbnet.ch/installer/
Usage: `sassc style/static/default.scss style/static/default.css`

If you want it to auto-watch, run as admin from this directory, and remember to disable your browser cache:

```bash
pip install watchdog
watchmedo shell-command --patterns="*.scss" --recursive --command='echo "${watch_src_path}" && sassc style/static/default.scss style/static/default.css' .
```

## Code Style

We use `flake8 docnado.py --max-line-length=110` to static check the code.

## Rebuilding the PyPi Package

PyPi

```
python -m pip install --user --upgrade setuptools wheel twine
python setup.py sdist bdist_wheel

python -m twine upload dist/*
```

## Rebuilding the EXE Package

Executable

```
env\Scripts\activate.bat
pip install pyinstaller
pyinstaller docnado.py
```
