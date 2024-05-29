import unittest
from text_classificator.classificator import Classificator
from tests.classificator import texts


class TestClassificator(unittest.TestCase):
    classificator = Classificator.create_or_load(
        [
            "marketing",
            "crypto",
            "tech",
            "flood",
            "dev",
            "design",
            "opinions",
            "ml",
            "tribuna",
        ],
        50,
    )

    def test_predictions(self):
        for n, v in vars(texts).items():
            if n.startswith("_"):
                continue
            _, probability = self.classificator.predict_max(v)
            self.assertGreaterEqual(probability, 0.2)


if __name__ == "__main__":
    unittest.main()
