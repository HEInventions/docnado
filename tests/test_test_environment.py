#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

"""Tests environment to make sure the test setup works"""


class TestTestEnvironment:
    """This test is just to make sure that the environment is set up correctly"""

    def test_print_path_to_tests_directory(self, capsys):
        """
        Print path to test directory on host
        """
        with capsys.disabled():
            print("\nPath to tests on host: ", sys.path[0])

    def test_Docnado_is_executable(self, testdirectory):
        """
        Test entrypoint and that Docnado is executable. If this fails no test can pass.
        """
        output = testdirectory.run('docnado --help')
        assert output.returncode == 0
