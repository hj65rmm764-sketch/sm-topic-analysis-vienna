"""
Evaluation der Anzahl an LDA-Topics

Dieses Skript berechnet den Coherence Score für verschiedene Anzahlen
an Topics. Dadurch kann die in topic_modeling.py verwendete Topic-Anzahl
datenbasiert bewertet werden.

Für jede Topic-Anzahl zwischen MIN_TOPICS und MAX_TOPICS wird:
- ein Gensim-LDA-Modell trainiert
- der c_v-Coherence-Score berechnet
- das Ergebnise als CSV gespeichert
- eine grafische Darstellung erzeugt
"""

import matplotlib.pyplot as plt
import pandas as pd
from gensim.corpora import Dictionary
from gensim.models import CoherenceModel, LdaModel
from config import (
    PROCESSED_DATA_PATH,
    COHERENCE_RESULTS_PATH,
    COHERENCE_PLOT_PATH,
    MIN_TOPICS,
    MAX_TOPICS,
    NUMBER_OF_TOPIC_WORDS
)

def load_data() -> pd.DataFrame:
    """
    Lädt die bereinigten Mastodon-Posts.

    Returns:
        DataFrame mit den bereinigten Posts
    """
    if not PROCESSED_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Bereinigte Daten nicht gefunden: {PROCESSED_DATA_PATH}. "
            "Bitte zuerst src/preprocessing.py ausführen."
        )

    return pd.read_csv(PROCESSED_DATA_PATH)

def prepare_tokens(df: pd.DataFrame) -> list[list[str]]:
    """
    Wandelt die bereinigten Texte in Tokenlisten um.

    Args:
        df: DataFrame mit der Spalte clean_text

    Returns:
        Liste mit einer Tokenliste pro Beitrag
    """
    if "clean_text" not in df.columns:
        raise KeyError(
            "Die benötigte Spalte 'clean_text' wurde nicht gefunden."
        )

    texts = (
        df["clean_text"]
        .fillna("")
        .astype(str)
    )

    tokenized_texts = [
        text.split()
        for text in texts
        if text.strip()
    ]

    return tokenized_texts

def create_dictionary_and_corpus(
    tokenized_texts: list[list[str]],
) -> tuple[Dictionary, list[list[tuple[int, int]]]]:
    """
    Erstellt ein Gensim-Wörterbuch und ein Bag-of-Words Korpus.

    Args:
        tokenized_texts: Bereinigte und tokenisierte Posts

    Returns:
        Gensim-Dictionary und Bag-of-Words Korpus
    """
    dictionary = Dictionary(tokenized_texts)

    corpus = [
        dictionary.doc2bow(tokens)
        for tokens in tokenized_texts
    ]

    return dictionary, corpus
