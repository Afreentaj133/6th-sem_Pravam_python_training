import math
import random
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

POSITIVE_WORDS = {
    'truth', 'safe', 'official', 'verified', 'clear', 'strong', 'win', 'gain', 'successful', 'confirmed',
    'legitimate', 'trust', 'trusted', 'secure', 'authorized', 'accurate', 'positive', 'real', 'fact', 'support',
}

NEGATIVE_WORDS = {
    'fake', 'scam', 'danger', 'urgent', 'exclusive', 'secret', 'shock', 'explosive', 'conspiracy', 'hoax',
    'claim', 'rumor', 'unverified', 'alleged', 'warn', 'alert', 'threat', 'risk', 'ban', 'banish', 'notorious',
}

NEWS_ITEMS = [
    (0, "Government releases official budget report showing strong growth and stable markets."),
    (0, "Local university researchers publish peer-reviewed study on renewable energy."),
    (0, "City council approves funding for public health services and community outreach programs."),
    (0, "National sports team wins championship after a well-deserved season of hard work."),
    (0, "Company announces verified product recall due to safety concerns and customer protection."),
    (0, "International diplomats reach an agreement to reduce trade barriers and increase cooperation."),
    (0, "Weather service confirms official warnings for heavy rain and flooding in the region."),
    (0, "Tech company launches a new security feature that protects user accounts from unauthorized access."),
    (0, "Scientists publish accurate climate data showing gradual temperature trends."),
    (0, "Elections proceed with verified results and independent observers report fair procedures."),
    (1, "Breaking: Secret government experiment causes massive health alarm in the city."),
    (1, "Shocking video reveals celebrity betrayal and hidden conspiracy plans."),
    (1, "Urgent alert: Alien invasion confirmed by insiders, prepare your emergency kits now!"),
    (1, "Exclusive report claims that miracle cure can reverse aging overnight."),
    (1, "Fake news site says politician is secretly controlled by shadow bankers."),
    (1, "This secret weight loss trick is banned by doctors but still works for everyone."),
    (1, "Unverified rumor: Major bank will collapse next week and wipe out savings."),
    (1, "Scam alert: Send money now or lose your account forever, this is not a drill."),
    (1, "Conspiracy theory alleges that the election was rigged by foreign agents."),
    (1, "Hoax story claims that drinking vinegar cures all diseases instantly."),
]


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


def simple_stem(token: str) -> str:
    if len(token) <= 3:
        return token
    if token.endswith('ies'):
        return token[:-3] + 'y'
    if token.endswith('sses') or token.endswith('shes') or token.endswith('ches'):
        return token[:-2]
    if token.endswith('s') and not token.endswith('ss'):
        return token[:-1]
    if token.endswith('ing') and len(token) > 5:
        return token[:-3]
    if token.endswith('ed') and len(token) > 4:
        return token[:-2]
    return token


