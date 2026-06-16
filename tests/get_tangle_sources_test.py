import unittest
import os
from pathlib import Path
import tempfile
from md_tangle.tangle import get_tangle_sources
from unittest.mock import patch


class AbsolutePathsTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_path = Path(self.temp_dir.name).resolve()
        self.fake_home = self.base_path / "fake_home"
        self.mock_env = {
            "HOME": str(self.fake_home),
            "USERPROFILE": str(self.fake_home),
            "HOMEPATH": str(self.fake_home)
        }

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_md_file(self, filename: str, content: str) -> str:
        file_path = self.base_path / f"test_{filename}.md"
        file_path.write_text(content, encoding="utf8")
        return str(file_path)

    def create_md_content(self, tangle_path: str) -> str:
        return f'\n```python tangle:{tangle_path}\nprint("hello")\n```\n'

    @patch("md_tangle.tangle.Path.home")
    @patch.dict("os.environ", {"HOME": "", "USERPROFILE": "", "HOMEPATH": ""})
    def test_make_absolute_with_real_files(self, mock_home):
        mock_home.return_value = self.fake_home
        os.environ.update(self.mock_env)
        test_cases = [
            {
                "name": "basic_relative_sibling",
                "markdown_path": "output.py",
                "expected": str(self.base_path / "output.py")
            },
            {
                "name": "relative_nested_subdirectory",
                "markdown_path": "build/src/output.py",
                "expected": str(self.base_path / "build" / "src" / "output.py")
            },
            {
                "name": "relative_parent_directory",
                "markdown_path": "../output.py",
                "expected": str(self.base_path.parent / "output.py")
            },
            {
                "name": "already_absolute_path",
                "markdown_path": str(self.base_path / "global_output.py"),
                "expected": str(self.base_path / "global_output.py")
            },
            {
                "name": "user_home_expansion",
                "markdown_path": "~/my_project/output.py",
                "expected": str(self.fake_home / "my_project" / "output.py")
            }
        ]

        for case in test_cases:
            with self.subTest(msg=case["name"]):
                md_content = self.create_md_content(case["markdown_path"])
                file_path_str = self.create_md_file(case['name'], md_content)
                sources = get_tangle_sources(file_path_str, ",")
                expected_path = case["expected"]

                self.assertIn(expected_path, sources)
                self.assertEqual(len(sources[expected_path]), 1)
                self.assertEqual(sources[expected_path][0]["block"], 'print("hello")\n')
                self.assertEqual(sources[expected_path][0]["tags"], [])


class GetTangleSourcesTest(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.md_file_path = os.path.join(self.temp_dir.name, "test.md")

    def tearDown(self):
        self.temp_dir.cleanup()

    def create_md_file(self, content):
        with open(self.md_file_path, "w", encoding="utf8") as f:
            f.write(content)
        return self.md_file_path

    def test_basic_tangle(self):
        content = """
```python tangle:output.py
print("hello")
```
"""
        filename = self.create_md_file(content)
        sources = get_tangle_sources(filename, ",")
        expected_path = self.temp_dir.name + "/output.py"

        self.assertIn(expected_path, sources)
        self.assertEqual(len(sources[expected_path]), 1)
        self.assertEqual(sources[expected_path][0]["block"], 'print("hello")\n')
        self.assertEqual(sources[expected_path][0]["tags"], [])

    def test_multiple_locations(self):
        content = """
```python tangle:out1.py,out2.py
print("dual")
```
"""
        filename = self.create_md_file(content)
        sources = get_tangle_sources(filename, ",")
        path1 = self.temp_dir.name + "/out1.py"
        path2 = self.temp_dir.name + "/out2.py"

        self.assertIn(path1, sources)
        self.assertIn(path2, sources)
        self.assertEqual(sources[path1][0]["block"], 'print("dual")\n')
        self.assertEqual(sources[path2][0]["block"], 'print("dual")\n')

    def test_tags(self):
        content = """
```python tangle:out.py tags:tag1,tag2
print("tagged")
```
"""
        filename = self.create_md_file(content)
        sources = get_tangle_sources(filename, ",")
        path = self.temp_dir.name + "/out.py"

        self.assertEqual(sources[path][0]["tags"], ["tag1", "tag2"])

    def test_copy_source(self):
        content = """
<!-- TANGLE_CP:./assets/src.png tangle:dest.png tags:img -->
"""
        filename = self.create_md_file(content)
        sources = get_tangle_sources(filename, ",")
        path = self.temp_dir.name + "/dest.png"
        copy_source = self.temp_dir.name + "/assets/src.png"

        self.assertIn(path, sources)
        self.assertEqual(sources[path][0]["source"], copy_source)
        self.assertEqual(sources[path][0]["tags"], ["img"])

    def test_custom_separator(self):
        content = """
```python tangle:out1.py;out2.py tags:tag1;tag2
print("sep")
```
"""
        filename = self.create_md_file(content)
        sources = get_tangle_sources(filename, ";")
        path1 = self.temp_dir.name + "/out1.py"
        path2 = self.temp_dir.name + "/out2.py"

        self.assertIn(path1, sources)
        self.assertIn(path2, sources)
        self.assertEqual(sources[path1][0]["tags"], ["tag1", "tag2"])

    def test_multiple_blocks_same_file(self):
        content = """
```python tangle:out.py
block1
```

```python tangle:out.py
block2
```
"""
        filename = self.create_md_file(content)
        sources = get_tangle_sources(filename, ",")
        path = self.temp_dir.name + "/out.py"

        self.assertEqual(len(sources[path]), 2)
        self.assertEqual(sources[path][0]["block"], "block1\n")
        self.assertEqual(sources[path][1]["block"], "block2\n")

    def test_tildes_separator(self):
        content = """
~~~~python tangle:out.py
tildes
~~~~
"""
        filename = self.create_md_file(content)
        sources = get_tangle_sources(filename, ",")
        path = self.temp_dir.name + "/out.py"

        self.assertIn(path, sources)
        self.assertEqual(sources[path][0]["block"], "tildes\n")

    def test_indented_block(self):
        content = """
    ```python tangle:out.py
    print("indented")
    ```
"""
        filename = self.create_md_file(content)
        sources = get_tangle_sources(filename, ",")
        path = self.temp_dir.name + "/out.py"

        self.assertIn(path, sources)
        self.assertEqual(sources[path][0]["block"], '    print("indented")\n')

    def test_no_tangle_markers(self):
        content = """
# Header
Just some text.
```python
print("no tangle")
```
"""
        filename = self.create_md_file(content)
        sources = get_tangle_sources(filename, ",")
        self.assertEqual(sources, {})

    def test_absolute_output_path(self):
        abs_path = "/tmp/md_tangle_abs_test.txt"
        content = f"""
```python tangle:{abs_path}
absolute
```
"""
        filename = self.create_md_file(content)
        sources = get_tangle_sources(filename, ",")

        self.assertIn(abs_path, sources)
        self.assertEqual(sources[abs_path][0]["block"], "absolute\n")

    def test_empty_file(self):
        filename = self.create_md_file("")
        sources = get_tangle_sources(filename, ",")
        self.assertEqual(sources, {})

    def test_unclosed_block(self):
        content = """
```python tangle:out.py
unclosed
"""
        filename = self.create_md_file(content)
        sources = get_tangle_sources(filename, ",")
        path = self.temp_dir.name + "/out.py"

        self.assertIn(path, sources)
        self.assertEqual(sources[path][0]["block"], "unclosed\n")


if __name__ == "__main__":
    unittest.main()
