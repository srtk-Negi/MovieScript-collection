import requests
from bs4 import BeautifulSoup


def get_movie_names_and_links_daily_script(BASE_URL: str) -> dict:
    """Fetch movie titles and script links, curate unique IDs, and return movie info."""
    daily_script_names_and_links = {}
    url_text = requests.get(BASE_URL).text
    soup = BeautifulSoup(url_text, "html.parser")
    previous_names = None
    script_list_info = soup.ul.find_all("p")
    for script_info in script_list_info:
        script_info_text = script_info.text
        by_index = script_info_text.lower().find("by")
        movie_title = script_info_text[:by_index].strip().replace("\xa0", "")
        if movie_title != previous_names:
            movie_link_tag = script_info.find("a").get("href")
            movie_link = f"https://www.dailyscript.com/{movie_link_tag}"
            daily_script_names_and_links[movie_title] = movie_link
        previous_names = movie_title
    return daily_script_names_and_links


def get_raw_files_daily_script(daily_script_names_and_links: dict) -> None:
    """Retreive html structure from script links and write raw html to files."""
    for movie_title in daily_script_names_and_links:
        script_url = daily_script_names_and_links[movie_title]
        soup = ""
        if ".doc" in script_url or ".pdf" in script_url:
            soup = script_url
        else:
            content = requests.get(script_url).text
            soup = BeautifulSoup(content, "html.parser")
        if "/" in movie_title:
            movie_title = movie_title.replace("/"), "_"
        file_name = "_".join(movie_title.strip().split())
        with open(f"rawfiles/{file_name}", "w", encoding="utf-8") as f:
            f.write(str(soup).strip())
