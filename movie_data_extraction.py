import pandas as pd
from movie_data.movie_data import extract_script
import os


def main():
    rawfiles = os.listdir("rawfiles")
    for file in rawfiles:
        if file.endswith(".html") or file.endswith(".htm") or file.endswith(".txt"):
            extract_script(f"rawfiles/{file}", f"{file[:-5]}.txt")
        elif file.endswith(".pdf") or file.endswith(".doc"):
            pass


if __name__ == "__main__":
    main()
