import time  # noqa: D100
import uuid

import pyodbc
import requests
from bs4 import BeautifulSoup

from config import Config
from dac_odbc import create_connection

config = Config()


def retrieve_imsdb_script_titles(url: str) -> list:
    """Retreive, refine, and return a list of movie titles from ismdb."""
    script_titles = []
    scripts_content = requests.get(url).text
    soup = BeautifulSoup(scripts_content, "html.parser")
    body = soup.find("body", id="mainbody")
    table = body.find_all("table")[1]
    td = table.find_all("td", valign="top")[1]
    p_tags = td.find_all("p")
    for p_tag in p_tags:
        script_title = p_tag.find("a").text
        if ", The" in script_title:
            script_title = script_title.replace(", The", "")
            script_title = "The " + script_title
        if ", A" in script_title:
            script_title = script_title.replace(", A", "")
            script_title = "A " + script_title
        script_titles.append(script_title)
    return script_titles


def generate_imsdb_script_ids(script_titles: list) -> list:
    """Generate and a return a list of script ids from movie titles."""
    script_ids = []
    for script_title in script_titles:
        script_title = script_title.replace("-", "")
        script_id = f"{uuid.uuid4().hex}_{script_title}"
        script_ids.append(script_id)
    return script_ids


def curate_imsdb_script_urls(script_titles: list) -> list:
    """Curate and return a list of valid urls from provided movie titles."""
    script_urls = []
    for script_title in script_titles:
        if script_title == "The Rage: Carrie 2":
            script_url = "https://imsdb.com/scripts/The-Rage-Carrie-2.html"
        elif script_title == "The Avengers (2012)":
            script_url = "https://imsdb.com/scripts/Avengers,-The-(2012).html"
        else:
            if (
                "The" in script_title
                and script_title[:4] != "The "
                and ":" in script_title
            ):
                script_title = script_title.replace(":", "")
                script_title = script_title.replace(" ", "-")
            else:
                if script_title[:4] == "The ":
                    script_title = script_title.replace("The ", "").strip()
                    script_title = script_title + ", The"
                if ":" in script_title:
                    script_title = script_title.replace(":", "")
                if "&" in script_title:
                    script_title = script_title.replace("&", "%2526")
                if "?" in script_title:
                    script_title = script_title.replace("?", "")
                script_title = script_title.replace(" ", "-")
            script_url = f"https://imsdb.com/scripts/{script_title}.html"
        script_urls.append(script_url)
    return script_urls


def extract_script_info(verified_script_url: str) -> str:
    """Extract script info from given url."""
    script_content = ""
    try:
        content = requests.get(verified_script_url).text
        soup = BeautifulSoup(content, "html.parser")
        script_block = soup.find_all("pre")[1]
        script_content = str(script_block.text.strip())
    except Exception:
        script_content = "First extraction process failed"

    if script_content == "First extraction process failed":
        try:
            content = requests.get(verified_script_url).text
            soup = BeautifulSoup(content, "html.parser")
            script_block = soup.find("pre")
            script_content = str(script_block.text.strip())
        except Exception:
            script_content = "Second extraction process failed"

    if script_content == "Second extraction process failed":
        try:
            content = requests.get(verified_script_url).text
            soup = BeautifulSoup(content, "html.parser")
            script_content = str(soup.find("td", class_="scrtext").text.strip())
        except Exception:
            script_content = "Third extraction process failed"

    if script_content == "Third extraction process failed":
        try:
            content = requests.get(verified_script_url).text
            soup = BeautifulSoup(content, "html.parser")
            script_block = soup.find("td", class_="scrtext")
            script_lines = script_block.find_all("font")
            for script_line in script_lines:
                script_line = script_line.text
                script_content += script_line
        except Exception:
            script_content = "Fourth extraction process failed"

    if script_content == "Fourth extraction process failed":
        verified_script_url = verified_script_url.replace("html", "pdf")
        content = requests.get(verified_script_url).text
        soup = BeautifulSoup(content, "html.parser")
        script_content = str(soup.body.h1.text.strip())

    return script_content


def insert_values(
    script_title: str, script_id: str, script_url: str, script_content: str
) -> None:
    """Insert values for script's title, id, url, and content within movie data table."""
    try:
        with create_connection(
            config.sand_db
        ) as connection, connection.cursor() as cursor:
            movie_table = config.movie_table
            sql = f"INSERT into {movie_table} values (?, ?, ?, ?)"
            cursor.execute(sql, script_title, script_id, script_url, script_content)
    except pyodbc.Error as error:
        print(error)
    time.sleep(0.001)


def imsdb() -> list:
    """Perform necessary to extract scripts from imsdb and returna  list of the valid script titles."""
    verified_imsdb_script_titles = []
    script_titles = retrieve_imsdb_script_titles("https://imsdb.com/all-scripts.html")
    script_ids = generate_imsdb_script_ids(script_titles)
    script_urls = curate_imsdb_script_urls(script_titles)
    for script_title, script_id, script_url in zip(
        script_titles,
        script_ids,
        script_urls,
    ):
        script_content = extract_script_info(script_url)
        if script_content != "Not Found" and script_content != "":
            insert_values(script_title, script_id, script_url, script_content)
            verified_imsdb_script_titles.append(script_title)
    return verified_imsdb_script_titles


def main() -> None:
    """Call functions above."""
    verified_imsdb_script_titles = imsdb()
    verified_imsdb_script_titles = list(set(verified_imsdb_script_titles))
    print(verified_imsdb_script_titles)


if __name__ == "__main__":
    main()
