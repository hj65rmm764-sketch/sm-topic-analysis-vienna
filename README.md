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
4. Vorverarbeitung der Tweet-Texte
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

sm-topic-analysis-vienna/
│
├── data/
│   ├── raw/                  Rohdaten aus der Mastodon API
│   ├── processed/            Bereinigte Datensätze für NLP
│   └── results/              
│
├── src/
│   ├── config.py             Zentrale Projektkonfiguration
│   ├── test_connection.py    Test-Verbindung zur Mastodon API
│   ├── collect_posts.py      Sammelt/speichert Posts in CSV
│   └── preprocess.py         Bereinigt die gesammelten Posts
│
├── .env                      Lokale Konfiguration
├── .gitignore
├── README.md
└── requirements.txt


## Einrichten der Umgebung

#### Virtuelle Umgebung erstellen:
`python -m venv venv`

#### Virtuelle Umgebung aktivieren:
`source venv/bin/activate`

#### Abhängigkeiten installieren:
`pip install -r requirements.txt`

## Umgebungsvariablen

Die Mastodon-Instanz wird in einer lokalen **.env** Datei gespeichert:  
**MASTODON_INSTANCE**=https://mastodon.social

## API Verbindung testen
`python src/test_connection.py`

## Beiträge sammeln
`python src/collect_posts.py`

## Beiträge bereinigen
`python src/preprocess.py`