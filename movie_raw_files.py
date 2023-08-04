from bs4 import BeautifulSoup
import requests

from movies_rawfiles import (
    get_movies_awesome_film,
    get_movies_daily_script,
    get_movies_imsdb,
    get_movies_screenplays_for_you,
    get_movies_screenplays_online,
    get_movies_script_pdf,
    get_movies_script_savant,
    curate_filename,
)


# from raw_files_collector.script_slug import get_raw_script_slug


URL_AWESOME_FILM = "http://www.awesomefilm.com/"
URL_DAILYSCRIPT = "https://www.dailyscript.com/movie.html"
URL_IMSDB = "https://imsdb.com/all-scripts.html"
URL_SCREENPLAYS_FOR_YOU = "https://sfy.ru/scripts/"
URL_SCREENPLAYS_ONLINE = "https://www.screenplays-online.de/"
URL_SCRIPT_PDF = "https://scriptpdf.com/full-list/"
URL_SCRIPT_SAVANT = "https://thescriptsavant.com/movies.html"
# URL_SCRIPT_SLUG = "https://www.scriptslug.com/request/?pg="

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64"}
FILEPATH = "rawfiles/"


def main():
    init_movie_list = []
    movie_map = {}
    # AWESOME FILM
    print("AWESOME FILM - STARTED")
    init_movie_list.extend(get_movies_awesome_film(URL_AWESOME_FILM))
    print("AWESOME FILM - FINISHED\n")

    # DAILY SCRIPT
    print("DAILY SCRIPT - STARTED")
    init_movie_list.extend(get_movies_daily_script(URL_DAILYSCRIPT))
    print("DAILY SCRIPT - FINISHED\n")

    # # IMSDB
    print("IMSDB - STARTED")
    init_movie_list.extend(get_movies_imsdb(URL_IMSDB))
    print("IMSDB - FINISHED\n")

    # # SCREENPLAYS FOR YOU
    print("SCREENPLAYS FOR YOU - STARTED")
    init_movie_list.extend(get_movies_screenplays_for_you(URL_SCREENPLAYS_FOR_YOU))
    print("SCREENPLAYS FOR YOU - FINISHED\n")

    # # SCREENPLAYS ONLINE
    print("SCREENPLAYS ONLINE - STARTED")
    init_movie_list.extend(get_movies_screenplays_online(URL_SCREENPLAYS_ONLINE))
    print("SCREENPLAYS ONLINE - FINISHED\n")

    # # SCRIPT PDF
    print("SCRIPT PDF - STARTED")
    init_movie_list.extend(get_movies_script_pdf(URL_SCRIPT_PDF))
    print("SCRIPT PDF - FINISHED\n")

    # # SCRIPT SAVANT
    print("SCRIPT SAVANT - STARTED")
    init_movie_list.extend(get_movies_script_savant(URL_SCRIPT_SAVANT))
    print("SCRIPT SAVANT - FINISHED\n")

    for movie in init_movie_list:
        if movie.title not in movie_map:
            movie_map[movie.title] = movie
        else:
            movie_map[movie.title].merge(movie)

    pdf_count = 0
    html_count = 0
    doc_count = 0
    for movie in movie_map.values():
        if movie.file_type == "pdf":
            pdf_count += 1
        elif movie.file_type in ["html", "htm", "txt"]:
            html_count += 1
        elif movie.file_type in ["doc", "docx"]:
            doc_count += 1
    print(f"pdf: {pdf_count}")
    print(f"html, txt, htm: {html_count}")
    print(f"doc: {doc_count}")
    print(f"Total unique movies objects: {len(movie_map)}")

    print("\nMovie object collection done.\nRawfile collection started\n")

    rawfiles_count = 0
    for movie in movie_map.values():
        try:
            if movie.file_type == "pdf" or movie.file_type == "doc":
                content = requests.get(movie.script_url).content
                filename = curate_filename(movie.title, movie.file_type)
                with open(f"{FILEPATH}{filename}", "wb") as f:
                    f.write(content)
                    rawfiles_count += 1
            elif movie.file_type in ["html", "htm"]:
                content = requests.get(movie.script_url, headers=headers)
                soup = BeautifulSoup(content.text, "html.parser")
                filename = curate_filename(movie.title, movie.file_type)
                with open(f"{FILEPATH}{filename}", "w", encoding="utf-8") as f:
                    f.write(str(soup))
                    rawfiles_count += 1
            elif movie.file_type == "txt":
                content = requests.get(movie.script_url)
                soup = BeautifulSoup(content.text, "html.parser")
                soup_str = str(soup)
                final_soup = f"<html><pre>{soup_str}</pre></html>"
                filename = curate_filename(movie.title, "html")
                with open(f"{FILEPATH}{filename}", "w", encoding="utf-8") as f:
                    f.write(final_soup)
                    rawfiles_count += 1
        except Exception as e:
            with open("error_log.txt", "a") as f:
                f.write(f"{movie.title} - {movie.script_url}\n{e}\n\n")

    print(f"Rawfile collection done.\nCollected {rawfiles_count} rawfiles.")

    # SCRIPT SLUG (WORKING BUT NOT THE BEST SOLUTION)
    # get_raw_script_slug(URL_SCRIPT_SLUG)


if __name__ == "__main__":
    main()
