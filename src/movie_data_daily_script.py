import uuid

import requests
from bs4 import BeautifulSoup

# Important Lists
movie_titles = []
movie_ids = []
movie_links = []
movie_info_list = []


def generate_unique_id(title: str):
    """Generate a unique id for each movie title."""
    formatted_title = title.replace(" ", "-")
    unique_id = f"{uuid.uuid4().hex}_{formatted_title}"
    return unique_id


def get_movie_info(url: str) -> list:
    """Fetch movie titles and script links, curate unique IDs, and return movie info."""
    url_text = requests.get(url).text
    soup = BeautifulSoup(url_text, "html.parser")

    previous_title = None
    script_list_info = soup.ul.find_all("p")

    for script_info in script_list_info:
        script_info_text = script_info.text
        by_index = script_info_text.lower().find("by")
        title = script_info_text[:by_index].strip().replace("\xa0", "")
        if title != previous_title:
            movie_link_tag = script_info.find("a").get("href")
            movie_link = f"https://www.dailyscript.com/{movie_link_tag}"
            if ".html" in movie_link or ".htm" in movie_link or ".txt" in movie_link:
                movie_titles.append(title)
                movie_ids.append(generate_unique_id(title))
                movie_links.append(movie_link)
        previous_title = title

    movie_info_list.append(movie_titles)
    movie_info_list.append(movie_ids)
    movie_info_list.append(movie_links)
    return movie_info_list


def get_movie_scripts(movie_link: str) -> str:
    """Retrieve the script content from the movie link."""
    script = ""
    if ".html" in movie_link:
        script_url_text = requests.get(movie_link).text
        soup = BeautifulSoup(script_url_text, "html.parser")
        try:
            if soup.find("pre"):
                try:
                    script = soup.body.find("pre").get_text().strip()
                except Exception:
                    script = soup.find("pre").get_text().strip()
            elif soup.find("p"):
                for p_tag in soup.find_all("p"):
                    p_tag.unwrap()
                script = soup.get_text().strip()
        except Exception:
            script = ".html NOT FOUND"
    elif ".htm" in movie_link:
        script_url_text = requests.get(movie_link).text
        soup = BeautifulSoup(script_url_text, "html.parser")
        try:
            if soup.find("blockquote"):
                script = soup.find("blockquote").get_text().strip()
            elif soup.find("pre"):
                try:
                    script = soup.body.find("pre").get_text().strip()
                except Exception:
                    script = soup.find("pre").get_text().strip()
        except Exception:
            script = ".htm not found"
    elif ".txt" in movie_link:
        try:
            script_url_text = requests.get(movie_link).text
            soup = BeautifulSoup(script_url_text, "html.parser")
            script = soup.get_text().strip()
            if script == "":
                script = "No script available"
        except requests.RequestException as e:
            print(f"Error fetching .txt file: {e}")
            script = ".txt not found"
        except Exception as e:
            print(f"Unexpected error: {e}")
            script = ".txt not found"
    return script


def main() -> None:
    """Fetch movie information from the specified URLs and writes it to a file."""
    title_list = []
    movie_info_list = get_movie_info("https://www.dailyscript.com/movie.html")
    movie_info_list = get_movie_info("https://www.dailyscript.com/movie_n-z.html")

    for movie_title, movie_id, movie_link in zip(
        movie_info_list[0], movie_info_list[1], movie_info_list[2]
    ):
        script = get_movie_scripts(movie_link)
        if script != "The work has been removed." and script != "ÿþ ":
            title_list.append(movie_title)
    print(title_list)


if __name__ == "__main__":
    main()
