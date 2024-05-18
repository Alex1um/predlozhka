import unittest
from unittest.mock import patch

from keywords_checker.keywords_checker import check_for_keywords


class TestKeywordCheck(unittest.TestCase):

    @patch('keywords_checker.keywords_checker.normalize_word')
    def test_single_keyword(self, mock_normalize_word):
        mock_normalize_word.side_effect = lambda x: x.lower()
        text = "Привет"
        keywords = ["привет"]
        expected_result = {"привет": True}
        result = check_for_keywords(text, keywords)
        self.assertEqual(result, expected_result)

    @patch('keywords_checker.keywords_checker.normalize_word')
    def test_multiple_keywords(self, mock_normalize_word):
        mock_normalize_word.side_effect = lambda x: x.lower()
        text = "Сегодня отличная погода"
        keywords = ["погода", "отличная"]
        expected_result = {"отличная": True, "погода": True}
        result = check_for_keywords(text, keywords)
        self.assertEqual(result, expected_result)

    @patch('keywords_checker.keywords_checker.normalize_word')
    def test_no_keywords(self, mock_normalize_word):
        mock_normalize_word.side_effect = lambda x: x.lower()
        text = "Как насчет встречи на выходных"
        keywords = ["привет", "программирование"]
        expected_result = {word: False for word in keywords}
        result = check_for_keywords(text, keywords)
        self.assertEqual(result, expected_result)

    @patch('keywords_checker.keywords_checker.normalize_word')
    def test_keywords_in_different_forms(self, mock_normalize_word):
        mock_normalize_word.side_effect = lambda x: {"люблю": "любить", "программировать": "программировать", "программирование": "программировать"}.get(x, x.lower())
        text = "Я люблю программировать"
        keywords = ["программирование"]
        expected_result = {"программировать": True}
        result = check_for_keywords(text, keywords)
        self.assertEqual(result, expected_result)

    @patch('keywords_checker.keywords_checker.normalize_word')
    def test_case_insensitivity(self, mock_normalize_word):
        mock_normalize_word.side_effect = lambda x: x.lower()
        text = "Python это отличный язык программирования"
        keywords = ["python", "язык"]
        expected_result = {"python": True, "язык": True}
        result = check_for_keywords(text, keywords)
        self.assertEqual(result, expected_result)

    @patch('keywords_checker.keywords_checker.normalize_word')
    def test_partial_word_match(self, mock_normalize_word):
        mock_normalize_word.side_effect = lambda x: {"программирование": "программировать", "программировать": "программирование"}.get(x, x.lower())
        text = "Программирование на Python"
        keywords = ["программировать", "python"]
        expected_result = {"программирование": True, "python": True}
        result = check_for_keywords(text, keywords)
        print(result)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()