def simple_lemmatize(token: str) -> str:
    lemma_map = {
        'claims': 'claim', 'claims': 'claim', 'says': 'say', 'saying': 'say', 'reported': 'report',
        'reported': 'report', 'published': 'publish', 'reached': 'reach', 'reveals': 'reveal',
        'revealed': 'reveal', 'warns': 'warn', 'warned': 'warn', 'alleges': 'allege', 'alleged': 'allege',
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


def sentiment_polarity(tokens: list[str]) -> float:
    positive = sum(1 for token in tokens if token in POSITIVE_WORDS)
    negative = sum(1 for token in tokens if token in NEGATIVE_WORDS)
    if not tokens:
        return 0.0
    raw_score = (positive - negative) / len(tokens)
    # Shift polarity into a non-negative feature range for BoW + sentiment modeling
    return (raw_score + 1.0) * 5.0


def process_text(text: str, mode: str) -> list[str]:
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    tokens = remove_stop_words(tokens)
    if mode == 'stem':
        return [simple_stem(token) for token in tokens]
    if mode == 'lemma':
        return [simple_lemmatize(token) for token in tokens]
    return tokens


def build_vocabulary(corpus: list[list[str]], min_freq: int = 1) -> dict[str, int]:
    frequency = Counter(token for tokens in corpus for token in tokens)
    return {
        token: idx
        for idx, (token, count) in enumerate(sorted(frequency.items()))
        if count >= min_freq
    }


def vectorize(corpus: list[list[str]], vocabulary: dict[str, int]) -> list[list[float]]:
    vectors = []
    for tokens in corpus:
        vector = [0.0] * (len(vocabulary) + 1)
        counts = Counter(tokens)
        for token, count in counts.items():
            if token in vocabulary:
                vector[vocabulary[token]] = float(count)
        vector[-1] = sentiment_polarity(tokens)
        vectors.append(vector)
    return vectors


def train_naive_bayes(X: list[list[float]], y: list[int], alpha: float = 1.0) -> dict:
    class_counts = Counter(y)
    feature_counts = {label: [0.0] * len(X[0]) for label in class_counts}
    total_tokens = {label: 0.0 for label in class_counts}

    for vector, label in zip(X, y):
        for idx, value in enumerate(vector):
            feature_counts[label][idx] += value
            total_tokens[label] += value

    vocab_size = len(X[0])
    model = {
        'priors': {label: class_counts[label] / len(y) for label in class_counts},
        'cond_prob': {},
    }
    for label in class_counts:
        model['cond_prob'][label] = [
            (feature_counts[label][idx] + alpha) / (total_tokens[label] + alpha * vocab_size)
            for idx in range(vocab_size)
        ]
    return model


def predict_naive_bayes(model: dict, X: list[list[float]]) -> list[int]:
    predictions = []
    for vector in X:
        scores = {}
        for label, prior in model['priors'].items():
            score = math.log(prior)
            for idx, value in enumerate(vector):
                if value != 0.0:
                    score += value * math.log(model['cond_prob'][label][idx])
            scores[label] = score
        predictions.append(max(scores, key=scores.get))
    return predictions


def accuracy_score(true: list[int], predictions: list[int]) -> float:
    return sum(1 for actual, predicted in zip(true, predictions) if actual == predicted) / len(true)


def classification_report(true: list[int], predictions: list[int]) -> dict[str, float]:
    tp = sum(1 for t, p in zip(true, predictions) if t == 1 and p == 1)
    tn = sum(1 for t, p in zip(true, predictions) if t == 0 and p == 0)
    fp = sum(1 for t, p in zip(true, predictions) if t == 0 and p == 1)
    fn = sum(1 for t, p in zip(true, predictions) if t == 1 and p == 0)
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        'accuracy': accuracy_score(true, predictions),
        'precision': precision,
        'recall': recall,
        'f1': f1,
    }


def split_dataset(data: list[tuple[int, str]], test_ratio: float = 0.3, seed: int = 42):
    random.seed(seed)
    data_copy = data.copy()
    random.shuffle(data_copy)
    split = int(len(data_copy) * (1 - test_ratio))
    return data_copy[:split], data_copy[split:]


def run_pipeline(mode: str) -> dict:
    train_data, test_data = split_dataset(NEWS_ITEMS)

    train_corpus = [process_text(text, mode) for _, text in train_data]
    test_corpus = [process_text(text, mode) for _, text in test_data]
    y_train = [label for label, _ in train_data]
    y_test = [label for label, _ in test_data]

    vocabulary = build_vocabulary(train_corpus, min_freq=1)
    X_train = vectorize(train_corpus, vocabulary)
    X_test = vectorize(test_corpus, vocabulary)

    model = train_naive_bayes(X_train, y_train)
    predictions = predict_naive_bayes(model, X_test)
    report = classification_report(y_test, predictions)

    return {
        'mode': mode,
        'vocab_size': len(vocabulary),
        'report': report,
        'test_data': test_data,
        'predictions': predictions,
        'y_test': y_test,
        'vocabulary': vocabulary,
    }


def print_results(results: dict) -> None:
    print(f"=== {results['mode'].upper()} RESULTS ===")
    print(f"Vocabulary size: {results['vocab_size']}")
    for metric, value in results['report'].items():
        print(f"  {metric.capitalize()}: {value:.2f}")
    print('\nSample predictions:')
    for (label, text), prediction in zip(results['test_data'], results['predictions']):
        truth = 'Fake' if label == 1 else 'Real'
        pred_label = 'Fake' if prediction == 1 else 'Real'
        print(f"  [{truth}] predicted={pred_label}: {text}")
    print('\n')


def compare_stemming_and_lemmatization():
    for mode in ['stem', 'lemma']:
        print_results(run_pipeline(mode))


if __name__ == '__main__':
    compare_stemming_and_lemmatization()
