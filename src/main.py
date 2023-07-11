from screenplays_for_you import get_movie_names_screenplays_for_you
from screenplays_online import get_movie_names_screenplays_online
from script_slug import get_movie_names_script_slug
from awesome_film import get_movie_names_awesome_film
from imsdb import get_movie_names_imsdb
from daily_script import get_movie_names_daily_script

URL_SCREENPLAYS_FOR_YOU = "https://sfy.ru/scripts"
URL_SCREENPLAYS_ONLINE = "https://www.screenplays-online.de/"
URL_SCRIPT_SLUG = "https://www.scriptslug.com/request/?pg="
URL_AWESOME_FILM = "http://www.awesomefilm.com/"
URL_IMSDB = "https://imsdb.com/all-scripts.html"
URL_DAILYSCRIPT_AM = "https://www.dailyscript.com/movie.html"
URL_DAILYSCRIPT_NZ = "https://www.dailyscript.com/movie_n-z.html"


def main():
    movie_names_screenplays_for_you = get_movie_names_screenplays_for_you(
        URL_SCREENPLAYS_FOR_YOU
    )
    movie_names_screenplays_online = get_movie_names_screenplays_online(
        URL_SCREENPLAYS_ONLINE
    )
    movie_names_script_slug = get_movie_names_script_slug(URL_SCRIPT_SLUG)
    movie_names_awesome_film = get_movie_names_awesome_film(URL_AWESOME_FILM)
    movie_names_imsdb = get_movie_names_imsdb(URL_IMSDB)
    movie_names_daily_script_am = get_movie_names_daily_script(URL_DAILYSCRIPT_AM)
    movie_names_daily_script_mz = get_movie_names_daily_script(URL_DAILYSCRIPT_NZ)
    movie_names_daily_script = movie_names_daily_script_am + movie_names_daily_script_mz

    print(f"\nSCREENPLAYS FOR YOU\n{movie_names_screenplays_for_you}")
    print(f"\nSCREENPLAYS ONLINE\n{movie_names_screenplays_online}")
    print(f"\nSCRIPT SLUG\n{movie_names_script_slug}")
    print(f"\nAWESOME FILM\n{movie_names_awesome_film}")
    print(f"\nIMSDB\n{movie_names_imsdb}")
    print(f"\nDAILY SCRIPT\n{movie_names_daily_script}")


if __name__ == "__main__":
    main()
