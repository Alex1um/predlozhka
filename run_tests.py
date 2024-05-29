import unittest
from tests.classificator import classification, vc


def classificator_suit():
    suite = unittest.TestSuite()
    suite.addTest(classification.TestClassificator("test_predictions"))
    suite.addTest(vc.TestGettingTexts("test_create_small_file"))
    suite.addTest(vc.TestGettingTexts("test_create_big_file"))
    suite.addTest(vc.TestGettingTexts("test_saving_file"))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(classificator_suit())
