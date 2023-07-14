from raw_files_collection.screenplays_for_you import get_raw_screenplays_for_you
from raw_files_collection.screenplays_online import get_raw_screenplays_online
from raw_files_collection.script_slug import get_raw_script_slug

URL_SCREENPLAYS_FOR_YOU = "https://sfy.ru/scripts"
URL_SCREENPLAYS_ONLINE = "https://www.screenplays-online.de/"
URL_SCRIPT_SLUG = "https://www.scriptslug.com/request/?pg="
URL_AWESOME_FILM = "http://www.awesomefilm.com/"
URL_IMSDB = "https://imsdb.com/all-scripts.html"
URL_DAILYSCRIPT_AM = "https://www.dailyscript.com/movie.html"
URL_DAILYSCRIPT_NZ = "https://www.dailyscript.com/movie_n-z.html"


def main():
    # SCREENPLAYS FOR YOU
    get_raw_screenplays_for_you(URL_SCREENPLAYS_FOR_YOU)

    # SCREENPLAYS ONLINE
    # get_raw_screenplays_online(URL_SCREENPLAYS_ONLINE)

    # SCRIPT SLUG
    # get_raw_script_slug(URL_SCRIPT_SLUG)


if __name__ == "__main__":
    main()
