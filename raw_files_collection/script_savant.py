import requests
from bs4 import BeautifulSoup


def get_raw_script_savant(URL_SCRIPT_SAVANT: str) -> None:
    """Rewrites movie names and links from script savant to a file."""
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

        with open("rawfiles/script_savant.txt", "a", encoding="utf-8") as f:
            f.write(f"{movie_title.strip()} - {movie_link}\n")
            pdf_count += 1

    print(f"Total number of PDFs collected from 'Script Savant': {pdf_count}")
