import re
import requests
from bs4 import BeautifulSoup
from .movie import Movie
from .helper_functions import switch_article, get_file_type

re_script_date = re.compile(r"\((\b\d{4}(?:-\d{2})?\b)")
re_year = re.compile(r"\(\d{4}\)")

MOVIE_PAGE_URL = "https://imsdb.com/Movie%20Scripts/"
MOVIE_SCRIPT_URL = "https://imsdb.com/"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}

month_dict = {
    "00": "January",
    "01": "January",
    "02": "February",
    "03": "March",
    "04": "April",
    "05": "May",
    "06": "June",
    "07": "Jule",
    "08": "August",
    "09": "September",
    "10": "October",
    "11": "November",
    "12": "December",
    "13": "December",
    "19": "December",
}


def get_movies_imsdb(URL_IMSDB: str) -> list[Movie]:
    """Get movies from IMSDB and return a list of Movie objects

    Args:
        URL_IMSDB (str): URL of IMSDB

    Returns:
        list[Movie]: List of Movie objects
    """
    movies = []
    try:
        scripts_content = requests.get(URL_IMSDB, headers=headers)
        soup = BeautifulSoup(scripts_content.text, "html.parser")
    except:
        with open("error_log.txt", "a", encoding="utf-8") as f:
            f.write(f"URL did not work for IMSDB\n")

    body = soup.find("body")

    table = body.find_all("table")[1]
    td = table.find_all("td", valign="top")[1]
    p_tags = td.find_all("p")

    for p_tag in p_tags:
        movie_title = p_tag.find("a").text
        movie_page = MOVIE_PAGE_URL + p_tag.find("a").get("href")
        writers = p_tag.find("i").string.replace("Written by", "").strip()

        movie_title = re.sub(re_year, "", movie_title).strip()
        script_date_match = re_script_date.search(p_tag.text)

        if script_date_match:
            script_date = script_date_match.group(1)
            try:
                if "-" in script_date:
                    script_date = script_date.split("-")
                    script_date = f"{month_dict[script_date[1]]} {script_date[0]}"
            except:
                print(f"{movie_title} from IMSDB has a date format error")
                continue
        else:
            script_date = None

        if (
            movie_title.endswith(", The")
            or movie_title.endswith(", A")
            or movie_title.endswith(", An")
        ):
            movie_title = switch_article(movie_title.split(" ")[-1], movie_title)

        try:
            movie_page_html = requests.get(movie_page, headers=headers)
            movie_page_soup = BeautifulSoup(movie_page_html.text, "html.parser")
        except:
            continue

        try:
            movie_script_link = MOVIE_SCRIPT_URL + (
                movie_page_soup.find("table", class_="script-details")
                .find_all("a")[-1]
                .get("href")
            )
        except:
            continue

        filetype = get_file_type(movie_script_link)

        movies.append(
            Movie(
                title=movie_title,
                script_url=movie_script_link,
                file_type=filetype,
                script_date=script_date,
                writers=writers,
            )
        )

    print(f"IMSDB: {len(movies)} movies found.")
    return movies
