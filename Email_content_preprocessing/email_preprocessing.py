import pandas as pd
import re
import spacy
from nltk.corpus import stopwords

# Load Spacy's English model for Named Entity Recognition (NER)
nlp = spacy.load("en_core_web_sm")


# Define a function for preprocessing
def preprocess_text(text):
    # Step 1: Lowercasing
    text = text.lower()
    
    # Step 2: Named Entity Recognition (NER) - Preserve named entities
    doc = nlp(text)
    entities = {ent.text: ent.label_ for ent in doc.ents}
    
    # Step 3: Remove unwanted punctuation but keep some like periods and quotes
    text = re.sub(r'[^\w\s\.\'\"]', '', text)  # Remove all but . ' "

    # Step 4: Tokenize and Remove Stopwords selectively
    stop_words = set(stopwords.words('english'))
    important_stopwords = {'he', 'she', 'it', 'they', 'them', 'his', 'her', 'him', 'the', 'a', 'an'}  # Keep these
    tokens = [word for word in text.split() if word not in stop_words or word in important_stopwords]

    # Step 5: Reconstruct the text
    text = ' '.join(tokens)
    
    # Step 6: Restore Named Entities with original capitalization
    for entity, label in entities.items():
        text = text.replace(entity.lower(), entity)
    
    return text

# Example usage with a sample DataFrame

df = pd.read_csv("email_subset.csv")
df = df[['id','content']]
# Apply preprocessing to the 'content' column
df['cleaned_content'] = df['content'].apply(preprocess_text)

# Optionally, save the DataFrame with the cleaned text
df.to_csv('email_subset_cleaned_with_preprocessing.csv', index=False)


