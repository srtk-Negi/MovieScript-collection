import re  # noqa: D100

import requests
from bs4 import BeautifulSoup

SCRIPT_TYPE_MATCH = re.compile(r"\([^)]*\)", re.DOTALL)
EXTRA_SPACES_MATCH = re.compile(r"\s{2,}", re.DOTALL)

movie_titles = []
content = requests.get("http://www.awesomefilm.com/").text
soup = BeautifulSoup(content, "html.parser")
with open("movie_script_testing.txt", "w") as f:
    tables = soup.body.find_all("table")[15:18]
    for table in tables:
        tds = table.find_all("td", class_="tbl")
        for td in tds:
            movie_title = td.text.replace("\n", "").strip()
            if ":" in movie_title:
                movie_title = movie_title.replace(":", ": ")
            if ", The" in movie_title:
                movie_title = movie_title.replace(", The", "")
                movie_title = "The " + movie_title
            if ", A" in movie_title:
                movie_title = movie_title.replace(", A", "")
                movie_title = "A " + movie_title
            if re.search(SCRIPT_TYPE_MATCH, movie_title):
                movie_title = re.sub(SCRIPT_TYPE_MATCH, "", movie_title).strip()
            if re.search(EXTRA_SPACES_MATCH, movie_title):
                movie_title = re.sub(EXTRA_SPACES_MATCH, " ", movie_title)
            if movie_title.endswith("-"):
                movie_title = movie_title[:-1].strip()
            if (
                "pdf" not in movie_title
                and "doc" not in movie_title
                and movie_title != "email"
                and movie_title != ""
            ):
                movie_titles.append(movie_title)
    movie_titles = list(set(movie_titles))
    print(movie_titles)
