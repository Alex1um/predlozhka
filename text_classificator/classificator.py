from os.path import getmtime
from time import time
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.linear_model import SGDClassifier
import numpy as np
import joblib

_cache_path = Path(__file__).parent.parent / "cache"
classificator_path = _cache_path / "classificator.pkl"


class Classificator:
    def __init__(self):
        """
        Initializes the Classificator object with a TfidfVectorizer, SVC, MultinomialNB, \
          and SGDClassifier models.
        Initializes self.pps with pipelines combining the vectorizer with each model.
        Initializes an empty set for classes and sets fitted_count to 0.
        """
        self.vectorizer = TfidfVectorizer()
        self.model = SVC(kernel="linear", probability=True)
        self.model2 = MultinomialNB()
        self.model3 = SGDClassifier(loss="modified_huber", penalty="l2")

        self.pps: tuple[Pipeline] = (
            make_pipeline(self.vectorizer, self.model),
            make_pipeline(self.vectorizer, self.model2),
            make_pipeline(self.vectorizer, self.model3),
        )

        self.classes = set()
        self.fitted_count = 0

    def fit(self, data: dict[str, list[str]]):
        """
        Fits the model to the given data.

        Parameters:
            data (dict[str, list[str]]): A dictionary containing the data to fit the model on. \
            The keys represent the labels, and the values are lists of texts.

        Returns:
            None
        """
        texts = []
        labels = []
        for k, v in data.items():
            texts.extend(v)
            l = len(v)
            labels.extend([k] * l)
            self.fitted_count += l

        self.classes |= set(labels)

        self.pps[0].fit(texts, labels)
        self.pps[1].fit(texts, labels)
        self.pps[2].fit(texts, labels)

    def partial_fit(self, data: dict[str, list[str]]):
        """
        Fits the model to a new batch of data, updating the model with the provided texts and labels.

        Parameters:
            data (dict[str, list[str]]): A dictionary containing the data to partially fit \
                  the model on. The keys represent the labels, and the values are lists of texts.

        Returns:
            None
        """
        texts = []
        labels = []
        for k, v in data.items():
            texts.extend(v)
            l = len(v)
            labels.extend([k] * l)
            self.fitted_count += l

        self.classes |= set(labels)

        self.model2.partial_fit(texts, labels, classes=np.array(data.keys()))
        self.model3.partial_fit(texts, labels, classes=np.array(data.keys()))

    def predict_proba(self, text: str) -> dict[str, tuple[float]]:
        """
        Predict the probabilities of each class for each model for the input text.

        Parameters:
            text (str): The input text to predict probabilities for.

        Returns:
            dict[str, tuple[float]]: A dictionary where the keys are class labels and \
                  the values are tuples of probabilities.
        """
        return {
            k: np.array(v)
            for k, *v in zip(
                self.pps[0].classes_,
                self.pps[0].predict_proba([text])[0],
                self.pps[1].predict_proba([text])[0],
                self.pps[2].predict_proba([text])[0],
            )
        }

    def predict_avgs(self, text: str) -> dict[str, float]:
        """
        Predicts the average probabilities of each class for the input text.

        Parameters:
            text (str): The input text to predict the average probabilities for.

        Returns:
            dict[str, float]: A dictionary where the keys are class labels and the \
                  values are the average probabilities.
        """
        return {
            k: np.average(v) for k, v in self.predict_proba(text).items()
        }

    def predict_max(self, text: str) -> tuple[str, float]:
        """
        Predicts the class with the highest average probability for the given text.

        Parameters:
            text (str): The input text to predict the class for.

        Returns:
            tuple[str, float]: A tuple containing the class label with the highest \
                  average probability and the probability value itself.
        """
        return max(tuple(self.predict_avgs(text).items()), key=lambda x: x[1])

    @classmethod
    def from_vcs(
        cls,
        subs: list[str] = [
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
        count: int = 30,
        remade: bool = False,
    ):
        """
        Creates a new instance of the class and fits it to the given data from VC.ru.

        Args:
            subs (list[str], optional): A list of subreddits to fetch data from. \
                  Defaults to ["marketing", "crypto", "tech", "flood", "dev", "design", \
                      "opinions", "ml", "tribuna"].
            count (int, optional): The number of texts to fetch from each subreddit. \
                  Defaults to 30.
            remade (bool, optional): Whether to recreate the texts file. Defaults to False.

        Returns:
            cls: A new instance of the class that has been fitted to the given data.
        """
        from .vcsub import create_or_load_texts
        texts = create_or_load_texts(subs, count, remade)
        cls = cls()
        cls.fit(texts)
        return cls

    def save(self):
        """
        Save the current instance of the class to a file.

        This function saves the current instance of the class to a file using joblib.dump(). \
              The saved file is in binary format.

        Parameters:
            self: The current instance of the class.

        Returns:
            None
        """
        with classificator_path.open("wb") as f:
            joblib.dump(self, f)

    @classmethod
    def load(self):
        """
        Loads the current instance of the class from a file in binary format.

        Parameters:
            self: The current instance of the class.

        Returns:
            The loaded instance of the class.
        """
        with classificator_path.open("rb") as f:
            return joblib.load(f)

    @classmethod
    def create_or_load(cls, subs: list[str], count: int):
        """
        A method to create or load an instance of the class based on certain conditions.

        Parameters:
            cls: The class itself.
            subs (list[str]): A list of substrings.
            count (int): An integer representing a count.

        Returns:
            An instance of the class based on the loading conditions.
        """
        if classificator_path.exists():
            loaded = cls.load()
            if loaded.fitted_count / len(loaded.classes) == count and set(subs) == loaded.classes and time() - getmtime(classificator_path) < 60 * 60 * 24 * 30:
                print("loaded")
                return loaded
        print("getting")
        cls = cls.from_vcs(subs, count)
        cls.save()
        return cls
