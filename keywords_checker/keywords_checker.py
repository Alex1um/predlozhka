from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, Doc

# Инициализация компонентов Natasha
segmenter = Segmenter()
morph_vocab = MorphVocab()
emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)


# Функция для нормализации слов
def normalize_word(word):
    doc = Doc(word)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    for token in doc.tokens:
        token.lemmatize(morph_vocab)
    return doc.tokens[0].lemma


def check_for_keywords(text, keywords):
    # Нормализуем текст
    normalized_text = [normalize_word(word) for word in text.split()]
    # Нормализуем ключевые слова
    normalized_keywords = [normalize_word(word) for word in keywords]
    return {keyword: keyword in normalized_text for keyword in normalized_keywords}
