"""
Explorative Datenanalyse und Entity-Analyse.

Dieses Skript analysiert die bereinigten Mastodon Posts.
Es werden Kennzahlen, häufige Hashtags, aktive User und
häufige Wörter berechnet.

Die Ergebnisse werden als CSV Datei in data/results/ gespeichert.
"""

from collections import Counter
from pathlib import Path
import pandas as pd

from config import (
    PROCESSED_DATA_PATH,
    RESULTS_DIR,
    DATASET_STATISTICS_PATH,
    LANGUAGE_DISTRIBUTION_PATH,
    TOP_HASHTAGS_PATH,
    TOP_USERS_PATH,
    WORD_FREQUENCIES_PATH,
)

def load_processed_data(path: Path) -> pd.DataFrame:
    """
    Lädt die bereinigten Daten.

    Args:
        path: Pfad zur bereinigten CSV Datei

    Returns:
        DataFrame mit bereinigten Posts
    """
    if not path.exists():
        raise FileNotFoundError(
            f"Datei nicht gefunden: {path}. "
            "Bitte zuerst preprocess.py ausführen."
        )
    
    return pd.read_csv(path)

def create_dataset_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Erstellt Statistiken zum Datensatz.
    """
    statistics = {
        "number_of_posts": len(df),
        "number_of_unique_users": df["username"].nunique(),
        "number_of_languages": df["language"].nunique(),
        "average_token_count": round(df["token_count"].mean(), 2),
        "median_token_count": round(df["token_count"].median(), 2),
        "max_token_count": int(df["token_count"].max()),
    }

    return pd.DataFrame(
        statistics.items(),
        columns = ["metric", "value"]
    )

def create_language_distribution(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    Berechnet Verteilung der erkannten Sprachen.
    """
    top_languages = (
        df["language"]
        .fillna("unknown")
        .value_counts()
        .head(top_n)
    )

    return pd.DataFrame(
        {
            "language": top_languages.index,
            "count": top_languages.values,
        }
    )

def create_top_hashtags(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    Ermittelt die häufigsten Hashtags
    """
    all_hashtags = []

    for hashtag_string in df["hashtags"].fillna(""):
        hashtags = hashtag_string.split(",")

        for hashtag in hashtags:
            hashtag = hashtag.strip().lower()

            if hashtag:
                all_hashtags.append(hashtag)

    counter = Counter(all_hashtags)

    return pd.DataFrame(
        counter.most_common(top_n),
        columns = ["hashtag", "count"]
    )

def create_top_users(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    Ermittelt die aktivsten User
    """
    top_users = (
        df["username"]
        .fillna("unknown")
        .value_counts()
        .head(top_n)
    )

    return pd.DataFrame(
        {
            "username": top_users.index,
            "count": top_users.values,
        }
    )

def create_word_frequencies(df: pd.DataFrame, top_n: int = 30) -> pd.DataFrame:
    """
    Zählt die am häufigsten vorkommenden Wörter
    """
    all_words = []

    for text in df["clean_text"].fillna(""):
        words = text.split()
        all_words.extend(words)

    counter = Counter(all_words)

    return pd.DataFrame(
        counter.most_common(top_n),
        columns = ["word", "count"]
    )

def main() -> None:
    """
    Führt explorative Analyse und Entitiy-Analyse durch
    """

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    df = load_processed_data(PROCESSED_DATA_PATH)

    dataset_statistics = create_dataset_statistics(df)
    language_distribution = create_language_distribution(df)
    top_hashtags = create_top_hashtags(df)
    top_users = create_top_users(df)
    word_frequencies = create_word_frequencies(df)

    dataset_statistics.to_csv(DATASET_STATISTICS_PATH, index=False, encoding="utf-8")
    language_distribution.to_csv(LANGUAGE_DISTRIBUTION_PATH, index=False, encoding="utf-8")
    top_hashtags.to_csv(TOP_HASHTAGS_PATH, index=False, encoding="utf-8")
    top_users.to_csv(TOP_USERS_PATH, index=False, encoding="utf-8")
    word_frequencies.to_csv(WORD_FREQUENCIES_PATH, index=False, encoding="utf-8")

    print("Explorative Analyse abgeschlossen.")
    print("-" * 80)

    print("Datensatzstatistik:")
    print(dataset_statistics)

    print("-" * 80)
    print("Top Hashtags:")
    print(top_hashtags.head(10))

    print("-" * 80)
    print("Top User:")
    print(top_users.head(10))

    print("-" * 80)
    print("Häufigste Wörter:")
    print(word_frequencies.head(10))

    print("-" * 80)
    print(f"Ergebnisse gespeichert unter: {RESULTS_DIR}")

if __name__ == "__main__":

    main()
