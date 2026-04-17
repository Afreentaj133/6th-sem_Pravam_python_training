import nltk
nltk.download('punkt_tab')
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required data
nltk.download('punkt')

text = "Python is very powerful. It is used in NLP."

# Word Tokenization
words = word_tokenize(text)
print("Words:", words)

# Sentence Tokenization
sentences = sent_tokenize(text)
print("Sentences:", sentences)