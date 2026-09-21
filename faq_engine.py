import re

MATCH_THRESHOLD = 0.2

# Наивный стеммер: отсекает частые окончания русских слов, чтобы
# "треки"/"треков", "приз"/"призы", "какой"/"какие" считались одним токеном.
_SUFFIXES = sorted(
    [
        "ими", "ыми", "ого", "его", "ому", "ему",
        "ая", "яя", "ое", "ее", "ие", "ые", "ов", "ев", "ей",
        "ям", "ам", "ом", "ем", "ах", "ях", "ой", "ый", "ий",
        "а", "я", "ы", "и", "о", "е", "й", "ь", "у", "ю",
    ],
    key=len,
    reverse=True,
)


def _stem(word):
    for suffix in _SUFFIXES:
        if word.endswith(suffix) and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


# Служебные слова без смысловой нагрузки — исключаются до сравнения,
# иначе после стемминга "как"/"какой"/"какая"/"какие" схлопываются
# в один общий токен и ложно совпадают с любым вопросом на "как...".
_STOPWORDS = {
    "как", "какой", "какая", "какие", "какое",
    "что", "чем", "когда", "где", "почему", "зачем",
    "сколько", "можно", "нужно", "надо", "есть", "будет",
    "ли", "на", "в", "с", "со", "у", "к", "о", "об", "от", "за", "из",
    "для", "по", "до", "это", "а", "и", "но", "или", "не", "ну",
}


def tokenize(text):
    words = re.findall(r"[а-яёa-z0-9]+", text.lower())
    return {_stem(w) for w in words if w not in _STOPWORDS}


def load_faq(path="faq.txt"):
    with open(path, encoding="utf-8") as f:
        content = f.read()

    pairs = []
    for block in content.split("\n\n"):
        block = block.strip()
        if not block:
            continue
        question, answer = "", ""
        for line in block.splitlines():
            if line.startswith("Q:"):
                question = line[2:].strip()
            elif line.startswith("A:"):
                answer = line[2:].strip()
        if question and answer:
            pairs.append((question, answer))
    return pairs


def find_answer(user_question, faq):
    user_tokens = tokenize(user_question)
    if not user_tokens:
        return None

    best_score, best_answer = 0.0, None
    for question, answer in faq:
        faq_tokens = tokenize(question)
        if not faq_tokens:
            continue
        score = len(user_tokens & faq_tokens) / len(user_tokens | faq_tokens)
        if score > best_score:
            best_score, best_answer = score, answer

    return best_answer if best_score >= MATCH_THRESHOLD else None
