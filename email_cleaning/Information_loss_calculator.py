import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

df = pd.read_csv("email_subset_cleaned_with_preprocessing.csv")

# Function to calculate token count ratio
def token_count_ratio(orig_text, cleaned_text):
    orig_tokens = len(orig_text.split())
    cleaned_tokens = len(cleaned_text.split())
    return cleaned_tokens / orig_tokens

# Function to calculate cosine similarity between original and preprocessed text
def calculate_cosine_similarity(orig_text, cleaned_text):
    vectorizer = TfidfVectorizer().fit_transform([orig_text, cleaned_text])
    vectors = vectorizer.toarray()
    cosine_sim = cosine_similarity(vectors)
    return cosine_sim[0, 1]

# Assuming df is your DataFrame containing original and cleaned content
df['token_count_ratio'] = df.apply(lambda row: token_count_ratio(row['content'], row['cleaned_content']), axis=1)
df['cosine_similarity'] = df.apply(lambda row: calculate_cosine_similarity(row['content'], row['cleaned_content']), axis=1)

# Calculate average metrics
average_token_count_ratio = df['token_count_ratio'].mean()
average_cosine_similarity = df['cosine_similarity'].mean()

print(f"Average Token Count Ratio: {average_token_count_ratio:.4f}")
print(f"Average Cosine Similarity: {average_cosine_similarity:.4f}")

