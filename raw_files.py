from raw_files_collection.screenplays_for_you import get_raw_screenplays_for_you
from raw_files_collection.screenplays_online import get_raw_screenplays_online
from raw_files_collection.script_slug import get_raw_script_slug
from raw_files_collection.awesome_film import get_raw_files_awesome_film
from raw_files_collection.daily_script import get_raw_files_daily_script
from raw_files_collection.imsdb import get_raw_files_imsdb
from raw_files_collection.script_pdf import get_raw_script_pdf
from raw_files_collection.script_savant import get_raw_script_savant

URL_SCREENPLAYS_FOR_YOU = "https://sfy.ru/scripts/"
URL_SCREENPLAYS_ONLINE = "https://www.screenplays-online.de/"
URL_SCRIPT_SLUG = "https://www.scriptslug.com/request/?pg="
URL_SCRIPT_PDF = "https://scriptpdf.com/full-list/"

URL_AWESOME_FILM = "http://www.awesomefilm.com/"
URL_DAILYSCRIPT = "https://www.dailyscript.com/movie.html"
URL_IMSDB = "https://imsdb.com/all-scripts.html"
URL_SCRIPT_SAVANT = "https://thescriptsavant.com/movies.html"


def main():
    movie_names = []
    # SCREENPLAYS FOR YOU
    print("SCREENPLAYS FOR YOU - STARTED")
    movie_names.extend(get_raw_screenplays_for_you(URL_SCREENPLAYS_FOR_YOU))
    print("SCREENPLAYS FOR YOU - FINISHED\n")

    # SCREENPLAYS ONLINE
    print("SCREENPLAYS ONLINE - STARTED")
    movie_names.extend(get_raw_screenplays_online(URL_SCREENPLAYS_ONLINE))
    print("SCREENPLAYS ONLINE - FINISHED\n")

    # SCRIPT PDF
    print("SCRIPT PDF - STARTED")
    movie_names.extend(get_raw_script_pdf(URL_SCRIPT_PDF))
    print("SCRIPT PDF - FINISHED\n")

    # AWESOME FILM
    print("AWESOME FILM - STARTED")
    movie_names.extend(get_raw_files_awesome_film(URL_AWESOME_FILM))
    print("AWESOME FILM - FINISHED\n")

    # DAILY SCRIPT
    print("DAILY SCRIPT - STARTED")
    movie_names.extend(get_raw_files_daily_script(URL_DAILYSCRIPT))
    print("DAILY SCRIPT - FINISHED\n")

    # SCRIPT SAVANT
    print("SCRIPT SAVANT - STARTED")
    movie_names.extend(get_raw_script_savant(URL_SCRIPT_SAVANT))
    print("SCRIPT SAVANT - FINISHED\n")

    # IMSDB
    print("IMSDB - STARTED")
    movie_names.extend(get_raw_files_imsdb(URL_IMSDB))
    print("IMSDB - FINISHED\n")

    # SCRIPT SLUG (WORKING BUT NOT THE BEST SOLUTION)
    # get_raw_script_slug(URL_SCRIPT_SLUG)

    with open("movie_names.txt", "a", encoding="utf-8") as outfile:
        outfile.write("\n".join(movie_names))


if __name__ == "__main__":
    main()
