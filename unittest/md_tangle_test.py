import unittest
from md_tangle import contains_code_block_separators, get_save_location, map_md_to_code_blocks

filename = "test.py"
valid_tangle_block = f"  ```javascript tangle:{filename} random"
invalid_tangle_block = "```javascript"


class TestPatternMatchers(unittest.TestCase):

    def test_contains_code_block_separators(self):
        self.assertTrue(contains_code_block_separators(valid_tangle_block))
        self.assertTrue(contains_code_block_separators("  ```"))
        self.assertTrue(contains_code_block_separators("  ~~~~"))
        self.assertFalse(contains_code_block_separators("```inline````"))
        self.assertFalse(contains_code_block_separators("Text ```"))
        self.assertFalse(contains_code_block_separators("Text ~~~~"))

    def test_get_save_location(self):
        self.assertEqual(get_save_location(valid_tangle_block), filename)
        self.assertEqual(get_save_location(invalid_tangle_block), None)

    def test_map_md_to_code_blocks(self):
        code_blocks = map_md_to_code_blocks("example.md")
        self.assertTrue("test.css" in code_blocks.keys())
        self.assertTrue("test.js" in code_blocks.keys())
        self.assertEqual(len(code_blocks["test.css"].splitlines()), 8)
        self.assertEqual(len(code_blocks["test.js"].splitlines()), 2)


if __name__ == '__main__':
    unittest.main()
