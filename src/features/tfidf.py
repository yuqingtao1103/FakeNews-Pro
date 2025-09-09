from sklearn.feature_extraction.text import TfidfVectorizer
def build_vectorizer(max_features: int = 50000, ngram_range=(1,2)):
    return TfidfVectorizer(lowercase=True, strip_accents="unicode", max_features=max_features, ngram_range=ngram_range, min_df=2)
