from time import sleep
import requests
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url: str, wait: int = 3) -> str:
    try:
        response = requests.get(
            url, headers={"user-agent": "Fake user-agent"}, timeout=wait
        )
        response.raise_for_status()
        sleep(1)
    except (requests.HTTPError, requests.ReadTimeout):
        return None
    else:
        return response.text


# Requisito 2
def scrape_novidades(html_content: str) -> list:
    return [
                link.css("a::attr(href)").get()
                for link in Selector(html_content).css("a.cs-overlay-link")
            ]


# Requisito 3
def scrape_next_page_link(html_content: str) -> str:
    if next_page := Selector(html_content).css("a.next"):
        return next_page.css("a::attr(href)").get()
    else:
        return None


# Requisito 4
def scrape_noticia(html_content: str) -> dict:
    select = Selector(html_content)

    return {
        "url": select.css("link[rel=canonical]::attr(href)").get(),
        "title": select.css("h1.entry-title::text").get().strip(),
        "timestamp": select.css("li.meta-date::text").get(),
        "writer": select.css("span.author a.url.fn.n::text").get(),
        "comments_count": len(select.css("ol.comment-list li").getall()),
        "summary": "".join(
            select.css("div.entry-content > p:nth-of-type(1) *::text")
            .getall()).strip(),
        "tags": select.css("a[rel=tag]::text").getall(),
        "category": select.css("span.label::text").get()
    }


# Requisito 5
def get_tech_news(amount: int):
    url = "https://blog.betrybe.com"
    tech_news = []

    while len(tech_news) <= amount:
        raw_data = fetch(url)
        news_url_list = scrape_novidades(raw_data)
        tech_news.extend(scrape_noticia(fetch(item)) for item in news_url_list)
        url = scrape_next_page_link(raw_data)

    create_news(tech_news[:amount])
    return tech_news[:amount]
