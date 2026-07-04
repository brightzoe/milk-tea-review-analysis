import tempfile
import unittest
from pathlib import Path

from src.chart_generator import ChartGenerator
from src.controller import SystemController


class ChartGeneratorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.summary = SystemController().run("data/reviews.csv", cls.tmp.name, verbose=False)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_generates_png_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = ChartGenerator(tmp).generate_all(self.summary)
            self.assertEqual(3, len(paths))
            for path in paths:
                self.assertTrue(Path(path).exists())
                self.assertGreater(Path(path).stat().st_size, 0)


if __name__ == "__main__":
    unittest.main()
