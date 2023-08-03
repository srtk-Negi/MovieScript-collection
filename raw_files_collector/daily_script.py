import re
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
# FILEPATH = "F:/Movie-Data-Collection/daily_script"
FILEPATH = "rawfiles"


# date_patterns = [
#     r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},\s+\d{4}\b",
#     r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\b",
#     r"\b\d{4}\b",
# ]

re_year = r"\b\d{4}\b"


def get_movie_names_and_links_daily_script(URL_DAILY_SCRIPT: str) -> dict:
    """Fetch movie titles and script links, curate unique IDs, and return movie info."""
    daily_script_names_and_links = {}

    url_text = requests.get(URL_DAILY_SCRIPT).text
    soup = BeautifulSoup(url_text, "html.parser")

    previous_names = None
    script_list_info = soup.ul.find_all("p")

    for script_info in script_list_info:
        script_info_text = script_info.text
        by_index = script_info_text.lower().find("by")
        movie_title = script_info_text[:by_index].strip().replace("\xa0", "")

        match = ""
        date = ""

        for date_pattern in date_patterns:
            match = re.search(date_pattern, script_info_text, re.IGNORECASE)
            if match:
                date = match.group()
                break

        if match == "":
            date = None

        movie_title = f"{movie_title} [{date if date else movie_title}]"

        if movie_title != previous_names:
            movie_link_tag = script_info.find("a").get("href")
            movie_link = f"https://www.dailyscript.com/{movie_link_tag}"
            daily_script_names_and_links[movie_title] = movie_link

        previous_names = movie_title

    return daily_script_names_and_links


def curate_filename(movie_title: str, file_type: str) -> str:
    """Gets the filename for the rawfile

    Args:
        movie_name (str): The movie name
        file_type (str): The file type

    Returns:
        str: The filename for the rawfile"""

    filename = ""
    for ch in movie_title.lower():
        if ch.isalnum() or ch == " ":
            filename += ch
    filename_2 = "_".join(filename.strip().split()) + file_type
    return filename_2


def get_raw_files_daily_script(URL_DAILY_SCRIPT: str) -> dict:
    """Retreive html structure from script links and write raw html to files."""
    final_dict = {}
    try:
        daily_script_names_and_links_1 = get_movie_names_and_links_daily_script(
            URL_DAILY_SCRIPT
        )
    except:
        with open("error_log.txt", "a", encoding="utf-8") as outfile:
            outfile.write(
                f"The URL {URL_DAILY_SCRIPT} did not work for 'Daily Script'\n"
            )
        return

    url_nz = URL_DAILY_SCRIPT.replace(".html", "_n-z.html")
    try:
        daily_script_names_and_links_2 = get_movie_names_and_links_daily_script(url_nz)
        final_dict = {
            **daily_script_names_and_links_1,
            **daily_script_names_and_links_2,
        }
    except:
        with open("error_log.txt", "a", encoding="utf-8") as outfile:
            outfile.write(
                f"The URL {URL_DAILY_SCRIPT} did not work for 'Daily Script'\n"
            )
        return

    i = 0
    for movie_title, movie_link in final_dict.items():
        print(f"{movie_title} - {movie_link}")
        if i == 10:
            break
        i += 1

    return final_dict
