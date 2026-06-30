"""
Test der Verbindung zur Mastodon API

Dieses Skript ruft öffentliche Beiträge zu einem Hashtag ab.
Für diesen Test wird kein Access Token benötigt, weil öffentliche
Hashtag-Timelines via REST-API abrufbar sind.
"""

import os
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

def main() -> None:
    """
    Ruft testweise öffentliche Beiträge mit dem Hashtag #Wien ab
    und gibt die wichtigsten Informationen im Terminal aus.
    """

    load_dotenv()

    instance = os.getenv("MASTODON_INSTANCE", "https://mastodon.social")
    hashtag = "Wien"

    url = f"{instance}/api/v1/timelines/tag/{hashtag}"

    params = {
        "limit": 10
    }

    print(f"Teste Mastodon-Instanz: {instance}")
    print(f"Hashtag: #{hashtag}")
    print("-" * 80)

    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()

    posts = response.json()

    print(f"Anzahl geladender Posts: {len(posts)}")
    print("-" * 80)

    for post in posts:
        # HTML Content bereinigen
        text = clean_html(post.get("content", ""))
        account = post.get("account", {})
        username = account.get("acct", "unknown")
        tags = [tag.get("name") for tag in post.get("tags", [])]

        print(f"Zeitpunkt: {post.get('created_at')}")
        print(f"User: {username}")
        print(f"Hashtags: {tags}")
        print(f"Text: {text}")
        print(f"URL: {post.get('url')}")
        print("-" * 80)

if __name__ == "__main__":
    main()