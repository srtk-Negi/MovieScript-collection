class Movie:
    def __init__(
        self,
        title: str,
        script_url: str,
        year: str = None,
        month: str = None,
        date: str = None,
        writers: str = None,
    ):
        self.title = title
        self.script_url = script_url
        self.year = year
        self.month = month
        self.date = date
        self.writers = writers

    def __str__(self):
        return f"{self.title}\n{self.script_url}\n{self.year}\n{self.month}\n{self.date}\n{self.writers}\n\n"
