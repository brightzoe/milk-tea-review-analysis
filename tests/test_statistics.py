import unittest
import tempfile

from src.controller import SystemController


class StatisticsManagerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.summary = SystemController().run("data/reviews.csv", cls.tmp.name)

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


if __name__ == "__main__":
    unittest.main()
