#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `docnado` package."""


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
