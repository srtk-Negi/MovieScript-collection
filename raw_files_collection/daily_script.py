import re
import requests
from bs4 import BeautifulSoup

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}


date_patterns = [
    r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},\s+\d{4}\b",
    r"\b(january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\b",
    r"\b\d{4}\b",
]


def get_movie_names_and_links_daily_script(URL_DAILY_SCRIPT: str) -> dict:
    """Fetch movie titles and script links, curate unique IDs, and return movie info."""
    daily_script_names_and_links = {}

    url_text = requests.get(URL_DAILY_SCRIPT).text
    soup = BeautifulSoup(url_text, "html.parser")

    previous_names = None
    script_list_info = soup.ul.find_all("p")

    for script_info in script_list_info:
        script_info_text = script_info.text
        by_index = script_info_text.lower().find("by")
        movie_title = script_info_text[:by_index].strip().replace("\xa0", "")

        match = ""
        date = ""

        for date_pattern in date_patterns:
            match = re.search(date_pattern, script_info_text, re.IGNORECASE)
            if match:
                date = match.group()
                break

        if match == "":
            date = None

        if movie_title != previous_names:
            movie_link_tag = script_info.find("a").get("href")
            movie_link = f"https://www.dailyscript.com/{movie_link_tag}"
            daily_script_names_and_links[movie_title] = movie_link

        previous_names = movie_title

    return daily_script_names_and_links


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


def get_raw_files_daily_script(URL_DAILY_SCRIPT: str) -> list[str]:
    """Retreive html structure from script links and write raw html to files."""
    final_dict = {}
    try:
        daily_script_names_and_links_1 = get_movie_names_and_links_daily_script(
            URL_DAILY_SCRIPT
        )
    except:
        with open("error_log.txt", "a", encoding="utf-8") as outfile:
            outfile.write(
                f"The URL {URL_DAILY_SCRIPT} did not work for 'Daily Script'\n"
            )
        return

    url_nz = URL_DAILY_SCRIPT.replace(".html", "_n-z.html")
    try:
        daily_script_names_and_links_2 = get_movie_names_and_links_daily_script(url_nz)
        final_dict = {
            **daily_script_names_and_links_1,
            **daily_script_names_and_links_2,
        }
    except:
        with open("error_log.txt", "a", encoding="utf-8") as outfile:
            outfile.write(
                f"The URL {URL_DAILY_SCRIPT} did not work for 'Daily Script'\n"
            )
        return

    pdf_count = 0
    doc_count = 0
    txt_count = 0
    rawfile_count = 0
    MOVIE_NAMES = []

    for movie_title, script_url in final_dict.items():
        if script_url.lower().endswith(".pdf"):
            try:
                content = requests.get(script_url, headers=headers).content
            except:
                with open("error_log.txt", "a", encoding="utf-8") as outfile:
                    outfile.write(
                        f"Could not get {script_url} for {movie_title} from daily script\n"
                    )
                continue

            MOVIE_NAMES.append(movie_title)
            file_type = ".pdf"
            filename_2 = curate_filename(movie_title, file_type)

            # with open(f"F:\Movie-Data-Collection\Rawfiles\{filename_2}", "wb") as f:
            with open(f"rawfiles/daily_script/{filename_2}", "wb") as f:
                f.write(content)
                pdf_count += 1

        elif script_url.lower().endswith(".doc"):
            try:
                content = requests.get(script_url, headers=headers).content
            except:
                with open("error_log.txt", "a", encoding="utf-8") as outfile:
                    outfile.write(
                        f"Could not get {script_url} for {movie_title} from daily script\n"
                    )
                continue

            MOVIE_NAMES.append(movie_title)
            file_type = ".doc"
            filename_2 = curate_filename(movie_title, file_type)

            # with open(f"F:\Movie-Data-Collection\Rawfiles\{filename_2}", "wb") as f:
            with open(f"rawfiles/daily_script/{filename_2}", "wb") as f:
                f.write(content)
                doc_count += 1

        elif script_url.lower().endswith(".txt"):
            try:
                content = requests.get(script_url, headers=headers).content
                soup = BeautifulSoup(content, "html.parser")
            except:
                with open("error_log.txt", "a", encoding="utf-8") as outfile:
                    outfile.write(
                        f"Could not get {script_url} for {movie_title} from daily script\n"
                    )
                continue

            soup_str = str(soup)
            final_content = f"<html><body>{soup_str}</body></html>"

            MOVIE_NAMES.append(movie_title)
            file_type = ".html"
            filename_2 = curate_filename(movie_title, file_type)

            with open(
                # f"F:\Movie-Data-Collection\Rawfiles\{filename_2}", "w", encoding="utf-8"
                f"rawfiles/daily_script/{filename_2}",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(final_content)
                txt_count += 1

        else:
            try:
                content = requests.get(script_url, headers=headers)
                soup = BeautifulSoup(content.text, "html.parser")
            except:
                with open("error_log.txt", "a", encoding="utf-8") as outfile:
                    outfile.write(
                        f"Could not get {script_url} for {movie_title} from daily script\n"
                    )
                continue

            MOVIE_NAMES.append(movie_title)
            file_type = ".html"
            filename_2 = curate_filename(movie_title, file_type)

            with open(
                # f"F:\Movie-Data-Collection\Rawfiles\{filename_2}", "w", encoding="utf-8"
                f"rawfiles/daily_script/{filename_2}",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(str(soup))
                rawfile_count += 1

    print(f"Total number of PDFs collected from 'Daily Script': {pdf_count}")
    print(f"Total number of DOCs collected from 'Daily Script': {doc_count}")
    print(f"Total number of TXTs collected from 'Daily Script': {txt_count}")
    print(f"Total number of raw files collected from 'Daily Script': {rawfile_count}")

    return MOVIE_NAMES
