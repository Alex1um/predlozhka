import unittest

from keywords_checker.keywords_checker import check_for_keywords


class TestKeywordCheck(unittest.TestCase):
    def test_single_keyword(self):
        text = "Привет"
        keywords = ["привет"]
        expected_result = {"привет": True}
        result = check_for_keywords(text, keywords)
        self.assertEqual(result, expected_result)

    def test_multiple_keywords(self):
        text = "Сегодня отличная погода"
        keywords = ["погода", "отличная"]
        expected_result = {"отличный": True, "погода": True}
        result = check_for_keywords(text, keywords)
        self.assertEqual(result, expected_result)

    def test_no_keywords(self):
        text = "Как насчет встречи на выходных"
        keywords = ["привет", "программирование"]
        expected_result = {word: False for word in keywords}
        result = check_for_keywords(text, keywords)
        self.assertEqual(result, expected_result)

    def test_keywords_in_different_forms(self):
        text = "Я люблю программировать"
        keywords = ["программирование", "программировать"]
        expected_result = {"программировать": True, "программирование": False}
        result = check_for_keywords(text, keywords)
        self.assertEqual(result, expected_result)

    def test_case_insensitivity(self):
        text = "Python это отличный язык программирования"
        keywords = ["python", "язык"]
        expected_result = {"python": True, "язык": True}
        result = check_for_keywords(text, keywords)
        self.assertEqual(result, expected_result)

    def test_partial_word_match(self):
        text = "Программирование на Python"
        keywords = ["программировать", "python"]
        expected_result = {"программировать": False, "python": True}
        result = check_for_keywords(text, keywords)
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()