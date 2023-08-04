class Movie:
    def __init__(
        self,
        title: str,
        script_url: str,
        file_type: str,
        movie_year: str = None,
        script_date: str = None,
        writers: str = None,
    ):
        self.title = title
        self.script_url = script_url
        self.file_type = file_type
        self.movie_year = movie_year
        self.script_date = script_date
        self.writers = writers

    def __str__(self):
        return f"{self.title}\n{self.script_url}\n{self.movie_year}\n{self.script_date}\n{self.writers}\n"

    def merge(self, movie):
        if self.script_url is None:
            self.script_url = movie.script_url
        if self.movie_year is None:
            self.movie_year = movie.movie_year
        if self.script_date is None:
            self.script_date = movie.script_date
        if self.writers is None:
            self.writers = movie.writers
