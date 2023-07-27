from bs4 import BeautifulSoup
import os


def get_awesome_film_script():
    rawfiles = os.listdir("rawfiles/awesome_film")

    for rawfile in rawfiles:
        if rawfile.endswith(".html"):
            with open("rawfiles/awesome_film/" + rawfile, "r") as f:
                content = f.read()
                soup = BeautifulSoup(content, "html.parser")

            script = soup.find("pre").string
            with open("data_files/awesome_film/" + rawfile[:-5] + ".txt", "w") as f:
                f.write(script)
