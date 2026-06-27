import unittest

from src.ml_classifier import SklearnSentimentClassifier
from src.review_reader import ReviewReader


class MLClassifierTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.reviews = ReviewReader().read_csv("data/reviews.csv")

    def test_train_and_predict(self):
        clf = SklearnSentimentClassifier()
        clf.train(self.reviews)
        self.assertIn(clf.predict("这杯奶茶太甜了"), {"正面", "中性", "负面"})

    def test_evaluate_returns_metrics(self):
        metrics = SklearnSentimentClassifier().evaluate(self.reviews)
        self.assertIn("accuracy", metrics)
        self.assertIn("classification_report", metrics)


if __name__ == "__main__":
    unittest.main()
