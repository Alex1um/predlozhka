import csv
import unittest
import tempfile
import shutil
import os

import numpy as np

from spam_checker.spam_checker import SpamChecker


class TestSpamChecker(unittest.TestCase):
    def setUp(self):
        # Создаем временную директорию
        self.test_dir = tempfile.mkdtemp()

        # Создаем временные файлы для сообщений и векторизатора
        self.messages_file = os.path.join(self.test_dir, 'messages.csv')
        self.vectorizer_file = os.path.join(self.test_dir, 'vectorizer.pkl')

        # Записываем тестовые сообщения в файл
        with open(self.messages_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Привет, как дела?"])
            writer.writerow(["Это тестовое сообщение."])
            writer.writerow(["Погода сегодня отличная."])
            writer.writerow(["Сооснователь OpenAI Илья Суцкевер объявил об уходе из компании"])

        # Создаем экземпляр SpamChecker
        self.spam_checker = SpamChecker(self.vectorizer_file, self.messages_file)

    def tearDown(self):
        # Удаляем временную директорию и все ее содержимое
        shutil.rmtree(self.test_dir)

    def test_check_spam_no_spam(self):
        new_messages = ["Сегодня хороший день для прогулки."]
        is_spam = self.spam_checker.check_spam(new_messages, threshold=0.8)
        self.assertFalse(is_spam["Сегодня хороший день для прогулки."])

    def test_check_spam_with_spam(self):
        new_messages = ["Это тестовое сообщение."]
        is_spam = self.spam_checker.check_spam(new_messages, threshold=0.8)
        self.assertTrue(is_spam["Это тестовое сообщение."])

    def test_check_spam_with_spam_large(self):
        new_messages = ["Илья Суцкевер, сооснователь OpenAI объявил, что уходит из компании"]
        is_spam = self.spam_checker.check_spam(new_messages, threshold=0.7)
        self.assertTrue(is_spam[new_messages[0]])

    def test_load_existing_vectorizer_and_matrix(self):
        self.assertTrue(os.path.exists(self.vectorizer_file))
        self.assertIsNotNone(self.spam_checker.vectorizer)
        self.assertIsNotNone(self.spam_checker.tfidf_matrix)

    def test_save_and_load_vectorizer_and_matrix(self):
        messages = self.spam_checker.read_messages_from_csv(self.messages_file)
        vectorizer = self.spam_checker.vectorizer
        tfidf_matrix = self.spam_checker.tfidf_matrix

        # Сохраняем векторизатор и матрицу
        self.spam_checker.save_vectorizer_and_matrix(vectorizer, tfidf_matrix, self.vectorizer_file)

        # Создаем новый экземпляр SpamChecker и загружаем векторизатор и матрицу
        new_spam_checker = SpamChecker(self.vectorizer_file, self.messages_file)
        new_vectorizer = new_spam_checker.vectorizer
        new_tfidf_matrix = new_spam_checker.tfidf_matrix

        self.assertTrue(np.array_equal(tfidf_matrix.toarray(), new_tfidf_matrix.toarray()))  # Проверка, что матрицы идентичны


if __name__ == '__main__':
    unittest.main()
