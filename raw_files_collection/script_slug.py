import requests
from bs4 import BeautifulSoup


def get_raw_script_slug(URL: str) -> None:
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    for i in range(1):
        url = URL + str(i)
        home_page_html = requests.get(url, headers=headers)
        home_page_data = BeautifulSoup(home_page_html.text, "html.parser")

        article_list = home_page_data.find("div", class_="js-scripts-list").find_all(
            "article"
        )

        for article in article_list:
            show_type = article.find("p").string
            if "film" in show_type.lower():
                link_to_script_page = article.find("a").get("href")
                movie_name = article.find("span").string
                print(f"Name - {movie_name.strip()}\t\t\tLink - {link_to_script_page}")
