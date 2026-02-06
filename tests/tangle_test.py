import unittest
import os
from unittest.mock import patch
from md_tangle.main import main
import md_tangle.main as main_module

class TangleTest(unittest.TestCase):
    def test_tangle_file(self):
        with patch.object(main_module, '__get_args') as mock_get_args:
            mock_get_args.return_value.filename = 'tests/test.md'
            mock_get_args.return_value.force = True
            mock_get_args.return_value.destination = None
            mock_get_args.return_value.separator = ','
            mock_get_args.return_value.verbose = False
            mock_get_args.return_value.version = False
            main()

        output_file = 'tests/output/basic/wezterm.lua'
        self.assertTrue(os.path.exists(output_file))

        with open(output_file, 'r') as f:
            content = f.read()
            self.assertIn("local wezterm = require 'wezterm'", content)
            self.assertIn("config.font = wezterm.font_with_fallback", content)
            self.assertIn("config.enable_tab_bar = false", content)
            self.assertIn("config.disable_default_key_bindings = true", content)
            self.assertIn("return config", content)
            self.assertNotIn("config.wsl_domains", content)

    def test_tangle_force_overwrite(self):
        output_dir = 'tests/output/overridden-path'
        with patch.object(main_module, '__get_args') as mock_get_args:
            mock_get_args.return_value.filename = 'tests/test.md'
            mock_get_args.return_value.force = True
            mock_get_args.return_value.destination = output_dir
            mock_get_args.return_value.separator = ','
            mock_get_args.return_value.verbose = False
            mock_get_args.return_value.version = False
            main()

        output_file = os.path.join(output_dir, 'wezterm.lua')
        self.assertTrue(os.path.exists(output_file))

        with open(output_file, 'r') as f:
            content = f.read()
            self.assertIn("local wezterm = require 'wezterm'", content)
            self.assertIn("config.font = wezterm.font_with_fallback", content)
            self.assertIn("config.enable_tab_bar = false", content)
            self.assertIn("config.disable_default_key_bindings = true", content)
            self.assertIn("return config", content)
            self.assertNotIn("config.wsl_domains", content)