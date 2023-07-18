import re  # noqa: D100

import requests
from bs4 import BeautifulSoup

SCRIPT_TYPE_MATCH = re.compile(r"\([^)]*\)", re.DOTALL)
EXTRA_SPACES_MATCH = re.compile(r"\s{2,}", re.DOTALL)


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
            soup = f"{movie_title}: {script_url}"
            with open("rawfiles/awesome_films_pdfs.txt", "a", encoding="utf-8") as f:
                soup = soup.strip()
                f.write(f"{soup}\n")
                pdf_count += 1

        elif script_url.lower().endswith(".doc"):
            with open(f"rawfiles/awesome_films_docs.txt", "a", encoding="utf-8") as f:
                f.write(f"{movie_title}: {script_url}\n")
                doc_count += 1

        elif script_url.lower().endswith(".txt"):
            with open(f"rawfiles/awesome_films_text.txt", "a", encoding="utf-8") as f:
                f.write(f"{movie_title}: {script_url}\n")
                text_count += 1

        else:
            try:
                content = requests.get(script_url)
                soup = BeautifulSoup(content.text, "html.parser")
            except:
                print(f"Could not get {script_url} for {movie_title} from awesome film")
                continue

            filename = ""
            for ch in movie_title.lower():
                if ch.isalnum() or ch == " ":
                    filename += ch
            filename_2 = "_".join(filename.strip().split()) + ".html"

            with open(f"rawfiles/{filename_2}", "a", encoding="utf-8") as f:
                f.write(str(soup))
                rawfile_count += 1

    print(f"Total number of raw files collected from 'Awesome Film': {rawfile_count}")
    print(f"Total number of PDFs collected from 'Awesome Film': {pdf_count}")
    print(f"Total number of text files collected from 'Awesome Film': {text_count}")
    print(f"Total number of doc files collected from 'Awesome Film': {doc_count}")
