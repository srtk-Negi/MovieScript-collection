import re

import requests
from bs4 import BeautifulSoup

# Match any string enclosed within parentheses
SCRIPT_TYPE_MATCH = re.compile(r"\([^)]*\)", re.DOTALL)
RE_TRANSCRIPT = re.compile(r"transcript", re.IGNORECASE)
RE_SCRIPT = re.compile(r"script", re.IGNORECASE)

# Match two or more consecutive white spaces
EXTRA_SPACES_MATCH = re.compile(r"\s{2,}", re.DOTALL)

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}


def get_movie_names_and_links_awesome_film(URL_AWESOME_FILM: str) -> dict:
    """Fetch script titles and links and append to a dictionary."""
    awesome_film_names_and_links = {}
    content = requests.get(URL_AWESOME_FILM, headers=headers)
    soup = BeautifulSoup(content.text, "html.parser")

    columns = soup.find_all("td", valign="top", align="center")
    table_rows = []

    for column in columns:
        table_rows.extend(column.find_all("tr"))
    del table_rows[-2:]

    for row in table_rows:
        movie_title = row.find("a").text
        movie_link = URL_AWESOME_FILM + row.find("a").get("href")

        movie_page = requests.get(movie_link, headers=headers)
        movie_soup = BeautifulSoup(movie_page.text, "html.parser")

        try:
            if "404" in movie_soup.find("title").string:
                continue
        except:
            pass

        movie_title = movie_title.replace("\n", "").strip()
        if ":" in movie_title:
            movie_title = movie_title.replace(":", ": ")

        if (
            movie_title.endswith(", The")
            or movie_title.endswith(", A")
            or movie_title.endswith(", An")
        ):
            movie_title = switch_article(movie_title.split(" ")[-1], movie_title)

        if re.search(SCRIPT_TYPE_MATCH, movie_title):
            movie_title = re.sub(SCRIPT_TYPE_MATCH, "", movie_title).strip()

        if re.search(EXTRA_SPACES_MATCH, movie_title):
            movie_title = re.sub(EXTRA_SPACES_MATCH, " ", movie_title)

        if movie_title.endswith("-"):
            movie_title = movie_title[:-1].strip()

        movie_title = re.sub(RE_TRANSCRIPT, "", movie_title).strip()
        movie_title = re.sub(RE_SCRIPT, "", movie_title).strip()

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
    return filename_2


def switch_article(article: str, movie_name: str) -> str:
    """Switches the position of the article of the movie name (The, An, A) from the end to the beginning (used as a helper function in get_movie_titles_and_years())

    Args:
        article (str): The article of the movie name
        movie_name (str): The movie name

    Returns:
        str: The movie name with the article at the beginning
    """
    new_name = movie_name.replace(f", {article}", "")
    movie_name = f"{article} " + new_name

    return movie_name


def get_raw_files_awesome_film(AWESOME_FILM_URL: str) -> list[str]:
    """Retrieve html structure from script links and write raw html to files."""
    try:
        awesome_film_names_and_links = get_movie_names_and_links_awesome_film(
            AWESOME_FILM_URL
        )
    except:
        with open("error_log.txt", "a", encoding="utf-8") as f:
            f.write("Provided URL did not work for awesome film\n")
        return

    MOVIE_NAMES = []

    pdf_count = 0
    doc_count = 0
    html_count = 0

    for movie_title, script_url in awesome_film_names_and_links.items():
        if script_url.lower().endswith(".pdf"):
            try:
                content = requests.get(script_url, headers=headers).content
            except:
                with open("error_log.txt", "a", encoding="utf-8") as f:
                    f.write(
                        f"Could not get {script_url} for {movie_title} from awesome film\n"
                    )
                continue

            MOVIE_NAMES.append(movie_title)
            file_type = ".pdf"
            filename_2 = curate_filename(movie_title, file_type)

            # with open(f"F:\Movie-Data-Collection\Rawfiles\{filename_2}", "wb") as f:
            with open(f"rawfiles/awesome_film/{filename_2}", "wb") as f:
                f.write(content)
                pdf_count += 1

        elif script_url.lower().endswith(".doc"):
            try:
                content = requests.get(script_url, headers=headers).content
            except:
                with open("error_log.txt", "a", encoding="utf-8") as f:
                    f.write(
                        f"Could not get {script_url} for {movie_title} from awesome film\n"
                    )
                continue

            MOVIE_NAMES.append(movie_title)
            file_type = ".doc"
            filename_2 = curate_filename(movie_title, file_type)

            # with open(f"F:\Movie-Data-Collection\Rawfiles\{filename_2}", "wb") as f:
            with open(f"rawfiles/awesome_film/{filename_2}", "wb") as f:
                f.write(content)
                doc_count += 1

        elif script_url.lower().endswith(".txt"):
            try:
                content = requests.get(script_url, headers=headers).content
                soup = BeautifulSoup(content, "html.parser")
            except:
                with open("error_log.txt", "a", encoding="utf-8") as f:
                    f.write(
                        f"Could not get {script_url} for {movie_title} from awesome film\n"
                    )
                continue

            soup_str = str(soup)
            final_content = f"<html><pre>{soup_str}</pre></html>"

            MOVIE_NAMES.append(movie_title)
            file_type = ".html"
            filename_2 = curate_filename(movie_title, file_type)

            with open(
                # f"F:\Movie-Data-Collection\Rawfiles\{filename_2}", "w", encoding="utf-8"
                f"rawfiles/awesome_film/{filename_2}",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(final_content)
                html_count += 1

        else:
            try:
                content = requests.get(script_url, headers=headers)
                soup = BeautifulSoup(content.text, "html.parser")
            except:
                with open("error_log.txt", "a", encoding="utf-8") as f:
                    f.write(
                        f"Could not get {script_url} for {movie_title} from awesome film\n"
                    )
                continue

            MOVIE_NAMES.append(movie_title)
            file_type = ".html"
            filename_2 = curate_filename(movie_title, file_type)

            with open(
                # f"F:\Movie-Data-Collection\Rawfiles\{filename_2}", "w", encoding="utf-8"
                f"rawfiles/awesome_film/{filename_2}",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(str(soup))
                html_count += 1

    print(f"Total number of html files collected from 'Awesome Film': {html_count}")
    print(f"Total number of PDFs collected from 'Awesome Film': {pdf_count}")
    print(f"Total number of doc files collected from 'Awesome Film': {doc_count}")

    return MOVIE_NAMES