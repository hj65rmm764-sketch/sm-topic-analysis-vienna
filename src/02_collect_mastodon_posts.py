"""
Sammelt öffentliche Mastodon-Beiträge zu Wien und speichert sie als CSV.

Dises Skript fragt mehrere Hashtag-Timelines ab, bereinigt nur HTML aus dem 
Content-Feld und speichert die Rohdaten strukturiert in data/raw_mastodon_posts.csv.
Die eigentliche NLP-Bereinigung erfolgt später in einem separaten Preprocessing-Skript.
"""

import os
import time
from datetime import datetime, timezone
import pandas as pd
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

def clean_html(raw_html: str) -> str:
    """
    Entfernt HTML-Tags aus Mastodon Beiträgen.

    Args:
        raw_html: HTML-Inhalt eines Posts

    Returns:
        Text ohne HTML-Tags
    """
    soup = BeautifulSoup(raw_html, "lxml")
    return soup.get_text(separator=" ", strip=True)

def fetch_hashtag_posts(instance: str, hashtag: str, limit: int = 40) -> list[dict]:
    """
    Ruft öffentliche Beiträge für bestimmtem Hashtag an.

    Args:
        instance: Mastodon-Instanz, zb https://mastodon.social
        hashtag: Hashtag ohne #, zb Wien
        limit: Max. Anzahl der Beiträge pro Anfrage

    Returns:
        Liste von Post-Dictionaries aus der Mastodon-API
    """
    url = f"{instance}/api/v1/timelines/tag/{hashtag}"
    params = {"limit": limit}

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    return response.json()

def extract_post_data(post: dict, query_hashtag: str) -> dict:
    """
    Extrahiere relevante Felder aus einem Post

    Args:
        post: Einzelner Post als Dictionary
        query_hashtag: Hashtag, über den der Post gefunden wurde

    Returns:
        Vereinfachtes Dictionary für Analyse
    """
    account = post.get("account", {})
    tags = [tag.get("name") for tag in post.get("tags", [])]

    return {
        "id": post.get("id"),
        "created_at": post.get("created_at"),
        "query_hashtag": query_hashtag,
        "username": account.get("acct"),
        "display_name": account.get("display_name"),
        "url": post.get("url"),
        "language": post.get("language"),
        "content_raw": post.get("content", ""),
        "text": clean_html(post.get("content", "")),
        "hashtags": ",".join(tags),
        "replies_count": post.get("replies_count"),
        "reblogs_count": post.get("reblogs_count"),
        "favourites_count": post.get("favourites_count"),
    }

def main() -> None:
    """
    Sammelt Posts zu mehreren Wien-bezogenen Hashtags und speichert sie als CSV
    """
    load_dotenv()

    instance = os.getenv("MASTODON_INSTANCE", "https://mastodon.social")

    hashtags = [
        "Wien",
        "Vienna",
        "Austria",
        "Österreich",
        "WienerLinien",
        "Klimakrise",
        "Hitzewelle",
    ]

    all_posts = []

    print(f"Verwendete Mastodon-Instanz: {instance}")
    print("-" * 80)

    for hashtag in hashtags:
        print(f"Lade Posts für #{hashtag} ...")

        try:
            posts = fetch_hashtag_posts(instance=instance, hashtag=hashtag, limit=40)
            for post in posts:
                all_posts.append(extract_post_data(post, query_hashtag=hashtag))

            print(f"Geladene Posts für #{hashtag}: {len(posts)}")

            #K Kurze Pause um öffentliche API nicht zu überlasten
            time.sleep(1)

        except requests.HTTPError as error:
            print(f"HTTP-Fehler bei #{hashtag}: {error}")
        except requests.RequestException as error:
            print(f"Request-Fehler bei #{hashtag}: {error}")

    df = pd.DataFrame(all_posts)

    # Duplkikate Beiträge entfernen, da ein Post mehrere Hashtags enthalten kann
    if not df.empty:
        df = df.drop_duplicates(subset="id")

    output_path = "data/raw/raw_mastodon_posts.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")

    print("-" * 80)
    print(f"Gespeicherte eindeutige Posts: {len(df)}")
    print(f"Datei gespeichert unter: {output_path}")
    print(
        f"Zeitpunkt der Erstellung: "
        f"{datetime.now().strftime('%d.%m.%Y %H:%M:%S')}"
    )

if __name__ == "__main__":
    main()