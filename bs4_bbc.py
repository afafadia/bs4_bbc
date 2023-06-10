import json

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.bbc.com/"
tags = []


def download_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""


def normalize_url(url):
    if len(url) == 0:
        return ""
    if url[0] == "/":
        return f"{BASE_URL[:-1]}{url}"
    return url


def parse_page(html):
    results = []
    item = {}
    soup = BeautifulSoup(html, "html.parser")
    for current in soup.find_all("a", class_="media__link"):
        if "href" in current.attrs:
            results.append(normalize_url(current["href"]))
        tags.append(current.find_next().text.strip())

    item["title"] = soup.title.text
    for url in list(set(results)):
        yield url


def parse_articles(next_urls):
    results = []
    try:
        for i, (url, tag) in enumerate(zip(next_urls, tags)):
            html = download_page(url)
            soup = BeautifulSoup(html, "html.parser")
            title_list = soup.css.select("h1")
            title = title_list[0] if title_list else ""
            image = soup.find("meta", property="og:image")["content"]

            results.append(
                {
                    # "id": (i + 1),
                    "page_title": title.text.strip() if title.text else "",
                    "image": image if "live" not in url else "LIVE PAGE",
                    "url": url,
                    "tag": tag,
                }
            )

        print(json.dumps(results, indent=4))

    except StopIteration:
        pass


frontier = [BASE_URL]
visited = {}

if __name__ == "__main__":
    while len(frontier) > 0:
        url_to_fetch = frontier.pop()
        html = download_page(url_to_fetch)
        parse_articles(parse_page(html))

        visited[url_to_fetch] = 0
