# sm-topic-analysis-vienna

Dieses Repository enthält ein Data-Analysis-Projekt zur Extraktion häufig diskutierter Themen aus öffentlichen Mastodon-Beiträgen mit Bezug zu Wien. Das Projekt wird im Rahmen eines IU Studienfachs umgesetzt.

## Ziel des Projekts

Ziel ist es, öffentlich verfügbare Mastodon-Beiträge mit Bezug zu Wien zu sammeln, zu bereinigen und mithilfe von NLP-Verfahren die fünf am häufigsten diskutierten Themen zu extrahieren.
Zusätzlich werden Entity-Analysen durchgeführt:
- häufig verwendete Hashtags
- besonders aktive User

## Datenquelle

Die Daten werden über öffentliche Mastodon-Hashtag-Timelines erhoben. Für den ersten Test wurde die Instanz mastodon.social und der Hashtag #Wien verwendet. Der API Zugriff funktioniert ohne Access Token, da nur öffentliche Beiträge gelesen werden.

## Geplanter Workflow

1. Verbindung zur öffentlichen Mastodon-API
2. Abruf öffentlicher Beiträge zu Wien über Hashtags wie #Wien, #Vienna, #Austria
3. Speicherung der Rohdaten im CSV-Format
4. Vorverarbeitung der Texte
    - Entfernen von HTML
    - Entfernen von URLs
    - Entfernen von Sonderzeichen
    - Kleinschreibung
    - Stopword-Entfernung
5. Entity-Analyse
    - häufigste Hashtags
    - aktivste User
6. Vektorisierung der Texte
    - Bag-of-Words
    - TF-IDF
7. Topic Modeling
    - Latent Semantic Analysis (LSA)
    - Latent Dirichlet Allocation (LDA)
8. Diskussion und Interpretation der Ergebnisse

## Projektstruktur

```
sm-topic-analysis-vienna/
│
├── data/
│   ├── raw/
│   │   └── raw_mastodon_posts.csv
│   │
│   ├── processed/
│   │   └── clean_mastodon_posts.csv
│   │
│   └── results/
│       ├── bag_of_words.csv
│       ├── dataset_statistics.csv
│       ├── language_distribution.csv
│       ├── lda_topics.csv
│       ├── lsa_topics.csv
│       ├── tfidf_scores.csv
│       ├── top_hashtags.csv
│       ├── top_users.csv
│       └── word_frequencies.csv
│
├── src/
│   ├── config.py
│   ├── test_connection.py
│   ├── collect_posts.py
│   ├── preprocess.py
│   ├── entity_analysis.py
│   └── topic_modeling.py
│
├── .env
├── .gitignore
├── README.md
└── requirements.txt
```
## Beschreibung

*config.py:*
Verwaltet sämtliche projektweite Einstellungen wie Dateipfade oder Ergebnisverzeichnisse.

*test_connection.py:*
Testet die Verbindung zur öffentlichen Mastodon-API und prüft, ob Posts erfolgreich geladen werden können.

*collect_posts.py:*
Verbindet sich mit der Mastodon-API und lädt Posts zu definierten Hashtags in Rohform herunter, es werden bereits Duplikate entfernt.

Output: data/raw/raw_mastodon_posts.csv

*preprocess.py:*
Bereitet die Texte für NLP Verfahren vor:
- URL Entfernung
- Entfernung von Mentions
- Entfernung von Sonderzeichen
- Kleinschreibung
- Tokenisierung
- Stopword-Entfernung
- Berechnung d. Tokenanzahl

Output: data/processed/clean_mastodon_posts.csv

*entity_analysis.py:*
Führt explorative Analyse durch und erstellt:
- Datensatzstatistik
- Sprachverteilung
- häufigste Hashtags
- aktivste User
- häufigste Wörter

Output: data/results/*

*topic_modeling.py:*
Implementiert NLP Verfahren:
- Bag-of-Words
- TF-IDF
- Latend Semantic Analysis (LSA)
- Latent Dirichlet Allocation (LDA)

Output: data/results/*

## Einrichten der Umgebung

#### Virtuelle Umgebung erstellen:
`python -m venv venv`

#### Virtuelle Umgebung aktivieren:
`source venv/bin/activate`

#### Abhängigkeiten installieren:
`pip install -r requirements.txt`

#### Umgebungsvariablen

Die Mastodon-Instanz wird in einer lokalen **.env** Datei gespeichert:  
**MASTODON_INSTANCE**=https://mastodon.social


## Ausführung

### API Verbindung testen
`python src/test_connection.py`

### Beiträge sammeln
`python src/collect_posts.py`

### Beiträge bereinigen
`python src/preprocess.py`

### Entitäts Analyse
`python src/entity_analysis.py`

### NLP Methoden
`python src/topic_modeling.py`
