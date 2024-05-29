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
    clas, prob = classificator.predict_max(text)
    return translated.get(clas, "Неизвестно"), prob
