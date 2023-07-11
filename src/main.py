from screenplays_for_you import get_movie_names_screenplays_for_you
from screenplays_online import get_movie_names_screenplays_online
from script_slug import get_movie_names_script_slug
from awesome_film import get_movie_names_awesome_film

URL_SCREENPLAYS_FOR_YOU = "https://sfy.ru/scripts"
URL_AWESOME_FILM = "http://www.awesomefilm.com/"


def main():
    movie_names = get_movie_names_screenplays_for_you(URL_SCREENPLAYS_FOR_YOU)
    print(movie_names)
    awesome_film_names = get_movie_names_awesome_film(URL_AWESOME_FILM)
    print(awesome_film_names)


if __name__ == "__main__":
    main()
