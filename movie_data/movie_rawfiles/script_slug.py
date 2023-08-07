"""Script to collect the rawfiles (html of the movie pages) from the 'Script Slug' endpoint"""
import requests
from bs4 import BeautifulSoup
import re

re_year = re.compile("\d{4}")


def get_raw_script_slug(URL: str) -> None:
    """Function to get the movie name, year of release, link to rawfile and the rawfile.

    Args:
        URL (str): URL of the first page of the request endpoint of 'Script Slug' website
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    for i in range(35):
        url = URL + str(i)
        home_page_html = requests.get(url, headers=headers)
        home_page_data = BeautifulSoup(home_page_html.text, "html.parser")

        article_list = home_page_data.find("div", class_="js-scripts-list").find_all(
            "article"
        )

        for article in article_list:
            show_type = article.find("p").string

            if "film" in show_type.lower():
                try:
                    year = re.findall(re_year, show_type)[0]
                except IndexError:
                    year = None
                movie_name = article.find("span").string.strip()

                if (
                    movie_name.endswith(", The")
                    or movie_name.endswith(", A")
                    or movie_name.endswith(", An")
                ):
                    movie_name = switch_article(movie_name.split(" ")[-1], movie_name)

                link_to_movie_page = article.find("a").get("href")

                rawfile = requests.get(link_to_movie_page, headers=headers)
                rawfile_data = BeautifulSoup(rawfile.text, "html.parser")

                filename = ""
                for ch in movie_name.lower():
                    if ch.isalnum() or ch == " ":
                        filename += ch
                filename_2 = "_".join(filename.strip().split()) + ".html"

                with open(f"rawfiles/{filename_2}", "w") as outfile:
                    outfile.write(str(rawfile_data))


def switch_article(article: str, movie_name: str) -> str:
    """Switches the position of the article of the movie name (The, An, A) from the end to the beginning (used as a helper function in get_movie_title_and_year())

    Args:
        article (str): The article of the movie name
        movie_name (str): The movie name

    Returns:
        str: The movie name with the article at the beginning
    """
    print("here")
    new_name = movie_name.replace(f", {article}", "")
    movie_name = f"{article} " + new_name

    return movie_name
