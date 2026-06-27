import unittest

from src.text_cleaner import TextCleaner


class TextCleanerTest(unittest.TestCase):
    def test_clean_removes_punctuation(self):
        self.assertEqual(TextCleaner().clean("奶茶！！！ 很好喝。"), "奶茶 很好喝")

    def test_extracts_keywords(self):
        cleaner = TextCleaner(vocabulary={"太甜", "等很久", "包装漏"})
        tokens = cleaner.extract_tokens("这杯太甜了，等很久，而且包装漏了")
        self.assertIn("太甜", tokens)
        self.assertIn("等很久", tokens)
        self.assertIn("包装漏", tokens)


if __name__ == "__main__":
    unittest.main()
