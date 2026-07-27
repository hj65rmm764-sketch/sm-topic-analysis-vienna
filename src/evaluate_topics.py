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