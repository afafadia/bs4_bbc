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
        return f"https://www.bbc.com{url}"
    return url


def parse_page(html):
    results = []
    item = {}
    soup = BeautifulSoup(html, "html.parser")
    for current in soup.find_all("a", class_="media__link"):
        if "href" in current.attrs:
            results.append(normalize_url(current["href"]))
    item["title"] = soup.title.text
    for url in list(set(results)):
        yield url


def parse_articles(next_urls):
    results = []
    try:
        for i, url in enumerate(next_urls):
            html = download_page(url)
            soup = BeautifulSoup(html, "html.parser")
            title = soup.css.select("h1")[0]

            results.append(
                {
                    "id": (i + 1),
                    "heading": title.text.strip() if title.text else "",
                }
            )

        # results = [result.text.strip() if result.text else "" for result in results]
        print(results)
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
