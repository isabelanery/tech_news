from tech_news.database import search_news
from datetime import datetime


# Requisito 6
def search_by_title(title):
    return [
        (news["title"], news["url"])
        for news in search_news(
            {"title": {"$regex": title, "$options": "i"}}
        )
    ]


# Requisito 7
def search_by_date(date):
    try:
        new_date = datetime.strptime(date, "%Y-%m-%d").strftime("%d/%m/%Y")
        return [
            (news["title"], news["url"])
            for news in search_news({"timestamp": new_date})
        ]

    except ValueError as e:
        raise ValueError("Data inválida") from e


# Requisito 8
def search_by_tag(tag):
    return [
        (news["title"], news["url"])
        for news in search_news({"tags": {"$regex": tag, "$options": "i"}})
    ]


# Requisito 9
def search_by_category(category):
    return [
        (news["title"], news["url"])
        for news in search_news({"category": {"$regex": category, "$options": "i"}})
    ]
