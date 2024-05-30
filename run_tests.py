"""
runs tests
"""
import unittest
from tests.classificator import classification, vc
from tests.keywords import keywords
from tests.spam import spam


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
    suite.addTest(keywords.TestKeywordCheck("test_single_keyword"))
    suite.addTest(keywords.TestKeywordCheck("test_multiple_keywords"))
    suite.addTest(keywords.TestKeywordCheck("test_no_keywords"))
    suite.addTest(keywords.TestKeywordCheck("test_keywords_in_different_forms"))
    suite.addTest(keywords.TestKeywordCheck("test_case_insensitivity"))
    suite.addTest(keywords.TestKeywordCheck("test_partial_word_match"))
    suite.addTest(spam.TestSpamChecker("test_check_spam_no_spam"))
    suite.addTest(spam.TestSpamChecker("test_check_spam_with_spam"))
    suite.addTest(spam.TestSpamChecker("test_check_spam_with_spam_large"))
    suite.addTest(spam.TestSpamChecker("test_load_existing_vectorizer_and_matrix"))
    suite.addTest(spam.TestSpamChecker("test_save_and_load_vectorizer_and_matrix"))
    return suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(classificator_suit())
