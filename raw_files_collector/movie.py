class Movie:
    def __init__(
        self,
        title: str,
        script_url: str,
        movie_year: str = None,
        script_date: str = None,
        writers: str = None,
    ):
        self.title = title
        self.script_url = script_url
        self.movie_year = movie_year
        self.script_date = script_date
        self.writers = writers

    def __str__(self):
        return f"{self.title}\n{self.script_url}\n{self.movie_year}\n{self.script_date}\n{self.writers}\n"
