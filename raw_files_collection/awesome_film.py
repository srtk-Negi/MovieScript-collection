import re

import requests
from bs4 import BeautifulSoup

# Match any string enclosed within parentheses
SCRIPT_TYPE_MATCH = re.compile(r"\([^)]*\)", re.DOTALL)

# Match two or more consecutive white spaces
EXTRA_SPACES_MATCH = re.compile(r"\s{2,}", re.DOTALL)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}


# def get_movie_names_and_links_awesome_film(URL_AWESOME_FILM: str) -> dict:
#     """Fetch script titles and links and append to a dictionary."""
#     awesome_film_names_and_links = {}

#     content = requests.get(URL_AWESOME_FILM).text
#     soup = BeautifulSoup(content, "html.parser")

#     tables = soup.body.find_all("table")[15:18]
#     for table in tables:
#         tds = table.find_all("td", class_="tbl")

#         for td in tds:
#             try:
#                 movie_link = "http://www.awesomefilm.com/" + td.a["href"]
#             except:
#                 print(f"Movie Link {movie_link} did not work.")
#                 continue

#             movie_title = td.text.replace("\n", "").strip()
#             movie_title_2 = ""

#             if ":" in movie_title:
#                 movie_title_2 = movie_title.replace(":", ": ")

#             if movie_title.endswith(", The"):
#                 movie_title = movie_title.replace(", The", "")
#                 movie_title_2 = "The " + movie_title

#             if movie_title.endswith(", A"):
#                 movie_title = movie_title.replace(", A", "")
#                 movie_title_2 = "A " + movie_title

#             if movie_title.endswith(", An"):
#                 movie_title = movie_title.replace(", An", "")
#                 movie_title_2 = "An " + movie_title

#             if re.search(SCRIPT_TYPE_MATCH, movie_title):
#                 movie_title_2 = re.sub(SCRIPT_TYPE_MATCH, "", movie_title)

#             if re.search(EXTRA_SPACES_MATCH, movie_title):
#                 movie_title_2 = re.sub(EXTRA_SPACES_MATCH, " ", movie_title)

#             if movie_title.endswith("-"):
#                 movie_title_2 = movie_title[:-1]


#             if movie_title != "email" and movie_title != "":
#                 awesome_film_names_and_links[movie_title_2] = movie_link
#     return awesome_film_names_and_links


def get_movie_names_and_links_awesome_film(URL_AWESOME_FILM: str) -> dict:
    """Fetch script titles and links and append to a dictionary."""
    awesome_film_names_and_links = {}
    content = requests.get(URL_AWESOME_FILM).text
    soup = BeautifulSoup(content, "html.parser")

    tables = soup.body.find_all("table")[15:18]
    for table in tables:
        tds = table.find_all("td", class_="tbl")
        for td in tds:
            try:
                movie_link = "http://www.awesomefilm.com/" + td.a["href"]
            except Exception:
                movie_link = "Not Found"
            movie_title = td.text.replace("\n", "").strip()
            if ":" in movie_title:
                movie_title = movie_title.replace(":", ": ")
            if movie_title.endswith(", The"):
                movie_title = movie_title.replace(", The", "")
                movie_title = "The " + movie_title
            if movie_title.endswith(", A"):
                movie_title = movie_title.replace(", A", "")
                movie_title = "A " + movie_title
            if re.search(SCRIPT_TYPE_MATCH, movie_title):
                movie_title = re.sub(SCRIPT_TYPE_MATCH, "", movie_title).strip()
            if re.search(EXTRA_SPACES_MATCH, movie_title):
                movie_title = re.sub(EXTRA_SPACES_MATCH, " ", movie_title)
            if movie_title.endswith("-"):
                movie_title = movie_title[:-1].strip()
            if movie_title != "email" and movie_title != "":
                awesome_film_names_and_links[movie_title] = movie_link
    return awesome_film_names_and_links


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
    print(filename_2)
    return filename_2


def get_raw_files_awesome_film(AWESOME_FILM_URL: str) -> None:
    """Retrieve html structure from script links and write raw html to files."""
    try:
        awesome_film_names_and_links = get_movie_names_and_links_awesome_film(
            AWESOME_FILM_URL
        )
    except:
        print("Provided URL did not work for awesome film")
        return

    pdf_count = 0
    text_count = 0
    doc_count = 0
    rawfile_count = 0

    for movie_title, script_url in awesome_film_names_and_links.items():
        if script_url.lower().endswith(".pdf"):
            try:
                content = requests.get(script_url, headers=headers).content
            except:
                print(f"Could not get {script_url} for {movie_title} from awesome film")
                continue

            file_type = ".pdf"
            filename_2 = curate_filename(movie_title, file_type)

            with open(f"rawfiles/{filename_2}", "wb") as f:
                f.write(content)
                pdf_count += 1

        elif script_url.lower().endswith(".doc"):
            try:
                content = requests.get(script_url, headers=headers).content
            except:
                print(f"Could not get {script_url} for {movie_title} from awesome film")
                continue

            filename = ""
            for ch in movie_title.lower():
                if ch.isalnum() or ch == " ":
                    filename += ch
            filename_2 = "_".join(filename.strip().split()) + ".doc"

            with open(f"rawfiles/{filename_2}", "wb", encoding="utf-8") as f:
                f.write(content)
                doc_count += 1

        elif script_url.lower().endswith(".txt"):
            try:
                content = requests.get(script_url, headers=headers).content
                soup = BeautifulSoup(content, "html.parser")
            except:
                print(f"Could not get {script_url} for {movie_title} from awesome film")
                continue

            soup_str = str(soup)
            final_content = f"<html><body>{soup_str}</body></html>"

            file_type = ".html"
            filename_2 = curate_filename(movie_title, file_type)

            with open(f"rawfiles/{filename_2}", "w", encoding="utf-8") as f:
                f.write(final_content)
                text_count += 1

        else:
            try:
                content = requests.get(script_url, headers=headers)
                soup = BeautifulSoup(content.text, "html.parser")
            except:
                print(f"Could not get {script_url} for {movie_title} from awesome film")
                continue

            file_type = ".html"
            filename_2 = curate_filename(movie_title, file_type)

            with open(f"rawfiles/{filename_2}", "w", encoding="utf-8") as f:
                f.write(str(soup))
                rawfile_count += 1

    print(f"Total number of raw files collected from 'Awesome Film': {rawfile_count}")
    print(f"Total number of PDFs collected from 'Awesome Film': {pdf_count}")
    print(f"Total number of text files collected from 'Awesome Film': {text_count}")
    print(f"Total number of doc files collected from 'Awesome Film': {doc_count}")
