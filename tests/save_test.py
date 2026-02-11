import unittest
import os
from unittest.mock import patch
from md_tangle.save import override_output_dest, save_to_file


class OverrideOutputDestTest(unittest.TestCase):
    def test_filename_only(self):
        code_blocks = {
            "file1.txt": "<file content 1>",
            "file2.txt": "<file content 2>",
        }
        self.assertEqual(
            override_output_dest(code_blocks, "./new/path"),
            {
                "./new/path/file1.txt": "<file content 1>",
                "./new/path/file2.txt": "<file content 2>",
            },
        )

    def test_single_dest(self):
        code_blocks = {"~/old/path/file.txt": "<file content>"}
        self.assertEqual(
            override_output_dest(code_blocks, "./new/path"),
            {"./new/path/file.txt": "<file content>"},
        )

    def test_multiple_files(self):
        code_blocks = {
            "~/old/path/file1.txt": "<file content 1>",
            "~/old/path/file2.txt": "<file content 2>",
            "~/old/path/file3.txt": "<file content 3>",
        }
        self.assertEqual(
            override_output_dest(code_blocks, "./new/path"),
            {
                "./new/path/file1.txt": "<file content 1>",
                "./new/path/file2.txt": "<file content 2>",
                "./new/path/file3.txt": "<file content 3>",
            },
        )


class SaveToFileTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = "/tmp/md_tangle_test_output"
        os.makedirs(self.temp_dir, exist_ok=True)
        self.temp_file = os.path.join(self.temp_dir, "test_file.txt")
        with open(self.temp_file, "w") as f:
            f.write("initial content")

    def tearDown(self):
        if os.path.exists(self.temp_file):
            os.remove(self.temp_file)
        if os.path.exists(self.temp_dir):
            os.rmdir(self.temp_dir)

    @patch("md_tangle.save.input")
    @patch("os.path.isfile")
    @patch(
        "md_tangle.save.os.makedirs"
    )  # Mock this to prevent actual directory creation outside of setUp
    def test_overwrite_yes(self, mock_makedirs, mock_isfile, mock_get_input):
        mock_isfile.return_value = True
        mock_get_input.return_value = "y"
        code_blocks = {self.temp_file: "new content"}
        save_to_file(code_blocks, force=False)
        with open(self.temp_file, "r") as f:
            self.assertEqual(f.read(), "new content")
        mock_get_input.assert_called_once_with(
            f"'{self.temp_file}' already exists. Overwrite? (Y/n) "
        )

    @patch("md_tangle.save.input")
    @patch("os.path.isfile")
    @patch("md_tangle.save.os.makedirs")
    def test_overwrite_no(self, mock_makedirs, mock_isfile, mock_get_input):
        mock_isfile.return_value = True
        mock_get_input.return_value = "n"
        code_blocks = {self.temp_file: "new content"}
        save_to_file(code_blocks, force=False)
        with open(self.temp_file, "r") as f:
            self.assertEqual(f.read(), "initial content")  # Should not be overwritten
        mock_get_input.assert_called_once_with(
            f"'{self.temp_file}' already exists. Overwrite? (Y/n) "
        )

    @patch("md_tangle.save.os.makedirs")
    def test_force_overwrite(self, mock_makedirs):
        # file exists, but force=True should ignore it
        code_blocks = {self.temp_file: "forced content"}
        save_to_file(code_blocks, force=True)
        with open(self.temp_file, "r") as f:
            self.assertEqual(f.read(), "forced content")

    @patch("md_tangle.save.os.makedirs")
    def test_new_file_creation(self, mock_makedirs):
        new_file = os.path.join(self.temp_dir, "new_file.txt")
        code_blocks = {new_file: "new file content"}
        save_to_file(code_blocks, force=False)
        with open(new_file, "r") as f:
            self.assertEqual(f.read(), "new file content")
        # Clean up the newly created file
        os.remove(new_file)

    @patch("md_tangle.save.print")  # Mock print to capture verbose output
    @patch("md_tangle.save.os.makedirs")
    def test_verbose_output(self, mock_makedirs, mock_print):
        code_blocks = {self.temp_file: "content\nwith\nlines"}
        save_to_file(code_blocks, verbose=True, force=True)
        mock_print.assert_called_once()
        # Check that the call includes the filename and line count
        expected_call_part = f"{self.temp_file}           3 lines"
        self.assertIn(expected_call_part, mock_print.call_args[0][0])
