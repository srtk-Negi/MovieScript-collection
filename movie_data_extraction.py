import pandas as pd
from movie_data.movie_data import extract_script
import os


def main():
    rawfiles = os.listdir("rawfiles")
    print(len(rawfiles))
    worked = 0
    not_worked = 0
    pdf = 0
    for file in rawfiles:
        if file.endswith(".html") or file.endswith(".htm") or file.endswith(".txt"):
            flag = extract_script(f"rawfiles/{file}", f"{file[:-5]}.txt")
            if flag:
                worked += 1
            else:
                not_worked += 1
        elif file.endswith(".pdf") or file.endswith(".doc"):
            pdf += 1
    print(f"Worked: {worked}\nNot Worked: {not_worked}\nPDF: {pdf}")


if __name__ == "__main__":
    main()
