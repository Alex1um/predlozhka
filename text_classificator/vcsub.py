"""
getting training texts module
"""
import re
import pickle
from pathlib import Path
from os.path import getmtime
from time import time
import requests
from text_classificator.preprocess import preprocess


USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64; rv:125.0) Gecko/20100101 Firefox/125.0"
API_TIMELINE = "https://api.vc.ru/v2.5/timeline"
_cache_path = Path(__file__).parent.parent / "cache"
sub_ids_file_path = _cache_path / "sub_ids.pkl"
texts_file_path = _cache_path / "texts.pkl"


def remove_html_tags(text):
    """
    Remove HTML tags from a given text.

    Args:
        text (str): The input text containing HTML tags.

    Returns:
        str: The text with HTML tags removed.

    This function uses regular expressions to remove HTML tags from a given text. It compiles a regular expression pattern
    to match any HTML tag and then uses the `re.sub()` function to replace all occurrences of the pattern with an
    empty string. The resulting text is returned.

    Example:
        >>> remove_html_tags("<p>Hello, <b>world</b>!</p>")
        'Hello, world!'
    """
    clean = re.compile("<.*?>")
    return re.sub(clean, "", text)


def get_timeline(session: requests.Session, ids, count: int = 50) -> str:
    """
    A function to get text from posts based on timeline(last posts from current time) in given subsite.

    Args:
        session (requests.Session): The session to use for making the API request.
        ids: The subsite ID to fetch the timeline for.
        count (int): The number of timeline items to retrieve (default is 100).

    Yields:
        str: The text content of each timeline item with HTML tags removed.
    """
    params = {"subsitesIds": ids} if ids is not None else None
    resp = session.get(API_TIMELINE, headers={
                       "User-Agent": USER_AGENT}, params=params)
    last_id = None
    last_sorting_value = None
    while count > 0 and resp.status_code == 200:
        json = resp.json()["result"]
        last_id = json["lastId"]
        last_sorting_value = json["lastSortingValue"]
        for item in json["items"]:
            s = ""
            for block in item["data"]["blocks"]:
                data = block["data"]
                text = data.get("text")
                if text:
                    s += preprocess(remove_html_tags(text)) + "\n"
            yield s
            count -= 1
            if count == 0:
                return
        resp = session.get(
            API_TIMELINE,
            headers={"User-Agent": USER_AGENT},
            params={
                "markdown": False,
                "lastId": last_id,
                "lastSortingValue": last_sorting_value,
                "subsitesIds": ids,
            },
        )


def get_topic_ids(session: requests.Session, topic: str) -> str:
    """
    Retrieves the ID of a topic from the VC.ru website using the provided session and topic.

    Args:
        session (requests.Session): The session to use for making the API request.
        topic (str): The topic to retrieve the ID for(in english as it is in url).

    Returns:
        str or None: The ID of the topic if found, None otherwise.

    Raises:
        None

    Examples:
        >>> session = requests.Session()
        >>> get_topic_ids(session, "news")
        '123456'
    """
    api_url = f"https://vc.ru/{topic}"

    page = session.get(api_url, headers={"User-Agent": USER_AGENT})
    begin = page.text.find(
        '<meta property="og:image" content="https://vc.ru/cover/fb/s/'
    )
    ids = None
    if begin != -1:
        begin += len('<meta property="og:image" content="https://vc.ru/cover/fb/s/')
        end = page.text.find("/", begin)
        ids = page.text[begin:end]
    return ids


def get_topic_posts(session: requests.Session, topic_id: str, count: int = 10):
    """
    Retrieves a tuple of posts from the given topic ID using the provided session.

    Args:
        session (requests.Session): The session to use for making the API request.
        topic_id (str): The ID of the topic to retrieve posts from.
        count (int, optional): The number of posts to retrieve. Defaults to 10.

    Returns:
        tuple: A tuple containing the retrieved posts.
    """
    return tuple(get_timeline(session, topic_id, count))


def create_texts_file(topicks: list[str], texts_count: int, save: bool = True) -> dict[str, list[str]]:
    """
    Creates a file containing texts for a list of topics.

    Args:
        topicks (list[str]): A list of topics.
        texts_count (int): The number of texts to retrieve for each topic.
        save (bool, optional): Whether to save the texts to a file. Defaults to True.

    Returns:
        dict[str, list[str]]: A dictionary containing the retrieved texts for each topic.

    Examples:
        >>> create_texts_file(["marketing", "tech"], 5)
        {'marketing': ['text1', 'text2', 'text3', 'text4', 'text5'], 'tech': ['text1', 'text2', 'text3', 'text4', 'text5']}
    """
    sub_ids = {}
    if sub_ids_file_path.exists():
        with sub_ids_file_path.open("rb") as f:
            sub_ids = pickle.load(f)
    texts = {}
    with requests.Session() as session:
        for topic in topicks:
            if topic not in sub_ids:
                sub_ids[topic] = get_topic_ids(session, topic)
            if sub_ids[topic] is None:
                continue
            texts[topic] = get_topic_posts(
                session, sub_ids[topic], count=texts_count)
        with sub_ids_file_path.open("wb") as f:
            pickle.dump(sub_ids, f)
        if save:
            with texts_file_path.open("wb") as f:
                pickle.dump((topicks, texts_count, texts), f)
    return texts


def create_or_load_texts(topicks: list[str], texts_count: int, recreate: bool = False) -> dict[str, list[str]]:
    """
    Creates or loads texts for a list of topics based on the provided parameters.
    Also updates the texts file if it is older than 30 days.

    Args:
        topicks (list[str]): A list of topics.
        texts_count (int): The number of texts to retrieve for each topic.
        recreate (bool, optional): Whether to recreate the texts file. Defaults to False.

    Returns:
        dict[str, list[str]]: A dictionary containing the retrieved texts for each topic.

    Examples:
        >>> create_or_load_texts(["marketing", "tech"], 5)
        {'marketing': ['text1', 'text2', 'text3', 'text4', 'text5'], 'tech': ['text1', 'text2', 'text3', 'text4', 'text5']}
    """
    if not recreate and texts_file_path.exists() and time() - getmtime(texts_file_path) < 60 * 60 * 24 * 30:
        with texts_file_path.open("rb") as f:
            old_topicks, old_texts_count, old_texts = pickle.load(f)
        if old_topicks == topicks and old_texts_count == texts_count:
            return old_texts
    return create_texts_file(topicks, texts_count)


def load_texts_file() -> dict[str, list[str]]:
    """
    Loads and returns the texts stored in a file.
    """
    with texts_file_path.open("rb") as f:
        _, _, texts = pickle.load(f)
        return texts
