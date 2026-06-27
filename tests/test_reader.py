import tempfile
import unittest
from pathlib import Path

from src.review_reader import ReviewReader


class ReviewReaderTest(unittest.TestCase):
    def test_reads_main_dataset(self):
        reviews = ReviewReader().read_csv("data/reviews.csv")
        self.assertGreaterEqual(len(reviews), 500)
        self.assertEqual({"蜜雪茶姬", "瑞巴克", "爷爷喜欢茶"}, {review.brand for review in reviews})

    def test_missing_label_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            path.write_text("review_id,date,brand,product,channel,content,rating\n1,d,b,p,c,text,5\n", encoding="utf-8")
            with self.assertRaises(ValueError):
                ReviewReader().read_csv(path)

    def test_invalid_label_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.csv"
            path.write_text(
                "review_id,date,brand,product,channel,content,rating,label\n1,d,b,p,c,text,5,开心\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValueError):
                ReviewReader().read_csv(path)


if __name__ == "__main__":
    unittest.main()
