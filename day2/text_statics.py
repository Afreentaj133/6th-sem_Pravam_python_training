import re

def detailed_text_stats(text):
    # Split sentences properly
    sentences = [s.strip() for s in re.split(r'[.!?]', text) if s.strip()]

    # Words
    words = text.split()

    # Characters (excluding spaces)
    chars = len(text.replace(" ", ""))

    # Unique words (cleaned)
    unique_words = set(w.lower().strip(".,!?") for w in words)

    # Averages
    avg_word_len = sum(len(w.strip(".,!?")) for w in words) / len(words) if words else 0
    avg_sent_len = len(words) / len(sentences) if sentences else 0

    # Lexical diversity
    lexical_div = len(unique_words) / len(words) if words else 0

    # Output
    print(f"Characters (no spaces) : {chars}")
    print(f"Total words            : {len(words)}")
    print(f"Unique words           : {len(unique_words)}")
    print(f"Sentences              : {len(sentences)}")
    print(f"Avg word length        : {avg_word_len:.1f} chars")
    print(f"Avg sentence length    : {avg_sent_len:.1f} words")
    print(f"Lexical diversity      : {lexical_div:.2f}")


# Sample text
sample = """
Python is a versatile programming language. It is widely used in data 
science, web development, and artificial intelligence. Python's simple 
syntax makes it ideal for beginners. Many companies use Python for their 
AI projects.
"""

detailed_text_stats(sample.strip())