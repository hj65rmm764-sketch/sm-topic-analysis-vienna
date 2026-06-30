"""
Preprocessing der gesammelten Beiträge

Dieses Skript lädt die Rohdaten aus data/raw/raw_mastodon_posts.csv,
bereinigt die Texte für NLP-Verfahren und speichert das Ergebins unter
data/processed/clean_mastodon_posts.csv

Folgende Schritte werden durchgfeführt:
    - URLs entfernen
    - Erwähnungen entfernen
    - Hashtag Zeichen entfernen (#)
    - in Kleinbuchstaben konvertiert
    - Sonderzeichen entfernen
    - Zahlen entfernen
    - Tokenisierung
    - Stopword-Entfernung
    - kurze Token entfernen
"""

import re
from pathlib import Path
import nltk
import pandas as pd
from nltk.corpus import stopwords

from config import (
    RAW_DATA_PATH,
    PROCESSED_DATA_PATH,
)

def download_nltk_resources() -> None:
    """
    Lädt benötigte NLTK Ressourcen herunter, falls noch nicht vorhanden
    """
    nltk.download("stopwords", quiet=True)

def build_stopword_list() -> set[str]:
    """
    Erställt eine Stopword-Liste für deutsche und englische Texte.

    Mastodon Beiträge zu Wien können in deutsch oder einer anderen Sprache geschreiben sein.
    Deshalb werden deutsche und englische Stopwords kombiniert.

    Returns:
        Set mit Stopwords
    """
    german_stopwords = set(stopwords.words("german"))
    english_stopwords = set(stopwords.words("english"))

    custom_stopwords = {
        "wien",
        "vienna",
        "austria",
        "österreich",
        "https",
        "http",
        "www",
        "amp",
    }

    return german_stopwords.union(english_stopwords).union(custom_stopwords)

def clean_text(text: str, stopword_set: set[str]) -> str:
    """
    Bereinigt einen einzelnen Text für spätere NLP Analyse.

    Args:
        text: Originaltext aus CSV
        stopword_set: Menge an Stopwords, die entfernt werden sollen

    Returns:
        Bereinigter Text als String
    """
    if not isinstance(text, str):
        return ""
    
    # URLs entfernen
    text = re.sub(r"http\S+|www\S+", " ", text)

    # User Erwähnungen entfernen
    text = re.sub(r"@\w+", " ", text)

    # Hashtag Zeichen entfernen - Begriffe bleiben erhalten
    text = text.replace("#", " ")

    # In Kleinbuchstaben umwandeln
    text = text.lower()

    # Umlaute vereinheitlichen
    text = (
        text.replace("ä", "ae")
        .replace("ö", "oe")
        .replace("ü", "ue")
        .replace("ß", "ss")
    )

    # Alles eentfernen, was kein Buchstabe ist
    text = re.sub(r"[^a-zA-Z\s]", " ", text)

    # Mehrfache Leerzeichen entfernen
    text = re.sub(r"\s+", " ", text).strip()

    # Tokenisierung
    tokens = text.split()

    # Stopwords und sehr kurze Wörter entfernen
    tokens = [
        token
        for token in tokens
        if token not in stopword_set and len(token) > 2
    ]

    return " ".join(tokens)

def main() -> None:
    """
    Führt das Preprocessing für alle gesammelten Mastodon-Posts aus
    """
    download_nltk_resources()

    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"Rohdaten nicht gefunden: {RAW_DATA_PATH}. "
            "Bitte zuerst src/02_collect_mastodon_posts.py ausführen."
        )
    
    stopword_set = build_stopword_list()

    df = pd.read_csv(RAW_DATA_PATH)

    print(f"Geladene Rohdaten: {len(df)} Beiträge")

    # Fehlende Texte durch leere Strings ersetzen
    df["text"] = df["text"].fillna("")

    # Bereinigten Text erzeugen
    df["clean_text"] = df["text"].apply(
        lambda value: clean_text(value, stopword_set)
    )

    # Tokenzahl pro bereinigtem Beitrag berechnen
    df["token_count"] = df["clean_text"].apply(
        lambda value: len(value.split())
    )

    # Sehr kurze Beiträge entfernen, da sie für Topic Modeling nicht hilfreich sind
    df_clean = df[df["token_count"] >= 3].copy()

    # Output-Ordner sicherhstellen
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)

    df_clean.to_csv(PROCESSED_DATA_PATH, index=False, encoding="utf-8")

    print(f"Beiträge nach Bereinigung: {len(df_clean)}")
    print(f"Entfernte sehr kurze Beiträge: {len(df) - len(df_clean)}")
    print(f"Datei gespeichert unter: {PROCESSED_DATA_PATH}")

    print("-" * 80)
    print("Beispiel bereinigter Texte:")
    print("-" * 80)

    for _, row in df_clean[["text", "clean_text"]].head(5).iterrows():
        print("Original:")
        print(row["text"])
        print("Bereinigt:")
        print(row["clean_text"])
        print("-" * 80)

if __name__ == "__main__":
    main()