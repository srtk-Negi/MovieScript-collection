"""Python script to get the names of all the movies from scriptslug.com in the form of a list."""
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.scriptslug.com/request/?pg="
MOVIE_NAMES = []


def get_movie_names_script_slug(doc: BeautifulSoup) -> list[str]:
    """Return a list of movie names from the scriptslug.com page."""
    movie_names = []
    name_type_list = (
        doc.find("div", class_="js-scripts-list")
        .find("div", class_="grid")
        .find_all("div", class_="h-5/6")
    )

    for item in name_type_list:
        show_type = item.find("p").string
        if "film" in show_type:
            movie_name = item.find("span").string.strip()
            if movie_name not in movie_names:
                movie_names.append(movie_name)
    return movie_names


def main():
    """The main method forms the URL for each page, gets the HTML, and calls the get_movie_names_from_script_slug method using a loop."""

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}

    for i in range(35):
        url = BASE_URL + str(i)
        page_html = requests.get(url, headers=headers)
        doc = BeautifulSoup(page_html.text, "html.parser")
        MOVIE_NAMES.extend(get_movie_names_script_slug(doc))

    print(MOVIE_NAMES)


if __name__ == "__main__":
    main()
