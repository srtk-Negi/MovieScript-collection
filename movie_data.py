from data_collector.awesome_film_data import get_awesome_film_scripts
from data_collector.daily_script_data import get_daily_script_scripts
from data_collector.imsdb_data import get_imsdb_scripts
from data_collector.screenplays_for_you_data import get_screenplays_for_you_scripts
from data_collector.screenplays_online_data import get_screenplays_online_scripts


def main():
    # get_awesome_film_scripts()
    # get_daily_script_scripts()
    # get_imsdb_scripts()
    # get_screenplays_for_you_scripts()
    get_screenplays_online_scripts()


if __name__ == "__main__":
    main()
