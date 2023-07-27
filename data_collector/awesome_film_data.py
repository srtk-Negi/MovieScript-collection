from bs4 import BeautifulSoup
import os


def get_awesome_film_script():
    rawfiles = os.listdir("rawfiles/awesome_film")
    for rawfile in rawfiles:
        if rawfile.endswith(".html"):
            with open("rawfiles/awesome_film/" + rawfile, "r", encoding="utf-8") as f:
                content = f.read()
                soup = BeautifulSoup(content, "html.parser")

            try:
                script = soup.find("pre").text
                with open(
                    "data_files/awesome_film/" + rawfile[:-5] + ".txt",
                    "w",
                    encoding="utf-8",
                ) as f:
                    f.write(script)
            except Exception as e:
                print(f"{rawfile}  {e}")
