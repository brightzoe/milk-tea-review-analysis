import unittest

from src.sentiment_analyzer import SentimentAnalyzer
from src.sentiment_lexicon import SentimentLexicon


class SentimentAnalyzerTest(unittest.TestCase):
    def setUp(self):
        self.analyzer = SentimentAnalyzer(SentimentLexicon())

    def test_positive(self):
        label = self.analyzer.classify(self.analyzer.calculate_score(["好喝", "实惠"]))
        self.assertEqual(label, "正面")

    def test_negative(self):
        label = self.analyzer.classify(self.analyzer.calculate_score(["太甜", "贵"]))
        self.assertEqual(label, "负面")

    def test_neutral(self):
        label = self.analyzer.classify(self.analyzer.calculate_score(["味道还可以"]))
        self.assertEqual(label, "中性")

    def test_negation_not_obviously_negative(self):
        label = self.analyzer.classify(self.analyzer.calculate_score(["不", "难喝"]))
        self.assertNotEqual(label, "负面")


if __name__ == "__main__":
    unittest.main()
