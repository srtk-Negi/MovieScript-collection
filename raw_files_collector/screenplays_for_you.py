"""Script to collect the rawfiles (html of the movie pages) from the 'Screenplays For You' endpoint"""

import requests
from bs4 import BeautifulSoup
import re


def get_raw_screenplays_for_you(URL: str) -> list[str]:
    """Function to get the name of the movie, year of release, link to the movie page and rawfile (html of the movie page)

    Args:
        URL (str): URL of the scripts page (ALL) of 'Scripts For You' website
    """
    MOVIE_NAMES = []
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    try:
        page_data = requests.get(URL, headers=headers)
        home_page_html = BeautifulSoup(page_data.text, "html.parser")
    except:
        with open("error_log.txt", "a", encoding="utf-8") as outfile:
            outfile.write("The URL did not work for 'Scripts For You'\n")
        return

    movie_elements_p = home_page_html.find("div", class_="two-thirds").find_all("p")
    del movie_elements_p[0]

    html_count = 0
    pdf_count = 0
    for element in movie_elements_p:
        a_tag = element.find("a")
        movie_title, year = get_movie_title_and_year(a_tag)
        link_to_movie_page = get_link_to_movie_page(movie_title, a_tag, URL)

        if link_to_movie_page == "pdf":
            pdf_count += 1
            continue

        try:
            rawfile = requests.get(link_to_movie_page, headers=headers)
            rawfile_html = BeautifulSoup(rawfile.text, "html.parser")
        except:
            with open("error_log.txt", "a", encoding="utf-8") as outfile:
                outfile.write(
                    f"Could not get {link_to_movie_page} for {movie_title} from Screenplays For You\n"
                )
            continue

        MOVIE_NAMES.append(movie_title)

        filename = ""
        for ch in movie_title.lower():
            if ch.isalnum() or ch == " ":
                filename += ch
        filename_2 = "_".join(filename.strip().split()) + ".html"

        with open(
            # f"F:\Movie-Data-Collection\Rawfiles\{filename_2}", "w", encoding="utf-8"
            f"rawfiles/screenplays_for_you/{filename_2}",
            "w",
            encoding="utf-8",
        ) as outfile:
            outfile.write(str(rawfile_html))
        html_count += 1

    print(f"Total number of html files collected from 'Scripts For You': {html_count}")
    print(f"Total number of pdfs collected from 'Scripts For You': {pdf_count}")

    return MOVIE_NAMES


def get_link_to_movie_page(movie_title: str, a_tag: BeautifulSoup, URL: str) -> str:
    """Gets the link to the movie page

    Args:
        a_tag (BeautifulSoup): A beautifulsoup object that is an anchor tag containg the movie name and the link
        URL (str): URL of the scripts page (ALL) of 'Scripts For You' website

    Returns:
        str: link to the movie page
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    base_link = URL[:-8]
    link_to_movie_page = a_tag.get("href")

    if link_to_movie_page.lower().endswith(".pdf"):
        try:
            content = requests.get(link_to_movie_page, headers=headers).content
        except:
            return link_to_movie_page

        filename = ""
        for ch in movie_title.lower():
            if ch.isalnum() or ch == " ":
                filename += ch
        filename_2 = "_".join(filename.strip().split()) + ".pdf"

        # with open(f"F:\Movie-Data-Collection\Rawfiles\{filename_2}", "wb") as outfile:
        with open(f"rawfiles/screenplays_for_you/{filename_2}", "wb") as outfile:
            outfile.write(content)
        return "pdf"

    if link_to_movie_page.startswith("http"):
        link_to_movie_page = base_link + link_to_movie_page[14:]
    else:
        link_to_movie_page = base_link + link_to_movie_page

    return link_to_movie_page


def get_movie_title_and_year(a_tag: BeautifulSoup) -> tuple:
    """Gets the movie title and the year of release of the movie

    Args:
        a_tag (BeautifulSoup): A beautifulsoup object that is an anchor tag containg the movie name and the link

    Returns:
        tuple: movie_title, year
    """
    re_year = re.compile("\(\d{4}\)")
    re_transcript = re.compile("transcript")

    movie_title = a_tag.string

    try:
        year = re.findall(re_year, movie_title)[0][1:-1]
    except IndexError:
        year = None

    movie_title = re.sub(re_year, "", movie_title).strip()
    movie_title = re.sub(re_transcript, "", movie_title).strip()

    if (
        movie_title.endswith(", The")
        or movie_title.endswith(", A")
        or movie_title.endswith(", An")
    ):
        movie_title = switch_article(movie_title.split(" ")[-1], movie_title)

    return movie_title, year


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
