#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `aws_consoler` CLI."""


import unittest

from aws_consoler import cli


class TestCLI(unittest.TestCase):
    """
    Tests for `aws_consoler` package.
    At the moment, this only includes tests for command-line arguments
    """

    def setUp(self):
        """Set up test fixtures, if any."""
        pass

    def tearDown(self):
        """Tear down test fixtures, if any."""
        pass

    def test_000_help(self):
        """Test no arguments to the CLI (expect help output)."""
        with self.assertRaises(SystemExit) as e:
            cli.main(["-h"])
        self.assertEqual(e.exception.code, 0)

    def test_001_all_arguments(self):
        """Test all arguments to the CLI (expect error)."""
        with self.assertRaises(SystemExit) as e:
            cli.main(["-p foo", "-a bar", "-s baz", "-t bul", "-r foo", "-R BAZ", "-o", "-v"])
        self.assertEqual(e.exception.code, 2)

    def test_002_profile_and_creds(self):
        """Test providing both a profile and credentials to the CLI."""
        with self.assertRaises(SystemExit) as e:
            cli.main(["-p foo", "-a bar", "-s baz", "-t bul"])
        self.assertEqual(e.exception.code, 2)

    def test_003_partial_creds(self):
        """Test providing only one credential argument to the CLI."""
        with self.assertRaises(SystemExit) as e:
            cli.main(["-a bar"])
        self.assertEqual(e.exception.code, 2)

    def test_004_token_only(self):
        """Test providing only a session token to the CLI."""
        with self.assertRaises(SystemExit) as e:
            cli.main(["-t bul"])
        self.assertEqual(e.exception.code, 2)

    def test_005_logic_exception(self):
        """Test malformed credentials to the CLI (passed in to logic)."""
        with self.assertRaises(SystemExit) as e:
            cli.main(["-a foo", "-s bar"])
        self.assertEqual(e.exception.code, 1)

