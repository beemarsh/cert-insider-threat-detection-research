from collections import Counter
from math import log2
import pandas as pd

df = pd.read_csv("email_subset_cleaned_with_preprocessing.csv")
def calculate_entropy(text_series):
    total_words = 0
    word_freq = Counter()
    for text in text_series:
        words = text.split()
        total_words += len(words)
        word_freq.update(words)
    entropy = -sum((count / total_words) * log2(count / total_words) for count in word_freq.values())
    return entropy

entropy_original = calculate_entropy(df['content'])
entropy_preprocessed = calculate_entropy(df['cleaned_content'])

print(f"Original Entropy: {entropy_original:.4f} bits per word")
print(f"Preprocessed Entropy: {entropy_preprocessed:.4f} bits per word")
