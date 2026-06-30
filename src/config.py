"""
Projektweite Config.

Alle Pfade und Parameter werden zentral verwaltet.
"""

# Verzeichnisse

from pathlib import Path

DATA_DIR = Path("data")

RAW_DIR = DATA_DIR / "raw"

PROCESSED_DIR = DATA_DIR / "processed"

RESULTS_DIR = DATA_DIR / "results"

# Dateien

RAW_DATA_PATH = RAW_DIR / "raw_mastodon_posts.csv"

PROCESSED_DATA_PATH = PROCESSED_DIR / "clean_mastodon_posts.csv"

# Mastodon

DEFAULT_INSTANCE = "https://mastodon.social"

SEARCH_HASHTAGS = [
    "Wien",
    "Vienna",
    "Österreich",
    "Austria",
    "WienerLinien",
    "Klimakrise",
    "Hitzewelle",
]

MAX_POSTS_PER_HASHTAG = 40