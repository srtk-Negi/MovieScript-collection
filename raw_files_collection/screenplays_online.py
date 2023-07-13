"""Script to collect the rawfiles (html of the movie pages) from the 'Screenplays Online' endpoint"""

import requests
from bs4 import BeautifulSoup
import re

re_year = re.compile("\(\d{4}\)")

def get_raw_screenplays_online(URL: str) -> None:
    """Function to get the name of the movie, year of release, link to the movie page and rawfile (html of the movie page)
    
    Args: 
        URL (str): URL of the home page of 'Screenplays Online' website

    Returns:
        None
    """
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
    home_page_html = requests.get(URL, headers=headers)
    home_page_data = BeautifulSoup(home_page_html.text, "html.parser")
    table_rows = home_page_data.find("table", class_="screenplay-listing").find_all("tr")
    del table_rows[0]

    i = 0
    for row in table_rows:
        if i == 5:
            break
        i += 1
        movie_1, year_1, movie_2, year_2 = get_movie_names_and_years(row)
        link_1, link_2 = get_links_to_movie_pages(row, URL)

        rawfile_1 = requests.get(link_1, headers=headers)
        rawfile_html_1 = BeautifulSoup(rawfile_1.text, "html.parser")
        filename_1 = get_filename(movie_1)

        rawfile_2 = requests.get(link_2, headers=headers)
        rawfile_html_2 = BeautifulSoup(rawfile_2.text, "html.parser")
        filename_2 = get_filename(movie_2)

        with open(f"rawfiles/{filename_1}", "w", encoding="utf-8") as outfile:
            outfile.write(str(rawfile_html_1))
        
        with open(f"rawfiles/{filename_2}", "w", encoding="utf-8") as outfile:
            outfile.write(str(rawfile_html_2))


def get_movie_names_and_years(row: BeautifulSoup) -> tuple:
    """Gets the movie names and years of release from the table row
    
    Args:
        row (BeautifulSoup): A beautifulsoup object that is a table row
        
    Returns:
        tuple: movie_1, year_1, movie_2, year_2
    """
    movies_in_row = row.find_all("td")

    movie_1 = movies_in_row[1].find("a").string
    movie_2 = movies_in_row[6].find("a").string

    year_1, year_2 = get_year_of_release(movie_1, movie_2)

    movie_1 = re.sub(re_year, "", movie_1).strip()
    movie_2 = re.sub(re_year, "", movie_2).strip()

    if movie_1.endswith(", The") or movie_1.endswith(", A") or movie_1.endswith(", An"):
        movie_1 = switch_article(movie_1.split(" ")[-1], movie_1)

    if movie_2.endswith(", The") or movie_2.endswith(", A") or movie_2.endswith(", An"):
        movie_2 = switch_article(movie_2.split(" ")[-1], movie_2)

    return movie_1, year_1, movie_2, year_2


def get_links_to_movie_pages(row: BeautifulSoup, URL: str) -> tuple:
    """Gets the links to the movie pages

    Args:
        row (BeautifulSoup): A beautifulsoup object that is a table row
        URL (str): URL of the home page of 'Screenplays Online' website
    
    Returns:
        tuple: link_1, link_2
    """
    movies_in_row = row.find_all("td")

    link_1 = URL + movies_in_row[1].find("a").get("href")
    link_2 = URL + movies_in_row[6].find("a").get("href")

    return link_1, link_2


def get_year_of_release(movie_1: str, movie_2: str) -> tuple:
    """Gets the year of release of the movies
    
    Args:
        movie_1 (str): Name of the first movie
        movie_2 (str): Name of the second movie
        
    Returns:
        tuple: year_1, year_2
    """
    try:
        year_1 = re.findall(re_year, movie_1)[0][1:-1]
    except IndexError:
        year_1 = None

    try:
        year_2 = re.findall(re_year, movie_2)[0][1:-1]
    except IndexError:
        year_2 = None

    return year_1, year_2


def switch_article(article: str, movie_name: str) -> str:
    """Switches the position of the article of the movie name (The, An, A) from the end to the beginning
    
    Args:
        article (str): The article of the movie name
        movie_name (str): The movie name
        
    Returns:
        str: The movie name with the article at the beginning
    """
    new_name = movie_name.replace(f", {article}", "")
    movie_name = f"{article} " + new_name

    return movie_name


def get_filename(movie_name: str) -> str:
    """Gets the filename for the rawfile
    
    Args:
        movie_name (str): The movie name
    
    Returns:
        str: The filename for the rawfile"""
    char_list = ""
    for ch in movie_name.lower():
        if ch.isalnum() or ch == " ":
                char_list += ch
        filename = "_".join(char_list.strip().split()) + ".html"

    return filename