"""
classificator tests
"""
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
        """
        Test the predictions made by the classifier.

        This function iterates over the variables in the `texts` module and checks if each variable starts with an underscore. If it does not, it predicts the maximum probability for the variable using the `predict_max` method of the `classificator` object. The predicted probability is then compared with 0.2 using the `assertGreaterEqual` method of the `unittest.TestCase` class.

        Parameters:
            self (TestClassificator): The instance of the test class.

        Returns:
            None
        """
        for n, v in vars(texts).items():
            if n.startswith("_"):
                continue
            _, probability = self.classificator.predict_max(v)
            self.assertGreaterEqual(probability, 0.2)


if __name__ == "__main__":
    unittest.main()
