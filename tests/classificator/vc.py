"""
text getter tests
"""
import unittest
from text_classificator.vcsub import create_texts_file, load_texts_file


class TestGettingTexts(unittest.TestCase):
    """
    text getter tests
    """
    def test_create_small_file(self):
        """
        Test case to verify the functionality of the `test_create_small_file` method.

        This test case checks if the `create_texts_file` function correctly creates a file
        containing a small number of texts for the "marketing" topic. The `create_texts_file`
        function is called with the parameters `["marketing"]` to specify the topic,
        `5` to specify the number of texts, and `save=False` to indicate that the file should not
        be saved.

        The test asserts that the length of the "marketing" key in the `texts` dictionary is
        equal to 5. This ensures that the correct number of texts are generated for the specified
        topic.

        This test case is part of the `TestGettingTexts` test class.

        Parameters:
            self: The instance of the test class.

        Returns:
            None
        """
        texts = create_texts_file(["marketing"], 5, save=False)
        self.assertEqual(len(texts["marketing"]), 5)

    def test_create_big_file(self):
        """
        Test case to verify the functionality of the `test_create_big_file` method.

        This test case checks if the `create_texts_file` function correctly creates a file
        containing a large number of texts for the "marketing" topic. The `create_texts_file`
        function is called with the parameters `["marketing"]` to specify the topic,
        `20` to specify the number of texts, and `save=False` to indicate that the file should
        not be saved.

        The test asserts that the length of the "marketing" key in the `texts` dictionary is
        equal to 20. This ensures that the correct number of texts are generated for the
        specified topic.

        Parameters:
            self: The instance of the test class.

        Returns:
            None
        """
        texts = create_texts_file(["marketing"], 20, save=False)
        self.assertEqual(len(texts["marketing"]), 20)

    def test_saving_file(self):
        """
        Test case to verify the functionality of the `test_saving_file` method.

        This test case checks if the `create_texts_file` function correctly saves and loads a
        file containing a small number of texts for the "marketing" topic. The
        `create_texts_file` function is called with the parameters `["marketing"]` to specify the
        topic, `5` to specify the number of texts, and `save=True` to indicate that the file
        should be saved. The saved file is then loaded using the `load_texts_file` function. The
        test asserts that the loaded texts are equal to the original texts.

        Parameters:
            self: The instance of the test class.

        Returns:
            None
        """
        texts = create_texts_file(["marketing"], 5, save=True)
        texts2 = load_texts_file()
        self.assertDictEqual(texts, texts2)


if __name__ == "__main__":
    unittest.main()
