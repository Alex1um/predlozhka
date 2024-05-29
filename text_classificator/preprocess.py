"""
preprocess functions
"""
def preprocess(text: str) -> str:
    """
    Preprocesses the given text by converting it to lowercase, replacing newline characters with
    spaces, replacing tab characters with spaces, removing commas, and replacing parentheses with
    "( " and " )".
    
    Parameters:
        text (str): The input text to be preprocessed.
        
    Returns:
        str: The preprocessed text.
    """
    text = text.lower()
    text = text.replace("\n", " ")
    text = text.replace("\t", " ")
    text = text.replace(",", "")
    text = text.replace("(", "( ")
    text = text.replace(")", " )")
    return text
