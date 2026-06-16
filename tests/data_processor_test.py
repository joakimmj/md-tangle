import unittest
from md_tangle.data_processor import override_output_dest, transform_file_data


class OverrideOutputDestTest(unittest.TestCase):
    def test_filename_only(self):
        file_data = {
            "file1.txt": "<file content 1>",
            "file2.txt": "<file content 2>",
        }
        self.assertEqual(
            override_output_dest(file_data, "./new/path"),
            {
                "./new/path/file1.txt": "<file content 1>",
                "./new/path/file2.txt": "<file content 2>",
            },
        )

    def test_single_dest(self):
        file_data = {"~/old/path/file.txt": "<file content>"}
        self.assertEqual(
            override_output_dest(file_data, "./new/path"),
            {"./new/path/file.txt": "<file content>"},
        )

    def test_multiple_files(self):
        file_data = {
            "~/old/path/file1.txt": "<file content 1>",
            "~/old/path/file2.txt": "<file content 2>",
            "~/old/path/file3.txt": "<file content 3>",
        }
        self.assertEqual(
            override_output_dest(file_data, "./new/path"),
            {
                "./new/path/file1.txt": "<file content 1>",
                "./new/path/file2.txt": "<file content 2>",
                "./new/path/file3.txt": "<file content 3>",
            },
        )


class TransformFileDataTest(unittest.TestCase):
    def test_untagged_block(self):
        tangle_sources = {
            "f.py": [{"block": "untagged\n", "tags": []}]
        }
        result = transform_file_data(tangle_sources, [])
        self.assertEqual(result["f.py"], {"code_block": "untagged\n"})

        result = transform_file_data(tangle_sources, ["some-tag"])
        self.assertEqual(result["f.py"], {"code_block": "untagged\n"})

    def test_tagged_filtering(self):
        tangle_sources = {
            "f.py": [
                {"block": "t1\n", "tags": ["tag1"]},
                {"block": "t2\n", "tags": ["tag2"]}
            ]
        }
        # Excluded when no tags match
        result = transform_file_data(tangle_sources, [])
        self.assertEqual(result["f.py"], None)

        # Included when tag matches
        result = transform_file_data(tangle_sources, ["tag1"])
        self.assertEqual(result["f.py"], {"code_block": "t1\n"})

        # Multiple tags
        result = transform_file_data(tangle_sources, ["tag1", "tag2"])
        self.assertEqual(result["f.py"], {"code_block": "t1\nt2\n"})

    def test_block_padding(self):
        tangle_sources = {
            "f.py": [
                {"block": "b1", "tags": []},
                {"block": "b2", "tags": []}
            ]
        }
        result = transform_file_data(tangle_sources, [], block_padding=2)
        self.assertEqual(result["f.py"], {"code_block": "b1\n\nb2"})

    def test_copy_source(self):
        tangle_sources = {
            "img.png": [{"source": "src.png", "tags": ["img"]}]
        }
        result = transform_file_data(tangle_sources, ["img"])
        self.assertEqual(result["img.png"], {"source_file": "src.png"})

    def test_tangle_priority(self):
        tangle_sources = {
            "mixed.txt": [
                {"block": "block\n", "tags": []},
                {"source": "src.txt", "tags": []}
            ]
        }
        result = transform_file_data(tangle_sources, [])
        self.assertEqual(result["mixed.txt"], {"code_block": "block\n"})
