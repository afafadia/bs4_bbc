# Code to scrap website "https://www.bbc.com" using BeautifulSoup

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.bbc.com/"


def download_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return ""


def normalize_url(url):
    if len(url) == 0:
        return ""
    if url[0] == "/":
        return f"{BASE_URL}"
    return url


def parse_page(html):
    results = []
    item = {}
    soup = BeautifulSoup(html, "html.parser")
    for current in soup.find_all("a", class_="media__link"):
        if "href" in current.attrs:
            # results.append(normalize_url(current["href"]))
            results.append(current["href"])
    item["title"] = soup.title.text
    return list(set(results)), item


frontier = [BASE_URL]
visited = {}

if __name__ == "__main__":
    while len(frontier) > 0:
        url_to_fetch = frontier.pop()
        html = download_page(url_to_fetch)
        next_urls, item = parse_page(html)
        print(next_urls, item)

        visited[url_to_fetch] = 0
