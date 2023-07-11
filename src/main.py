from screenplays_for_you import get_movie_names_screenplays_for_you
from screenplays_online import get_movie_names_screenplays_online
from script_slug import get_movie_names_script_slug

URL_SCREENPLAYS_FOR_YOU = "https://sfy.ru/scripts"
URL_SCREENPLAYS_ONLINE = "https://www.screenplays-online.de/"
URL_SCRIPT_SLUG = "https://www.scriptslug.com/request/?pg="


def main():
    movie_names_screenplays_for_you = get_movie_names_screenplays_for_you(
        URL_SCREENPLAYS_FOR_YOU
    )
    movie_names_screenplays_online = get_movie_names_screenplays_online(
        URL_SCREENPLAYS_ONLINE
    )
    movie_names_script_slug = get_movie_names_script_slug(URL_SCRIPT_SLUG)
    print(
        "----------**********----------**********--------------------**********----------**********----------"
    )
    print(f"SCREENPLAYS FOR YOU\n{movie_names_screenplays_for_you}")
    print(
        "----------**********----------**********--------------------**********----------**********----------"
    )
    print(f"SCREENPLAYS ONLINE\n{movie_names_screenplays_online}")
    print(
        "----------**********----------**********--------------------**********----------**********----------"
    )
    print(f"SCRIPT SLUG\n{movie_names_script_slug}")


if __name__ == "__main__":
    main()
