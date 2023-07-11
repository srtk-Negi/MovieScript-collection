import requests
from bs4 import BeautifulSoup

# Important Lists
movie_names_daily_script = []


def get_movie_names_daily_script(BASE_URL: str) -> list:
    """Fetch movie titles and script links, curate unique IDs, and return movie info."""
    url_text = requests.get(BASE_URL).text
    soup = BeautifulSoup(url_text, "html.parser")

    previous_names = None
    script_list_info = soup.ul.find_all("p")

    for script_info in script_list_info:
        script_info_text = script_info.text
        by_index = script_info_text.lower().find("by")
        title = script_info_text[:by_index].strip().replace("\xa0", "")
        if title != previous_names:
            movie_link_tag = script_info.find("a").get("href")
            movie_link = f"https://www.dailyscript.com/{movie_link_tag}"
            if ".html" in movie_link or ".htm" in movie_link or ".txt" in movie_link:
                movie_names_daily_script.append(title)
        previous_names = title
    return movie_names_daily_script
