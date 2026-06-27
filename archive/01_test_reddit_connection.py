"""
Test der Verbindung zur Reddit API.

Dieses Skript prüft, ob die Zugangsdaten aus der .env Datei korrekt gelesen werden
und ob mit PRAW ein read-only Zugriff auf Reddit möglich ist.
"""

import os
import praw
from dotenv import load_dotenv

def create_reddit_client() -> praw.Reddit:
    """
    Erstellt einen read-only Reddit-Client mit den Zugangsdaten aus der .env Datei

    Return:
        praw.Reddit: Reddit-Client-Intsanz für read-only API Zugriffe
    """
    load_dotenv()

    client_id = os.getenv("REDDIT_CLIENT_ID")
    client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    user_agent = os.getenv("REDDIT_USER_AGENT")

    if not client_id or not client_secret or not user_agent:
        raise ValueError(
            "Fehlende Reddit-Zugangsdaten. Bitte prüfe REDDIT_CLIENT_ID, "
            "REDDIT_CLIENT_SECRET ud REDDIT_USER_AGENT in der .env Datei."
        )
    
    #read-only Client erstellen
    reddit = praw.Reddit(
        client_id = client_id,
        client_secret = client_secret,
        user_agent = user_agent
    )

    return reddit

def main() -> None:
    """
    Führt einen einfachen Verbindungstest aus, indem aktuelle Posts aus r/wien
    abgerufen und im Terminal ausgegeben werden.
    """

    reddit = create_reddit_client()

    #prüft read-only Modus von PRAW
    print(f"Read-only Modus: {reddit.read_only}")
    print("-" * 80)

    #Beispiel: aktuelle Beiträge aus Subreddit r/wien abrufen
    subreddit = reddit.subreddit("wien")

    for submission in subreddit.hot(limit=10):
        print(f"Titel: {submission.title}")
        print(f"Autor: {submission.author}")
        print(f"Score: {submission.score}")
        print(f"Kommentare: {submission.num_comments}")
        print(f"URL: https://www.reddit.com{submission.permalink}")
        print("-" * 80)

if __name__ == "__main__":
    main()