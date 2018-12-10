#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `docnado` package."""

from subprocess import call
import os


class TestRunDocnadoWithArguments:
    """
    These tests use the module 'pytest-testdirectory'.
    It creates a tmp-directory within .tox\\{env}\\tmp\\testname and runs the command.
    For usage see:
    github.com/steinwurf/pytest-testdirectory"""

    def test_Docnado_new(self, testdirectory):
        """
        User passes new. Should create required directories.
        """
        output = testdirectory.run('docnado --new')
        assert output.returncode == 0
        assert testdirectory.contains_dir('docs')
        assert testdirectory.contains_dir('style')
        assert testdirectory.contains_file('logo.png')

    def test_Docnado_help(self, testdirectory):
        """
        User passes help
        """
        output = testdirectory.run('docnado --help')
        assert output.stdout.match('*show this help message and exit*')
        assert output.returncode == 0

    def test_Docnado_broken_links(self, testdirectory):
        """
        Test broken link finding functionality:
        "docnado --find-broken-links"
        """
        broken_page = (
            'title:      TestPage\n'
            'desc:       This is a Docnado Test Page with a link error\n'
            'date:       2018/01/01\n'
            'version:    1.0.0\n'
            'template:   document\n'
            'nav:        Test\n'
            'percent:    100\n'
            'authors:    author@docnadoauthor\n'
            '\n'
            '# Welcome To The Test Page\n'
            '\n'
            'Welcome to the Docnado documentation.\n'
            '\n'
            'This is a sentence with a [Broken Link](http://255.255.255.255 "This is a broken link") in it.\n'
            '\n'
            'Browse the navigation bar to look at the documentation.\n'
            '{: .tip}\n'
        )

        testdirectory.run('docnado --new')
        output = testdirectory.run('docnado --find-broken-links')
        assert output.returncode == 0

        testdirectory.write_text('docs/test.md', broken_page, 'utf8')
        os.chdir(str(testdirectory))
        retval = call('docnado --find-broken-links', shell=True)
        assert retval == 255
