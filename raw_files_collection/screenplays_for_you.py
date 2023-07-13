"""Script to collect the rawfiles (html of the movie pages) from the 'Screenplays For You' endpoint"""

import requests
from bs4 import BeautifulSoup
import re


def get_raw_screenplays_for_you(URL: str):
    """Function to get the name of the movie, year of release, link to the movie page and rawfile (html of the movie page)

    Args:
        URL (str): URL of the scripts page (ALL) of 'Scripts For You' website
    """ 
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    page_data = requests.get(URL, headers=headers)
    home_page_html = BeautifulSoup(page_data.text, "html.parser")

    movie_elements_p = home_page_html.find("div", class_="two-thirds").find_all("p")
    del movie_elements_p[0]

    i = 0
    for element in movie_elements_p:
        if i == 10:
            break
        i += 1
        a_tag = element.find("a")
        movie_title, date = get_movie_title_and_date(a_tag)
        link_to_movie_page = get_link_to_movie_page(a_tag, URL)

        rawfile = requests.get(link_to_movie_page, headers=headers)
        rawfile_html = BeautifulSoup(rawfile.text, "html.parser")

        filename = ""
        for ch in movie_title.lower():
            if ch.isalnum() or ch == " ":
                filename += ch
        filename_2 = "_".join(filename.strip().split()) + ".html"

        with open(f"../rawfiles/{filename_2}", "w", encoding="utf-8") as outfile:
            outfile.write(str(rawfile_html))


def get_link_to_movie_page(a_tag: BeautifulSoup, URL: str) -> str:
    """Gets the link to the movie page

    Args:
        a_tag (BeautifulSoup): A beautifulsoup object that is an anchor tag containg the movie name and the link
        URL (str): URL of the scripts page (ALL) of 'Scripts For You' website

    Returns:
        str: link to the movie page
    """  
    base_link = URL[:-8]
    link_to_movie_page = a_tag.get("href")
    if link_to_movie_page.startswith("http"):
        link_to_movie_page = base_link + link_to_movie_page[14:]
    else:
        link_to_movie_page = base_link + link_to_movie_page

    return link_to_movie_page


def get_movie_title_and_date(a_tag: BeautifulSoup) -> tuple:
    """Gets the movie title and the year of release of the movie

    Args:
        a_tag (BeautifulSoup): A beautifulsoup object that is an anchor tag containg the movie name and the link

    Returns:
        tuple: Movie title and year
    """
    re_year = re.compile("\(\d{4}\)")
    re_transcript = re.compile("transcript")

    movie_title = a_tag.string

    date = re.findall(re_year, movie_title)[0][1:-1]

    movie_title = re.sub(re_year, "", movie_title).strip()
    movie_title = re.sub(re_transcript, "", movie_title).strip()

    if movie_title.endswith(", The"):
        new_name = movie_title.replace(", The", "")
        movie_title = "The " + new_name

    return movie_title, date
