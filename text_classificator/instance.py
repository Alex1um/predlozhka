"""
classificator instance for project uses
"""
from text_classificator.classificator import Classificator

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
