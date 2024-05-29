"""
runs tests
"""
import unittest
from tests.classificator import classification, vc


def classificator_suit():
    """
    Generates a test suite for the classificator module.

    This function creates a test suite that includes tests for the `TestClassificator` class
    and the `TestGettingTexts` class. The tests included in the suite are:
    
    - `test_predictions` from the `TestClassificator` class.
    - `test_create_small_file` from the `TestGettingTexts` class.
    - `test_create_big_file` from the `TestGettingTexts` class.
    - `test_saving_file` from the `TestGettingTexts` class.

    Returns:
        unittest.TestSuite: The test suite containing the specified tests.
    """
    suite = unittest.TestSuite()
    suite.addTest(classification.TestClassificator("test_predictions"))
    suite.addTest(vc.TestGettingTexts("test_create_small_file"))
    suite.addTest(vc.TestGettingTexts("test_create_big_file"))
    suite.addTest(vc.TestGettingTexts("test_saving_file"))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(classificator_suit())
