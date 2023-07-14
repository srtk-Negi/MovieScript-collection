import requests
from bs4 import BeautifulSoup


def get_movie_names_and_links_imsdb(URL_IMSDB: str) -> dict:
    """Retreive, refine, and return a dictionary of mapped titles and urls for imsdb."""
    movie_names_imsdb = []
    script_urls_imsdb = []
    scripts_content = requests.get(URL_IMSDB).text
    soup = BeautifulSoup(scripts_content, "html.parser")
    body = soup.find("body", id="mainbody")
    table = body.find_all("table")[1]
    td = table.find_all("td", valign="top")[1]
    p_tags = td.find_all("p")
    for p_tag in p_tags:
        movie_title = p_tag.find("a").text
        if movie_title.endswith(", The"):
            movie_title = movie_title.replace(", The", "")
            movie_title = "The " + movie_title
        if movie_title.endswith(", A"):
            movie_title = movie_title.replace(", A", "")
            movie_title = "A " + movie_title
        movie_names_imsdb.append(movie_title)
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
                movie_title = movie_title.replace(":", "")
                movie_title = movie_title.replace(" ", "-")
            else:
                if movie_title[:4] == "The ":
                    movie_title = movie_title.replace("The ", "").strip()
                    movie_title = movie_title + ", The"
                if ":" in movie_title:
                    movie_title = movie_title.replace(":", "")
                if "&" in movie_title:
                    movie_title = movie_title.replace("&", "%2526")
                if "?" in movie_title:
                    movie_title = movie_title.replace("?", "")
                movie_title = movie_title.replace(" ", "-")
            script_url = f"https://imsdb.com/scripts/{movie_title}.html"
        script_urls_imsdb.append(script_url)
    movie_names_and_links_imsdb = dict(zip(movie_names_imsdb, script_urls_imsdb))
    return movie_names_and_links_imsdb


def get_raw_files_imsdb(movie_names_and_links_imsdb: dict) -> None:
    """Retreive html structure from script links and write raw html to files."""
    for movie_title in movie_names_and_links_imsdb:
        script_url = movie_names_and_links_imsdb[movie_title]
        content = requests.get(script_url).text
        soup = BeautifulSoup(content, "html.parser")
        file_name = "_".join(movie_title.strip().split())
        with open(f"rawfiles/{file_name}", "w", encoding="utf-8") as f:
            f.write(str(soup).strip())
