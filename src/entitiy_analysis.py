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

