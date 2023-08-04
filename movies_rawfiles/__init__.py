"""This module contains the functions to collect the raw files from the
different websites.
"""

from .awesome_film import get_movies_awesome_film
from .daily_script import get_movies_daily_script
from .imsdb import get_movies_imsdb
from .screenplays_for_you import get_movies_screenplays_for_you
from .screenplays_online import get_movies_screenplays_online
from .script_pdf import get_movies_script_pdf
from .script_savant import get_movies_script_savant
from .helper_functions import get_file_type, curate_filename, switch_article
from .movie import Movie
