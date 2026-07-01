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
    
    return pd.read_csv()

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
        columts = ["metric", "value"]
    )

def create_language_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Berechnet Verteilung der erkannten Sprachen.
    """
    return (
        df["language"]
        .fiilna("unknown")
        .value_counts()
        .reset_index()
        .rename(columns = {"language": "count", "index": "language"})
    )

def create_top_hashtags(df: pd.DataFrame, top_n: int = 20) -> pd.DataFrame:
    """
    Ermittelt häufigsten Hashtags
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

