"""
classificator instance for project uses
"""
from spam_checker.spam_checker import SpamChecker
from text_classificator.classificator import Classificator
from keywords_checker.keywords_checker import check_for_keywords

classificator = Classificator.create_or_load(
    [
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
    50,
)

translated = {
    "marketing": "Маркетинг",
    "crypto": "Криптовалюта",
    "tech": "Технологии",
    "flood": "Оффтоп",
    "dev": "Разработка",
    "design": "Дизайн",
    "opinions": "Мнения",
    "ml": "Машинное обучение",
    "tribuna": "Реклама/Продвижение",
}

spam_checker = SpamChecker('cache/vectorizer.pkl', 'cache/messages.csv')


def get_translated(text):
    """
    Predicts the class and probability of the given text using the `Classificator` object's
    `predict_max` method.
    
    Args:
        text (str): The input text to predict the class and probability for.
        
    Returns: tuple[str, float]: A tuple containing the translated class label (or "Неизвестно" if
    not found) and the probability value.
    """
    clas, prob = classificator.predict_max(text)
    return translated.get(clas, "Неизвестно"), prob


def get_spam_msg(text):
    is_spam = spam_checker.check_spam([text])
    if is_spam[text]:
        return 'Текст публикации был помечен как спам'
    else:
        return 'Спам в этой публикации не был обнаружен'


keywords = [
    'программирование',
    'политика',
    'чечня',
    'америка',
    'Казаков'
]


def get_keywords_msg(text):
    result = check_for_keywords(text, keywords)
    if any(result.values()):
        message = 'Были обнаружены следующие ключевые слова: '
        for key, val in result:
            if val:
                message += f'{key} '
        return message
    else:
        return 'Ключевые слова обнаружены не были'