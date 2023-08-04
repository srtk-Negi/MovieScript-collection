def last_index_of(string: str, char: str) -> int:
    """Gets the last index of a character in a string

    Args:
        char (str): The character to find
        string (str): The string to find the character in

    Returns:
        int: The last index of the character in the string
    """
    for i in range(len(string) - 1, -1, -1):
        if string[i] == char:
            return i


def get_file_type(filename: str) -> str:
    """Gets the file type of the filename. Only work for pdf, txt, doc, html, htm files

    Args:
        filename (str): The filename

    Returns:
        str: The file type
    """
    filetype = filename[last_index_of(filename, ".") + 1 :].lower()
    if not (
        filetype == "pdf"
        or filetype == "txt"
        or filetype == "doc"
        or filetype == "html"
        or filetype == "htm"
    ):
        filetype = "html"

    return filetype


def curate_filename(movie_title: str, file_type: str) -> str:
    """Gets the filename for the rawfile

    Args:
        movie_name (str): The movie name
        file_type (str): The file type

    Returns:
        str: The filename for the rawfile"""

    filename = ""
    for ch in movie_title.lower():
        if ch.isalnum() or ch == " ":
            filename += ch
    filename_2 = f'{"_".join(filename.strip().split())}.{file_type}'
    return filename_2


def switch_article(article: str, movie_name: str) -> str:
    """Switches the position of the article of the movie name (The, An, A) from the end to the beginning (used as a helper function in get_movie_titles_and_years())

    Args:
        article (str): The article of the movie name
        movie_name (str): The movie name

    Returns:
        str: The movie name with the article at the beginning
    """
    new_name = movie_name.replace(f", {article}", "")
    movie_name = f"{article} " + new_name

    return movie_name


def get_name_to_compare(movie_name: str) -> str:
    """Gets the name to compare for the movie

    Args:
        movie_name (str): The movie name

    Returns:
        str: The name to compare for the movie
    """
    name = movie_name.lower()
    name_to_compare = ""
    for ch in name:
        if ch.isalnum():
            name_to_compare += ch

    return name_to_compare


def main():
    last_index_of()


if __name__ == "__main__":
    main()
