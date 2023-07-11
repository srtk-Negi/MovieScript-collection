from screenplays_for_you import get_movie_names_screenplays_for_you
from screenplays_online import get_movie_names_screenplays_online
from script_slug import get_movie_names_script_slug

URL_SCREENPLAYS_FOR_YOU = "https://sfy.ru/scripts"


def main():
    movie_names = get_movie_names_screenplays_for_you(URL_SCREENPLAYS_FOR_YOU)
    print(movie_names)


if __name__ == "__main__":
    main()
