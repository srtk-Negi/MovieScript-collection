import re
import requests
from bs4 import BeautifulSoup

IMSDB_DATE_PATTERN = r"\d{4}(?:-\d{2})?|undated draft"
YEAR_PATTERN = r"\(\d{4}\)"

MOVIE_PAGE_URL = "https://imsdb.com/Movie%20Scripts/"
MOVIE_SCRIPT_URL = "https://imsdb.com/"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}


def get_movie_names_and_links_imsdb(URL_IMSDB: str) -> dict:
    """Extracts movie date and returns a dictionary of mapped titles and urls for imsdb."""
    name_link_dict = {}

    scripts_content = requests.get(URL_IMSDB, headers=headers)
    soup = BeautifulSoup(scripts_content.text, "html.parser")

    body = soup.find("body")

    table = body.find_all("table")[1]
    td = table.find_all("td", valign="top")[1]
    p_tags = td.find_all("p")

    for p_tag in p_tags:
        movie_title = p_tag.find("a").text
        movie_page = MOVIE_PAGE_URL + p_tag.find("a").get("href")

        movie_title = re.sub(YEAR_PATTERN, "", movie_title).strip()
        match = re.findall(IMSDB_DATE_PATTERN, p_tag.text)
        date = match[0] if match else None

        if (
            movie_title.endswith(", The")
            or movie_title.endswith(", A")
            or movie_title.endswith(", An")
        ):
            movie_title = switch_article(movie_title.split(" ")[-1], movie_title)

        try:
            movie_page_html = requests.get(movie_page, headers=headers)
            movie_page_soup = BeautifulSoup(movie_page_html.text, "html.parser")
        except:
            print(f"Cant get {movie_title} page")
            continue

        try:
            movie_script_link = MOVIE_SCRIPT_URL + (
                movie_page_soup.find("table", class_="script-details")
                .find_all("a")[-1]
                .get("href")
            )
        except:
            print(f"Cant get {movie_title} script")
            continue

        name_link_dict[movie_title] = movie_script_link
    return name_link_dict


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


def get_raw_files_imsdb(URL_IMSDB: str) -> list[str]:
    """Retreive html structure from script links and write raw html to files."""
    # try:
    movie_names_and_links_imsdb = get_movie_names_and_links_imsdb(URL_IMSDB)
    # except:
    #     with open("error_log.txt", "a", encoding="utf-8") as outfile:
    #         outfile.write("URL did not work for IMSDB\n")
    #     return

    MOVIE_NAMES = []
    # html_count = 0

    for movie_title, movie_link in movie_names_and_links_imsdb.items():
        with open("test.txt", "a", encoding="utf-8") as outfile:
            outfile.write(f"{movie_title} - {movie_link}\n")
    #     script_url = movie_names_and_links_imsdb[movie_title]
    #     try:
    #         content = requests.get(script_url).text
    #         soup = BeautifulSoup(content, "html.parser")
    #     except:
    #         with open("error_log.txt", "a", encoding="utf-8") as outfile:
    #             outfile.write(
    #                 f"Could not get {script_url} for {movie_title} from IMSDB\n"
    #             )
    #         continue

    #     MOVIE_NAMES.append(movie_title)
    #     file_type = ".html"
    #     filename_2 = curate_filename(movie_title, file_type)

    #     with open(f"rawfiles/imsdb/{filename_2}", "w", encoding="utf-8") as f:
    #         f.write(str(soup).strip())
    #         html_count += 1

    # print(f"Total number of html files collected from IMSDB {html_count}")

    return MOVIE_NAMES
