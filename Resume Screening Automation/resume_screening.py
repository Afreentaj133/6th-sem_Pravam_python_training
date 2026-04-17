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

# Relevant keywords for tech jobs (can be expanded)
TECH_KEYWORDS = {
    'python', 'java', 'javascript', 'c++', 'sql', 'machine learning', 'data science', 'ai', 'artificial intelligence',
    'deep learning', 'neural networks', 'tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy', 'flask', 'django',
    'react', 'angular', 'node.js', 'html', 'css', 'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'linux',
    'agile', 'scrum', 'devops', 'ci/cd', 'api', 'rest', 'graphql', 'database', 'mysql', 'postgresql', 'mongodb',
    'big data', 'hadoop', 'spark', 'kafka', 'elasticsearch', 'redis', 'microservices', 'cloud', 'serverless',
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


def extract_keywords(tokens: list[str]) -> list[str]:
    return [token for token in tokens if token in TECH_KEYWORDS]


def simple_lemmatize(token: str) -> str:
    lemma_map = {
        'went': 'go', 'gone': 'go', 'bought': 'buy', 'brought': 'bring', 'sent': 'send',
        'received': 'receive', 'running': 'run', 'meeting': 'meet', 'paid': 'pay', 'using': 'use',
        'claims': 'claim', 'says': 'say', 'saying': 'say', 'reported': 'report',
        'published': 'publish', 'reached': 'reach', 'reveals': 'reveal', 'revealed': 'reveal',
        'warns': 'warn', 'warned': 'warn', 'alleges': 'allege', 'alleged': 'allege',
        'developing': 'develop', 'developed': 'develop', 'programming': 'program', 'coded': 'code',
        'managing': 'manage', 'managed': 'manage', 'leading': 'lead', 'led': 'lead',
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


def process_text(text: str, extract_keywords_flag: bool = False) -> list[str]:
    cleaned = clean_text(text)
    tokens = tokenize(cleaned)
    tokens = remove_stop_words(tokens)
    if extract_keywords_flag:
        tokens = extract_keywords(tokens)
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


def match_resume_to_job(job_description: str, resume: str) -> dict:
    job_tokens = process_text(job_description, extract_keywords_flag=True)
    resume_tokens = process_text(resume, extract_keywords_flag=True)
    combined_corpus = [job_tokens, resume_tokens]
    vocabulary = build_vocabulary(combined_corpus)
    job_vec = vectorize(job_tokens, vocabulary)
    resume_vec = vectorize(resume_tokens, vocabulary)
    similarity = cosine_similarity(job_vec, resume_vec)
    score = similarity * 100
    match_level = 'High Match' if score >= 70 else 'Medium Match' if score >= 40 else 'Low Match'
    return {
        'similarity': similarity,
        'score': score,
        'match_level': match_level,
        'job_keywords': job_tokens,
        'resume_keywords': resume_tokens,
    }


def screen_candidates(job_description: str, resumes: list[str]) -> list[dict]:
    results = []
    for i, resume in enumerate(resumes, 1):
        match = match_resume_to_job(job_description, resume)
        match['candidate_id'] = i
        results.append(match)
    # Sort by score descending
    results.sort(key=lambda x: x['score'], reverse=True)
    return results


def main():
    job_desc = """
    We are looking for a Python developer with experience in machine learning, data science, and web development.
    Skills required: Python, TensorFlow, Flask, SQL, Git, Docker.
    """

    resumes = [
        """
        I am a software engineer with 5 years of experience in Python, machine learning using TensorFlow, and building web apps with Flask.
        I have worked with SQL databases and use Git for version control. Familiar with Docker for deployment.
        """,
        """
        Experienced data scientist skilled in R, statistics, and visualization. Some Python knowledge for scripting.
        """,
        """
        Full-stack developer proficient in JavaScript, React, Node.js, and MongoDB. Basic Python experience.
        """,
    ]

    print("Resume Screening Results:\n")
    results = screen_candidates(job_desc, resumes)
    for result in results:
        print(f"Candidate {result['candidate_id']}:")
        print(f"  Score: {result['score']:.1f}%")
        print(f"  Match Level: {result['match_level']}")
        print(f"  Job Keywords: {result['job_keywords']}")
        print(f"  Resume Keywords: {result['resume_keywords']}")
        print()


if __name__ == '__main__':
    main()
