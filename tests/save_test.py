import unittest
from md_tangle.save import override_output_dest


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
