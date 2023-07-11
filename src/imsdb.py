import requests
from bs4 import BeautifulSoup


def get_movie_names_imsdb(URL_IMSDB: str) -> list:
    """Retreive, refine, and return a list of movie titles from ismdb."""
    movie_names_imsdb = []
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
    return movie_names_imsdb
