"""
Projektweite Config.

Alle Pfade und Parameter werden zentral verwaltet.
"""



from pathlib import Path

# Ordner in dem config.py liegt: .../sm-topic-analysis-vienna/src
SRC_DIR = Path(__file__).resolve().parent

# Projektwurzel: .../sm-topic-analysis-vienna
PROJECT_ROOT = SRC_DIR.parent

# Verzeichnisse

DATA_DIR = PROJECT_ROOT / "data"

RAW_DIR = DATA_DIR / "raw"

PROCESSED_DIR = DATA_DIR / "processed"

RESULTS_DIR = DATA_DIR / "results"

# Dateien

RAW_DATA_PATH = RAW_DIR / "raw_mastodon_posts.csv"

PROCESSED_DATA_PATH = PROCESSED_DIR / "clean_mastodon_posts.csv"

DATASET_STATISTICS_PATH = RESULTS_DIR / "dataset_statistics.csv"

LANGUAGE_DISTRIBUTION_PATH = RESULTS_DIR / "languange_distribution.csv"

TOP_HASHTAGS_PATH = RESULTS_DIR / "top_hashtags.csv"

TOP_USERS_PATH = RESULTS_DIR / "top_users.csv"

WORD_FREQUENCIES_PATH = RESULTS_DIR / "word_frequencies.csv"

BAG_OF_WORDS_PATH = RESULTS_DIR / "bag_of_words.csv"

TFIDF_RESULTS_PATH = RESULTS_DIR / "tfidf_scores.csv"

LSA_RESULTS_PATH = RESULTS_DIR / "lsa_topics.csv"

LDA_RESULTS_PATH = RESULTS_DIR / "lda_topics.csv"

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

# Misc

NUMBER_OF_TOPICS = 5

NUMBER_OF_TOPIC_WORDS = 10