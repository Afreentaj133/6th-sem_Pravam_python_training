import string

# Task 1: Tokenization function
def tokenize_sentence(sentence):
    # Remove punctuation
    translator = str.maketrans('', '', string.punctuation)
    cleaned_sentence = sentence.translate(translator)
    
    # Convert to lowercase (optional but useful)
    cleaned_sentence = cleaned_sentence.lower()
    
    # Split into words
    tokens = cleaned_sentence.split()
    
    return tokens


# Task 2: Sentence classifier
def classify_sentence(sentence):
    sentence = sentence.strip()
    
    if sentence.endswith('?'):
        return "Question"
    elif sentence.endswith('!'):
        return "Exclamation"
    else:
        return "Statement"


# -------------------------------
# Testing the analyzer
# -------------------------------
if __name__ == "__main__":
    text = input("Enter a sentence: ")
    
    tokens = tokenize_sentence(text)
    classification = classify_sentence(text)
    
    print("\nTokens:", tokens)
    print("Sentence Type:", classification)