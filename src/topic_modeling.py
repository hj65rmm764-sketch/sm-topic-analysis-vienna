"""
Topic Modeling

Dieses Skript implementiert die im Studienskript behandelten NLP Verfahren:

1. Bag-of-Words
2. TD-IDF
3. LSA
4. LDA
"""

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

from config import (
    PROCESSED_DATA_PATH,
    BAG_OF_WORDS_PATH,
)

