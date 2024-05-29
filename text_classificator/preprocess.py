def preprocess(text: str) -> str:
    text = text.lower()
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace(",", "")
    text = text.replace("(", "( ")
    text = text.replace(")", " )")
    return text
