import unittest

from src.models import Review
from src.problem_analyzer import ProblemAnalyzer


class ProblemAnalyzerTest(unittest.TestCase):
    def test_multiple_categories(self):
        categories = ProblemAnalyzer().match_problem_categories("太甜了，包装漏了，等很久")
        self.assertIn("口味问题", categories)
        self.assertIn("包装问题", categories)
        self.assertIn("出餐问题", categories)

    def test_positive_review_has_no_problem(self):
        review = Review("1", "d", "b", "p", "c", "好喝又实惠", 5, "正面", rule_sentiment_label="正面")
        ProblemAnalyzer().analyze(review)
        self.assertEqual([], review.problem_categories)

    def test_token_based_matching_avoids_substring_false_positive(self):
        categories = ProblemAnalyzer().match_problem_categories("奶盖很细腻", ["细腻"])
        self.assertNotIn("口味问题", categories)


if __name__ == "__main__":
    unittest.main()
