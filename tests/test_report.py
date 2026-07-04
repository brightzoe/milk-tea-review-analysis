import tempfile
import unittest
from pathlib import Path

from src.controller import SystemController
from src.report_exporter import ReportExporter
from src.review_reader import ReviewReader
from src.statistics_manager import StatisticsManager


class ReportExporterTest(unittest.TestCase):
    def test_controller_generates_outputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            SystemController().run("data/reviews.csv", tmp, verbose=False)
            output = Path(tmp)
            report = output / "analysis_report.md"
            csv_file = output / "analyzed_reviews.csv"
            model_file = output / "sentiment_model.pkl"
            self.assertTrue(report.exists())
            self.assertTrue(csv_file.exists())
            self.assertTrue(model_file.exists())
            self.assertGreater(model_file.stat().st_size, 0)
            text = report.read_text(encoding="utf-8")
            self.assertIn("sklearn", text)
            self.assertIn("charts/sentiment_distribution.png", text)
            csv_text = csv_file.read_text(encoding="utf-8-sig")
            self.assertIn("rule_sentiment_label", csv_text)
            self.assertIn("ml_sentiment_label", csv_text)


if __name__ == "__main__":
    unittest.main()
