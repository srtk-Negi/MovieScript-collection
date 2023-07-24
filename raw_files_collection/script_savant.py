import requests
from bs4 import BeautifulSoup


def get_raw_script_savant(URL_SCRIPT_SAVANT: str) -> list[str]:
    """Rewrites movie names and links from script savant to a file."""
    MOVIE_NAMES = []
    try:
        content = requests.get(URL_SCRIPT_SAVANT).text
        soup = BeautifulSoup(content, "html.parser")
    except:
        print("Provided URL did not work for script savant")
        return

    script_block = soup.find_all("td", align="left")[2]
    script_groupings = script_block.find_all("a")
    del script_groupings[0]

    pdf_count = 0
    for grouping in script_groupings:
        movie_link = "https://thescriptsavant.com/" + grouping["href"]
        movie_title = grouping.text

        if movie_title.endswith("Script"):
            movie_title = movie_title.replace(" Script", "")

        filename = get_filename(movie_title)

        with open(
            f"F:\Movie-Data-Collection\Rawfiles\{filename}", "a", encoding="utf-8"
        ) as f:
            f.write(f"{movie_title.strip()} - {movie_link}\n")
            pdf_count += 1

    print(f"Total number of PDFs collected from 'Script Savant': {pdf_count}")
    return MOVIE_NAMES


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
