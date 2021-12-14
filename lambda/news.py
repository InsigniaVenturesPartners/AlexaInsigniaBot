import requests
import datetime

URL = "https://www.insignia.vc/startup_info/data.json"

def get_news():
    response = requests.get(URL)
    response_json = response.json()

    companies = response_json["portfolios"]
    articles = []
    for company in companies:
        articles.append(
            {
                "title": company["public_info"]["external_article_title"],
                "source": company["public_info"]["external_article_source"],
                "url": company["public_info"]["external_article_link"],
                "date": company["public_info"]["external_article_date"],
            }
        )

    articles.sort(
        key=lambda article: datetime.datetime.strptime(article["date"] or "1970-01-01","%Y-%m-%d"),
        reverse=True
    )

    return articles
