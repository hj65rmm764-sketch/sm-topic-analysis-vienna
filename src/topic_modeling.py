"""
Topic Modeling

Dieses Skript implementiert die im Studienskript behandelten NLP Verfahren:

1. Bag-of-Words
2. TD-IDF
3. LSA
4. LDA
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

from config import (
    PROCESSED_DATA_PATH,
    BAG_OF_WORDS_PATH,
    TFIDF_RESULTS_PATH,
)

def load_data() -> pd.DataFrame:
    """
    Lädt bereinigte Posts
    """
    return pd.read_csv(PROCESSED_DATA_PATH)

def create_bag_of_words(df: pd.DataFrame, max_features: int = 50,) -> pd.DataFrame:
    """
    Erstellt eine Bag-of-Words Darstellung.

    Args:
        df: Bereinigte Posts
        max_features: Max Anzahl an Wörtern

    Returns:
        DataFrame mit häufigsten Begriffen
    """

    vectorizer = CountVectorizer(
        max_features=max_features
    )

    bow_matrix = vectorizer.fit_transform(
        df["clean_text"]
    )

    frequencies = bow_matrix.sum(axis=0).A1

    words = vectorizer.get_feature_names_out()

    result = pd.DataFrame(
        {
        "word": words,
        "count": frequencies
        }
    )

    return result

def create_tfidf_scores(df: pd.DataFrame, max_features: int = 50,) -> pd.DataFrame:
    """
    Berechnet die durchschnittlichen TF-IDF Werte aller Begriffe im Datensatz.

    Args:
        df: bereinigte Posts
        max_features: Max Anzahl an Posts

    Returns:
        DataFrame mit Begriffen und durchschnittlichen TF-IDF Wert
    """
    vectorizer = TfidfVectorizer(
        max_features=max_features
    )

    tfidf_matrix = vectorizer.fit_transform(
        df["clean_text"]
    )

    words = vectorizer.get_feature_names_out()

    average_scores = tfidf_matrix.mean(axis=0).A1

    result = pd.DataFrame(
        {
            "word": words,
            "average_tfidf": average_scores,
        }
    )

    results = result.sort_values(
        by="average_tfidf",
        ascending=False,
    )

    return result

    

def main():

    df = load_data()

    bag_of_words = create_bag_of_words(df)
    tfidf_scores = create_tfidf_scores(df)

    bag_of_words.to_csv(
        BAG_OF_WORDS_PATH,
        index=False,
        encoding="utf-8",
    )

    tfidf_scores.to_csv(
        TFIDF_RESULTS_PATH,
        index=False,
        encoding="utf-8"
    )

    print("-" * 80)
    print("Bag-of-Words")
    print("-" * 80)

    print(bag_of_words.head(20))

    print("-" * 80)
    print(f"Datei gespeichert unter:\n{BAG_OF_WORDS_PATH}")

    print("-" * 80)
    print("TF-IDF")
    print("-" * 80)

    print(tfidf_scores.head(20))

    print("-" * 80)
    print(f"Datei gespeichert unter:\n{TFIDF_RESULTS_PATH}")

if __name__ == "__main__":
    main()