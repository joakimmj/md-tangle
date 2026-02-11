import unittest
import os
from unittest.mock import patch
from md_tangle.main import main
import md_tangle.main as main_module


class TangleTest(unittest.TestCase):
    def test_tangle(self):
        with patch.object(main_module, "__get_args") as mock_get_args:
            # default values
            mock_get_args.return_value.verbose = False
            mock_get_args.return_value.version = False
            mock_get_args.return_value.destination = None
            mock_get_args.return_value.include = ""
            mock_get_args.return_value.separator = ","
            # active arguments
            mock_get_args.return_value.filename = "tests/test.md"
            mock_get_args.return_value.force = True
            main()

        output_file = "tests/output/basic/wezterm.lua"
        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(os.path.exists("tests/output/basic/hello_world1.lua"))
        self.assertTrue(os.path.exists("tests/output/basic/hello_world2.lua"))

        with open(output_file, "r") as f:
            content = f.read()
            self.assertIn("local wezterm = require 'wezterm'", content)
            self.assertNotIn("config.font = wezterm.font_with_fallback", content)
            self.assertIn("config.enable_tab_bar = false", content)
            self.assertIn("config.disable_default_key_bindings = true", content)
            self.assertNotIn("config.wsl_domains", content)
            self.assertIn("return config", content)
            self.assertNotIn("-- not tangled", content)
            self.assertNotIn("-- no files", content)
            self.assertNotIn("-- only tagged", content)

    def test_tangle_overwrite_destination(self):
        output_dir = "tests/output/overridden-path"
        with patch.object(main_module, "__get_args") as mock_get_args:
            # default values
            mock_get_args.return_value.verbose = False
            mock_get_args.return_value.version = False
            mock_get_args.return_value.separator = ","
            # active arguments
            mock_get_args.return_value.filename = "tests/test.md"
            mock_get_args.return_value.force = True
            mock_get_args.return_value.destination = output_dir
            mock_get_args.return_value.include = "theme"
            main()

        output_file = os.path.join(output_dir, "wezterm.lua")
        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(os.path.exists("tests/output/basic/hello_world1.lua"))
        self.assertTrue(os.path.exists("tests/output/basic/hello_world2.lua"))

        with open(output_file, "r") as f:
            content = f.read()
            self.assertIn("local wezterm = require 'wezterm'", content)
            self.assertIn("config.font = wezterm.font_with_fallback", content)
            self.assertIn("config.enable_tab_bar = false", content)
            self.assertIn("config.disable_default_key_bindings = true", content)
            self.assertNotIn("config.wsl_domains", content)
            self.assertIn("return config", content)
            self.assertNotIn("-- not tangled", content)
            self.assertNotIn("-- no files", content)
            self.assertNotIn("-- only tagged", content)

    def test_tangle_tag(self):
        output_dir = "tests/output/with-tags"
        with patch.object(main_module, "__get_args") as mock_get_args:
            # default values
            mock_get_args.return_value.verbose = False
            mock_get_args.return_value.version = False
            mock_get_args.return_value.separator = ","
            # active arguments
            mock_get_args.return_value.filename = "tests/test.md"
            mock_get_args.return_value.force = True
            mock_get_args.return_value.destination = output_dir
            mock_get_args.return_value.include = "styling,wsl"
            main()

        output_file = os.path.join(output_dir, "wezterm.lua")
        self.assertTrue(os.path.exists(output_file))
        self.assertTrue(os.path.exists("tests/output/basic/hello_world1.lua"))
        self.assertTrue(os.path.exists("tests/output/basic/hello_world2.lua"))

        with open(output_file, "r") as f:
            content = f.read()
            self.assertIn("local wezterm = require 'wezterm'", content)
            self.assertIn("config.font = wezterm.font_with_fallback", content)
            self.assertIn("config.enable_tab_bar = false", content)
            self.assertIn("config.disable_default_key_bindings = true", content)
            self.assertIn("config.wsl_domains", content)
            self.assertIn("return config", content)
            self.assertNotIn("-- not tangled", content)
            self.assertNotIn("-- no files", content)
            self.assertNotIn("-- only tagged", content)
