import math
import re
from collections import Counter

STOP_WORDS = {
    'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', 'as', 'at',
    'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', 'could', 'did', 'do',
    'does', 'doing', 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', 'has', 'have', 'having',
    'he', 'her', 'here', 'hers', 'herself', 'him', 'himself', 'his', 'how', 'i', 'if', 'in', 'into', 'is',
    'it', 'its', 'itself', 'let', 'me', 'more', 'most', 'my', 'myself', 'nor', 'of', 'off', 'on', 'once', 'only',
    'or', 'other', 'ought', 'our', 'ours', 'ourselves', 'out', 'over', 'own', 'same', 'she', 'should', 'so', 'some',
    'such', 'than', 'that', 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', 'these', 'they',
    'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', 'we', 'were', 'what',
    'when', 'where', 'which', 'while', 'who', 'whom', 'why', 'will', 'with', 'you', 'your', 'yours', 'yourself',
    'yourselves'
}


def clean_text(text: str) -> str:
    text = re.sub(r'<.*?>', ' ', text)
    text = re.sub(r'http\S+|www\.[^\s]+', ' ', text)
    text = re.sub(r'[^a-zA-Z\s]', ' ', text)
    text = text.lower()
    return re.sub(r'\s+', ' ', text).strip()


def tokenize(text: str) -> list[str]:
    return [word for word in text.split() if word]


def remove_stop_words(tokens: list[str]) -> list[str]:
    return [token for token in tokens if token not in STOP_WORDS]


def simple_lemmatize(token: str) -> str:
    lemma_map = {
        'went': 'go', 'gone': 'go', 'bought': 'buy', 'brought': 'bring', 'sent': 'send',
        'received': 'receive', 'running': 'run', 'meeting': 'meet', 'paid': 'pay', 'using': 'use',
        'claims': 'claim', 'says': 'say', 'saying': 'say', 'reported': 'report',
        'published': 'publish', 'reached': 'reach', 'reveals': 'reveal', 'revealed': 'reveal',
        'warns': 'warn', 'warned': 'warn', 'alleges': 'allege', 'alleged': 'allege',
    }
    if token in lemma_map:
        return lemma_map[token]
    if token.endswith('ies') and len(token) > 4:
        return token[:-3] + 'y'
    if token.endswith('ves') and len(token) > 4:
        return token[:-3] + 'f'
    if token.endswith('ing') and len(token) > 5:
        return token[:-3]
    if token.endswith('ed') and len(token) > 4:
        base = token[:-2]
        if base.endswith('i'):
            return base[:-1] + 'y'
        return base
    if token.endswith('s') and len(token) > 3:
        return token[:-1]
    return token


def process_text(text: str) -> list[str]:
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    tokens = remove_stop_words(tokens)
    return [simple_lemmatize(token) for token in tokens]


def build_vocabulary(corpus: list[list[str]]) -> dict[str, int]:
    all_tokens = [token for tokens in corpus for token in tokens]
    frequency = Counter(all_tokens)
    return {token: idx for idx, (token, _) in enumerate(sorted(frequency.items()))}


def vectorize(tokens: list[str], vocabulary: dict[str, int]) -> list[float]:
    vector = [0.0] * len(vocabulary)
    counts = Counter(tokens)
    for token, count in counts.items():
        if token in vocabulary:
            vector[vocabulary[token]] = float(count)
    return vector


def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a ** 2 for a in vec1))
    norm2 = math.sqrt(sum(b ** 2 for b in vec2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot_product / (norm1 * norm2)


def compute_similarity(text1: str, text2: str) -> float:
    tokens1 = process_text(text1)
    tokens2 = process_text(text2)
    combined_corpus = [tokens1, tokens2]
    vocabulary = build_vocabulary(combined_corpus)
    vec1 = vectorize(tokens1, vocabulary)
    vec2 = vectorize(tokens2, vocabulary)
    return cosine_similarity(vec1, vec2)


def main():
    # Example documents
    doc1 = """
    The quick brown fox jumps over the lazy dog. This is a classic pangram used in typing tests.
    It contains every letter of the alphabet at least once.
    """

    doc2 = """
    A fast brown fox leaps over a sleepy dog. This sentence is also a pangram.
    It includes all letters from A to Z.
    """

    similarity = compute_similarity(doc1, doc2)
    print(f"Similarity between documents: {similarity:.4f}")

    # Another example
    doc3 = """
    Machine learning is a subset of artificial intelligence. It involves training algorithms on data.
    """

    doc4 = """
    Artificial intelligence encompasses machine learning. Algorithms learn from datasets.
    """

    similarity2 = compute_similarity(doc3, doc4)
    print(f"Similarity between ML docs: {similarity2:.4f}")


if __name__ == '__main__':
    main()
