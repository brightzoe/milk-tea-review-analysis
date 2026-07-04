import unittest
import tempfile

from src.controller import SystemController
from src.statistics_manager import StatisticsManager


class StatisticsManagerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.summary = SystemController().run("data/reviews.csv", cls.tmp.name, verbose=False)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_brand_counts(self):
        self.assertEqual(3, len(self.summary.brand_reports))
        self.assertTrue(all(report.total_count >= 160 for report in self.summary.brand_reports))

    def test_sentiment_counts_sum(self):
        self.assertEqual(self.summary.total_count, sum(self.summary.sentiment_counts.values()))

    def test_problem_ranking_present(self):
        self.assertTrue(self.summary.problem_counts)

    def test_consistency_rates_present(self):
        self.assertIn("规则模型", self.summary.consistency_rates)
        self.assertIn("机器学习模型", self.summary.consistency_rates)
        self.assertIn("评分映射", self.summary.consistency_rates)
        self.assertTrue(all(0 <= rate <= 1 for rate in self.summary.consistency_rates.values()))

    def test_rating_to_label(self):
        manager = StatisticsManager()
        self.assertEqual("正面", manager.rating_to_label(5))
        self.assertEqual("正面", manager.rating_to_label(4))
        self.assertEqual("中性", manager.rating_to_label(3))
        self.assertEqual("负面", manager.rating_to_label(2))
        self.assertEqual("负面", manager.rating_to_label(1))


if __name__ == "__main__":
    unittest.main()
