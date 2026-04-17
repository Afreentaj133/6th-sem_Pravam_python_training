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
        'answers': 'answer', 'answering': 'answer', 'questions': 'question', 'asking': 'ask',
        'students': 'student', 'teachers': 'teacher', 'learning': 'learn', 'studying': 'study',
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


def evaluate_answer(reference_answer: str, student_answer: str) -> dict:
    ref_tokens = process_text(reference_answer)
    stud_tokens = process_text(student_answer)
    combined_corpus = [ref_tokens, stud_tokens]
    vocabulary = build_vocabulary(combined_corpus)
    ref_vec = vectorize(ref_tokens, vocabulary)
    stud_vec = vectorize(stud_tokens, vocabulary)
    similarity = cosine_similarity(ref_vec, stud_vec)
    score = similarity * 100  # Convert to percentage
    evaluation = 'Correct' if score >= 70 else 'Incorrect' if score < 50 else 'Partially Correct'
    return {
        'similarity': similarity,
        'score': score,
        'evaluation': evaluation,
        'ref_tokens': ref_tokens,
        'stud_tokens': stud_tokens,
    }


def main():
    # Example reference and student answers
    reference = """
    Photosynthesis is the process by which plants convert light energy into chemical energy.
    It occurs in the chloroplasts and involves chlorophyll absorbing sunlight.
    """

    student_correct = """
    Plants use photosynthesis to turn sunlight into chemical energy using chlorophyll in chloroplasts.
    """

    student_partial = """
    Photosynthesis helps plants make food from light.
    """

    student_wrong = """
    Animals eat plants to get energy through digestion.
    """

    print("Evaluating student answers:\n")

    for i, stud in enumerate([student_correct, student_partial, student_wrong], 1):
        result = evaluate_answer(reference, stud)
        print(f"Student Answer {i}:")
        print(f"  Similarity: {result['similarity']:.4f}")
        print(f"  Score: {result['score']:.1f}%")
        print(f"  Evaluation: {result['evaluation']}")
        print(f"  Reference tokens: {result['ref_tokens']}")
        print(f"  Student tokens: {result['stud_tokens']}")
        print()


if __name__ == '__main__':
    main()
