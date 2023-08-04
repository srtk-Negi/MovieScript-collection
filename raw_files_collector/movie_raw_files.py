from awesome_film import get_movies_awesome_film
from daily_script import get_movies_daily_script
from imsdb import get_movies_imsdb
from screenplays_for_you import get_movies_screenplays_for_you
from screenplays_online import get_movies_screenplays_online
from script_pdf import get_movies_script_pdf
from script_savant import get_movies_script_savant

# from raw_files_collector.script_slug import get_raw_script_slug


URL_AWESOME_FILM = "http://www.awesomefilm.com/"
URL_DAILYSCRIPT = "https://www.dailyscript.com/movie.html"
URL_IMSDB = "https://imsdb.com/all-scripts.html"
URL_SCREENPLAYS_FOR_YOU = "https://sfy.ru/scripts/"
URL_SCREENPLAYS_ONLINE = "https://www.screenplays-online.de/"
URL_SCRIPT_PDF = "https://scriptpdf.com/full-list/"
URL_SCRIPT_SAVANT = "https://thescriptsavant.com/movies.html"
# URL_SCRIPT_SLUG = "https://www.scriptslug.com/request/?pg="


def main():
    init_movie_list = []
    movie_map = {}
    # AWESOME FILM
    print("AWESOME FILM - STARTED")
    init_movie_list.extend(get_movies_awesome_film(URL_AWESOME_FILM))
    print("AWESOME FILM - FINISHED\n")

    # DAILY SCRIPT
    # print("DAILY SCRIPT - STARTED")
    # init_movie_list.extend(get_movies_daily_script(URL_DAILYSCRIPT))
    # print("DAILY SCRIPT - FINISHED\n")

    # # IMSDB
    # print("IMSDB - STARTED")
    # movie_list.extend(get_movies_imsdb(URL_IMSDB))
    # print("IMSDB - FINISHED\n")

    # # SCREENPLAYS FOR YOU
    # print("SCREENPLAYS FOR YOU - STARTED")
    # movie_list.extend(get_movies_screenplays_for_you(URL_SCREENPLAYS_FOR_YOU))
    # print("SCREENPLAYS FOR YOU - FINISHED\n")

    # # SCREENPLAYS ONLINE
    # print("SCREENPLAYS ONLINE - STARTED")
    # movie_list.extend(get_movies_screenplays_online(URL_SCREENPLAYS_ONLINE))
    # print("SCREENPLAYS ONLINE - FINISHED\n")

    # # SCRIPT PDF
    # print("SCRIPT PDF - STARTED")
    # movie_list.extend(get_movies_script_pdf(URL_SCRIPT_PDF))
    # print("SCRIPT PDF - FINISHED\n")

    # # SCRIPT SAVANT
    # print("SCRIPT SAVANT - STARTED")
    # movie_list.extend(get_movies_script_savant(URL_SCRIPT_SAVANT))
    # print("SCRIPT SAVANT - FINISHED\n")

    # for movie in init_movie_list:
    #     if movie.title not in movie_map:
    #         movie_map[movie.title] = movie
    #     else:
    #         movie_map[movie.title].merge(movie)

    with open("test.txt", "w", encoding="utf-8") as outfile:
        for movie in init_movie_list:
            outfile.write(
                f"{movie.title}\n{movie.script_url}\n{movie.movie_year}\n{movie.script_date}\n{movie.writers}\n{movie.file_type}\n{movie.num_elements()}\n\n"
            )

    # SCRIPT SLUG (WORKING BUT NOT THE BEST SOLUTION)
    # get_raw_script_slug(URL_SCRIPT_SLUG)


if __name__ == "__main__":
    main()
