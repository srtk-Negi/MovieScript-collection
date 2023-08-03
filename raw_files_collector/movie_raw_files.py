from awesome_film import get_names_and_links_awesome_film
from daily_script import get_raw_files_daily_script
from imsdb import get_raw_files_imsdb
from screenplays_for_you import get_raw_screenplays_for_you
from screenplays_online import get_raw_screenplays_online
from script_pdf import get_raw_script_pdf
from script_savant import get_raw_script_savant

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
    movie_title_list = []
    # AWESOME FILM
    # print("AWESOME FILM - STARTED")
    awesome_list = get_names_and_links_awesome_film(URL_AWESOME_FILM)
    for ob in awesome_list:
        print(ob)
    # print("AWESOME FILM - FINISHED\n")

    # DAILY SCRIPT
    # print("DAILY SCRIPT - STARTED")
    # get_raw_files_daily_script(URL_DAILYSCRIPT)
    # print("DAILY SCRIPT - FINISHED\n")

    # # IMSDB
    # print("IMSDB - STARTED")
    # get_raw_files_imsdb(URL_IMSDB)
    # print("IMSDB - FINISHED\n")

    # # SCREENPLAYS FOR YOU
    # print("SCREENPLAYS FOR YOU - STARTED")
    # get_raw_screenplays_for_you(URL_SCREENPLAYS_FOR_YOU)
    # print("SCREENPLAYS FOR YOU - FINISHED\n")

    # # SCREENPLAYS ONLINE
    # print("SCREENPLAYS ONLINE - STARTED")
    # get_raw_screenplays_online(URL_SCREENPLAYS_ONLINE)
    # print("SCREENPLAYS ONLINE - FINISHED\n")

    # # SCRIPT PDF
    # print("SCRIPT PDF - STARTED")
    # get_raw_script_pdf(URL_SCRIPT_PDF)
    # print("SCRIPT PDF - FINISHED\n")

    # # SCRIPT SAVANT
    # print("SCRIPT SAVANT - STARTED")
    # get_raw_script_savant(URL_SCRIPT_SAVANT)
    # print("SCRIPT SAVANT - FINISHED\n")

    # SCRIPT SLUG (WORKING BUT NOT THE BEST SOLUTION)
    # get_raw_script_slug(URL_SCRIPT_SLUG)


if __name__ == "__main__":
    main()
