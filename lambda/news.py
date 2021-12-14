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
    # data = [company["public_info"] for company in companies]
    # articles = [
    #     {
    #         "title": item["external_article_title"],
    #         "source": item["external_article_source"],
    #         "url": item["external_article_link"],
    #         "date": item["external_article_date"],
    #     }
    #     for item in data
    # ]

    articles.sort(
        key=lambda article: datetime.datetime.strptime(article["date"] or "1970-01-01","%Y-%m-%d"),
        reverse=True
    )
    print(articles)

    return articles
