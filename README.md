# sm-topic-analysis-vienna

Dieses Repository enthält ein Data-Analysis-Projekt zur Extraktion häufig diskutierter Themen aus Reddit-Beiträgen mit Bezug zu Wien. Das Projekt wird im Rahmen eines IU Studienfachs umgesetzt.

## Ziel des Projekts

Ziel ist es, öffentlich verfügbare Reddit-Beiträge mit Bezug zu Wien zu sammeln, textuell vorzubereiten und mithilfe von NLP-Verfahren die fünf am häufigsten diskutierten Themen zu extrahieren. Zusätzlich werden häufig verwendete Subreddits bzw. Flairs und besonders aktive User analysiert.

## Geplanter Workflow

1. Verbindung zur Reddit-API über PRAW
2. Abruf relevanter Beiträge aus Subreddits wie r/wien oder r/austria
3. Speicherung der Rohdaten im CSV-Format
4. Vorverarbeitung der Tweet-Texte
    - Entfernen von URLs
    - Entfernen von Sonderzeichen
    - Kleinschreibung
    - Stopword-Entfernung
5. Entity-Analyse
    - häufigste Subreddits oder Flairs
    - aktivste User
6. Vektorisierung der Texte
    - Bag-of-Words
    - TF-IDF
7. Topic Modeling
    - Latent Semantic Analysis (LSA)
    - Latent Dirichlet Allocation (LDA)
8. Diskussion und Interpretation der Ergebnisse

## Projektstruktur

## Einrichten der Umgebung

#### Virtuelle Umgebung erstellen:
python -m venv venv

#### Virtuelle Umgebung aktivieren:
source venv/bin/activate

#### Abhängigkeiten installieren:
pip install -r requirements.txt

## Umgebungsvariablen

Die Zugangsdaten werden in einer lokalen .env Datei gespeichert:
REDDIT_CLIENT_ID=deine_reddit_client_id  
REDDIT_CLIENT_SECRET=dein_reddit_client_secret  
REDDIT_USER_AGENT=dein_reddit_user_agent  

## API-Test

python src/01_test_reddit_connection.py