import unittest
from text_classificator.vcsub import create_texts_file, load_texts_file

class TestGettingTexts(unittest.TestCase):
    def test_create_small_file(self):
        texts = create_texts_file(["marketing"], 5, save=False)
        self.assertEqual(len(texts["marketing"]), 5)
    
    def test_create_big_file(self):
        texts = create_texts_file(["marketing"], 20, save=False)
        self.assertEqual(len(texts["marketing"]), 20)
    
    def test_saving_file(self):
        texts = create_texts_file(["marketing"], 5, save=True)
        texts2 = load_texts_file
        self.assertDictEqual(texts, texts2)
