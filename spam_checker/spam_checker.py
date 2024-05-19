import csv
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os


class SpamChecker:
    def __init__(self, vectorizer_file, messages_file):
        self.messages_file = messages_file
        self.vectorizer_file = vectorizer_file
        self.messages = self.read_messages_from_csv(self.messages_file)
        if os.path.exists(self.vectorizer_file):
            self.vectorizer, self.tfidf_matrix = self.load_vectorizer_and_matrix(self.vectorizer_file)
        else:
            self.vectorizer = TfidfVectorizer()
            self.tfidf_matrix = self.vectorizer.fit_transform(self.messages)
            self.save_vectorizer_and_matrix(self.vectorizer, self.tfidf_matrix, self.vectorizer_file)

    # Функция для чтения сообщений из .csv файла
    def read_messages_from_csv(self, filename):
        messages = []
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                messages.append(row[0])
        return messages

    # Сохранение и загрузка объектов с использованием joblib
    def save_vectorizer_and_matrix(self, vectorizer, matrix, filename):
        joblib.dump((vectorizer, matrix), filename)

    def load_vectorizer_and_matrix(self, filename):
        return joblib.load(filename)

    def check_spam(self, new_messages: list, threshold=0.8):
        # Проверка новых сообщений поочередно
        for new_message in new_messages:
            # Преобразование нового сообщения в TF-IDF вектор
            new_message_tfidf = self.vectorizer.transform([new_message])

            # Вычисление косинусного сходства между новым сообщением и уже имеющимися
            cosine_similarities = cosine_similarity(new_message_tfidf, self.tfidf_matrix)

            is_spam = dict()
            if any(similarity > threshold for similarity in cosine_similarities[0]):
                is_spam[new_message] = True
            else:
                is_spam[new_message] = False
                # Добавление нового сообщения в список сообщений
                self.messages.append(new_message)
                # Обновление TF-IDF матрицы
                self.tfidf_matrix = self.vectorizer.fit_transform(self.messages)
                # Сохранение обновленного векторизатора и матрицы
                self.save_vectorizer_and_matrix(self.vectorizer, self.tfidf_matrix, self.vectorizer_file)
                # Сохранение обновленного списка сообщений в .csv файл
                with open(self.messages_file, 'a', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([new_message])
            return is_spam