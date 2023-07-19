import re
import requests
from bs4 import BeautifulSoup

DATE_PATTERN = r"\d{4}(?:-\d{2})?|undated draft"


def get_movie_names_and_links_imsdb(URL_IMSDB: str) -> dict:
    """Extracts movie date and returns a dictionary of mapped titles and urls for imsdb."""
    movie_names_imsdb = []
    script_urls_imsdb = []

    scripts_content = requests.get(URL_IMSDB).text
    soup = BeautifulSoup(scripts_content, "html.parser")
    body = soup.find("body", id="mainbody")
    table = body.find_all("table")[1]
    td = table.find_all("td", valign="top")[1]
    p_tags = td.find_all("p")

    movie_title = ""
    movie_title_2 = ""
    date = ""

    for p_tag in p_tags:
        movie_title = p_tag.find("a").text
        match = re.findall(DATE_PATTERN, p_tag.text)

        if match:
            date = match[0]
        else:
            date = None

        if (
            movie_title.endswith(", The")
            or movie_title.endswith(", A")
            or movie_title.endswith(", An")
        ):
            movie_title = switch_article(movie_title.split(" ")[-1], movie_title)
        movie_names_imsdb.append(movie_title)
        print(f"Movie Name: {movie_title}\nMovie Date: {date}\n")

    for movie_title in movie_names_imsdb:
        if movie_title == "The Rage: Carrie 2":
            script_url = "https://imsdb.com/scripts/The-Rage-Carrie-2.html"

        elif movie_title == "The Avengers (2012)":
            script_url = "https://imsdb.com/scripts/Avengers,-The-(2012).html"

        else:
            if (
                "The" in movie_title
                and movie_title[:4] != "The "
                and ":" in movie_title
            ):
                movie_title_2 = movie_title.replace(":", "")
                movie_title_2 = movie_title.replace(" ", "-")

            else:
                if movie_title[:4] == "The ":
                    movie_title_2 = movie_title.replace("The ", "").strip()
                    movie_title_2 = movie_title + ", The"

                if ":" in movie_title:
                    movie_title_2 = movie_title.replace(":", "")

                if "&" in movie_title:
                    movie_title_2 = movie_title.replace("&", "%2526")

                if "?" in movie_title:
                    movie_title_2 = movie_title.replace("?", "")

                movie_title_2 = movie_title_2.replace(" ", "-")

            script_url = f"https://imsdb.com/scripts/{movie_title_2}.html"

        script_urls_imsdb.append(script_url)
    movie_names_and_links_imsdb = dict(zip(movie_names_imsdb, script_urls_imsdb))

    return movie_names_and_links_imsdb


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


def get_raw_files_imsdb(URL_IMSDB: str) -> None:
    """Retreive html structure from script links and write raw html to files."""
    try:
        movie_names_and_links_imsdb = get_movie_names_and_links_imsdb(URL_IMSDB)
    except:
        print("URL did not work for IMSDB.")
        return

    rawfile_count = 0

    for movie_title in movie_names_and_links_imsdb:
        script_url = movie_names_and_links_imsdb[movie_title]
        try:
            content = requests.get(script_url).text
            soup = BeautifulSoup(content, "html.parser")
        except:
            print(f"Could not get content for {movie_title} from IMSDB")
            continue

        file_type = ".html"
        filename_2 = curate_filename(movie_title, file_type)

        with open(f"rawfiles/{filename_2}", "a", encoding="utf-8") as f:
            f.write(str(soup).strip())
            rawfile_count += 1

    print(f"The number of raw files collected from IMSDB is {rawfile_count}")
