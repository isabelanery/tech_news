from time import sleep
import requests
from parsel import Selector


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
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
