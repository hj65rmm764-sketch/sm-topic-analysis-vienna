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
    LSA_RESULTS_PATH,
    NUMBER_OF_TOPICS,
    NUMBER_OF_TOPIC_WORDS,
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


def create_lsa_topics(df: pd.DataFrame, number_of_topics: int = NUMBER_OF_TOPICS, number_of_words: int = NUMBER_OF_TOPIC_WORDS, max_features: int = 100,) -> pd.DataFrame:
    """
    Führt LSA auf Basis einer TF-IDF Matrix durch.

    LSA reduziert die Dimensionen der TF-IDF Matrix und versucht, latente semantische
    Strukturen bzw Themen in Texten sichtbar zu mache.
    """

    # TF-IDF Matrix erstellen
    vectorizer = TfidfVectorizer(
        max_features=max_features
    )

    tfidf_matrix = vectorizer.fit_transform(
        df["clean_text"]
    )

    words = vectorizer.get_feature_names_out()

    # TruncatedSVD wird für LSA verwendet
    lsa_model = TruncatedSVD(
        n_components=number_of_topics,
        random_state=42
    )

    lsa_model.fit(tfidf_matrix)

    topics = []

    # Für jedes Thema werden die wichtigsten Wörter extrahiert
    for topic_index, component in enumerate(lsa_model.components_):
        word_indices = component.argsort()[::-1][:number_of_words]
        topic_words = [words[index] for index in word_indices]

        topics.append(
            {
                "topic": f"LSA Topic {topic_index + 1}",
                "top_words": ", ".join(topic_words)
            }
        )
    return pd.DataFrame(topics)

def main():

    df = load_data()

    bag_of_words = create_bag_of_words(df)
    tfidf_scores = create_tfidf_scores(df)
    lsa_topics = create_lsa_topics(df)

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

    lsa_topics.to_csv(
        LSA_RESULTS_PATH,
        index=False,
        encoding="utf-8",
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

    print("-" * 80)
    print("LSA Topics")
    print("-" * 80)

    print(lsa_topics)

    print("-" * 80)
    print(f"Datei gespeichert unter:\n{LSA_RESULTS_PATH}")

if __name__ == "__main__":
    main()