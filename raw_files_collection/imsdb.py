import requests
from bs4 import BeautifulSoup


def get_movie_names_and_urls_imsdb(URL_IMSDB: str) -> list:
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
        script_title = p_tag.find("a").text
        if script_title.endswith(", The"):
            script_title = script_title.replace(", The", "")
            script_title = "The " + script_title
        if script_title.endswith(", A"):
            script_title = script_title.replace(", A", "")
            script_title = "A " + script_title
        movie_names_imsdb.append(script_title)

    for script_title in movie_names_imsdb:
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
        script_urls_imsdb.append(script_url)

    movie_names_and_urls_imsdb = dict(zip(movie_names_imsdb, script_urls_imsdb))

    return movie_names_and_urls_imsdb
