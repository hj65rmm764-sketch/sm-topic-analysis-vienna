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

def compute_coherence_scores(
    tokenized_texts: list[list[str]],
    dictionary: Dictionary,
    corpus: list[list[tuple[int, int]]],
    min_topics: int = MIN_TOPICS,
    max_topics: int = MAX_TOPICS
) -> pd.DataFrame:
    """
    Berechnet den c_v-Coherence Score für mehrere Topic Anzahlen.

    Args:
        tokenized_texts: Tokenisierte Posts
        dictionary: Gensim-Wörterbuch
        corpus: Bag-of-Words Korpus
        min_topics: Kleinste zu untersuchende Topic-Anzahl
        max_topics: Größte zu untersuchende Topuc-Anzahl

    Returns:
        DataFrame mit Topic-Anzahl und Coherence Score
    """
    results = []

    for number_of_topics in range(min_topics, max_topics +1):
        print(
            f"Berechne Modell mit {number_of_topics} Topics ..."
        )

        lda_model = LdaModel(
            corpus=corpus,
            id2word=dictionary,
            num_topics=number_of_topics,
            random_state=42,
            passes=10,
            iterations=100,
            alpha="auto",
            per_word_topics=False,
        )

        coherence_model = CoherenceModel(
            model=lda_model,
            texts=tokenized_texts,
            dictionary=dictionary,
            coherence="c_v",
            topn=NUMBER_OF_TOPIC_WORDS,
            processes=1,
        )

        coherence_score = coherence_model.get_coherence()

        results.append(
            {
                "number_of_topics": number_of_topics,
                "coherence_score": coherence_score,
            }
        )

        print(
            f"Coherence Score: {coherence_score:.4f}"
        )

    return pd.DataFrame(results)

def create_coherence_plot(results: pd.DataFrame) -> None:
    """
    Erstellt eine graphische Darstellung des Coherence Scores.

    Args:
        results: DataFrame mit Topic-Anzahlen und Coherence Scores
    """
    plt.figure(figsize=(8,5))

    plt.plot(
        results["number_of_topics"],
        results["coherence_score"],
        marker="o",
    )

    plt.xlabel("Anzahl der Topics")
    plt.ylabel("Coherence Score (c_v)")
    plt.title("Coherence Score nach Anzahl der LDA Topics")
    plt.xticks(results["number_of_topics"])
    plt.grid(True)
    plt.tight_layout()

    COHERENCE_PLOT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.savefig(
        COHERENCE_PLOT_PATH,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close

def main() -> None:
    """
    Führt die Evaluation der Topic-Anzahlen aus.
    """
    df = load_data()

    print(f"Geladene Posts: {len(df)}")

    tokenized_texts = prepare_tokens(df)

    print(
        f"Für die Evaluation verwendete Texte: "
        f"{len(tokenized_texts)}"
    )

    if not tokenized_texts:
        raise ValueError(
            "Es sind keine für die bereinigten Texte für die Evaluation verfügbar."
        )

    dictionary, corpus = create_dictionary_and_corpus(
        tokenized_texts
    )

    if len(dictionary) == 0:
        raise ValueError(
            "Das erzeugte Wörterbuch enthält keine Begriffe."
        )

    print(f"Anzahl unterschiedlicher Begriffe: {len(dictionary)}")
    print(f"-" * 80)

    results = compute_coherence_scores(
        tokenized_texts=tokenized_texts,
        dictionary=dictionary,
        corpus=corpus,
    )

    COHERENCE_RESULTS_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    results.to_csv(
        COHERENCE_RESULTS_PATH,
        index=False,
        encoding="utf-8",
    )

    create_coherence_plot(results)

    best_result = results.loc[
        results["coherence_score"].idxmax()
    ]

    print("-" * 80)
    print("Coherence Auswertung")
    print("-" * 80)
    print(results.to_string(index=False))

    print("-" * 80)
    print(
        "Höchster Coherence Score: "
        f"{best_result['coherence_score']:.4f}"
    )
    print(
        "Topic-Anzahl mit höchstem Score: "
        f"{int(best_result['number_of_topics'])}"
    )

    print("-" * 80)
    print(
        f"Ergebnisse gespeichert unter:\n"
        f"{COHERENCE_RESULTS_PATH}"
    )
    print(
        f"Grafik gespeichert unter:\n"
        f"{COHERENCE_PLOT_PATH}"
    )

if __name__ == "__main__":
    main()