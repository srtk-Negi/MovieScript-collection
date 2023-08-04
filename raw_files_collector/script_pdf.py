"""Script to get the name of the movie and the link to the pdf of the script from the 'Script PDFs' endpoint
and write it to a file"""
import requests
from bs4 import BeautifulSoup
import re
from movie import Movie


def get_movies_script_pdf(URL: str) -> list[Movie]:
    """Function to get the name of the movie and the link to the pdf of the script from the 'Script PDFs' endpoint

    Args:
        URL (str): URL of the 'Script PDFs' endpoint
    """
    movies = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    re_year = re.compile(r"\(\d{4}\)")

    try:
        home_page_html = requests.get(URL, headers=headers)
        home_page_data = BeautifulSoup(home_page_html.text, "html.parser")
    except:
        with open("error_log.txt", "a", encoding="utf-8") as outfile:
            outfile.write("The URL did not work for 'Script PDFs'\n")
        return

    sections = home_page_data.find("div", class_="entry-content").find_all("ul")
    del sections[-1]

    for section in sections:
        li_tags = section.find_all("li")
        for li_tag in li_tags:
            movie_title = li_tag.find("a").text
            script_url = li_tag.find("a").get("href")

            try:
                movie_year = re.findall(re_year, movie_title)[0][1:-1]
                movie_title = re.sub(re_year, "", movie_title).strip()
            except IndexError:
                movie_year = None

            if (
                movie_title.endswith(", The")
                or movie_title.endswith(", A")
                or movie_title.endswith(", An")
            ):
                movie_title = switch_article(movie_title.split(" ")[-1], movie_title)

            movies.append(
                Movie(title=movie_title, script_url=script_url, movie_year=movie_year)
            )

    return movies


def switch_article(article: str, movie_name: str) -> str:
    """Switches the position of the article of the movie name (The, An, A) from the end to the beginning (used as a helper function in get_movie_title_and_year())

    Args:
        article (str): The article of the movie name
        movie_name (str): The movie name

    Returns:
        str: The movie name with the article at the beginning
    """
    new_name = movie_name.replace(f", {article}", "")
    movie_name = f"{article} " + new_name

    return movie_name
