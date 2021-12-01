from selenium import webdriver
from bs4 import BeautifulSoup

def get_news():
    driver = webdriver.Chrome() # might need to set up some stuff for lambda
    URL = "https://www.insignia.vc/"

    driver.get(URL)
    source = driver.page_source
    driver.close()

    soup = BeautifulSoup(source, "html.parser")

    data = ""

    for i in soup.select(".py-5.container"):
        if "LATEST NEWS" in i.text: # latest news div
            data = i

    result = []

    for i in data.children:
        if not i.get("class"): # the news divs don't have classes for some reason
            children = i.findChildren("a", recursive=True)
            print(children[0],children[1])
            article = {
                "title": children[0].contents[0],
                "url": children[0]["href"],
                "publisher": children[1].contents[0],
            }
            result.append(article)

    return result