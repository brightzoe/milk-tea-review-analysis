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

    def test_ignores_brand_terms_when_extracting_review_tokens(self):
        cleaner = TextCleaner(vocabulary={"爷爷喜欢茶", "喜欢", "一般"})
        tokens = cleaner.extract_tokens_for_review("爷爷喜欢茶的柠檬茶味道一般", ["爷爷喜欢茶", "柠檬茶"])
        self.assertNotIn("爷爷喜欢茶", tokens)
        self.assertNotIn("喜欢", tokens)
        self.assertIn("一般", tokens)

    def test_keeps_real_sentiment_after_ignoring_brand(self):
        cleaner = TextCleaner(vocabulary={"爷爷喜欢茶", "喜欢", "好喝"})
        tokens = cleaner.extract_tokens_for_review("爷爷喜欢茶这杯真的好喝，我喜欢", ["爷爷喜欢茶", "柠檬茶"])
        self.assertNotIn("爷爷喜欢茶", tokens)
        self.assertIn("好喝", tokens)
        self.assertIn("喜欢", tokens)

    def test_prefers_longer_non_overlapping_keyword(self):
        cleaner = TextCleaner(vocabulary={"细腻", "腻"})
        tokens = cleaner.extract_tokens("奶盖很细腻")
        self.assertIn("细腻", tokens)
        self.assertNotIn("腻", tokens)


if __name__ == "__main__":
    unittest.main()
