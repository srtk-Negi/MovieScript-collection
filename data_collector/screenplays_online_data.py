from bs4 import BeautifulSoup
import os


def get_screenplays_online_scripts():
    rawfiles = os.listdir("rawfiles/screenplays_online")

    worked = 0
    for rawfile in rawfiles:
        if rawfile.endswith(".html"):
            with open(
                f"rawfiles/screenplays_online/{rawfile}", "r", encoding="utf-8"
            ) as f:
                content = f.read()
                soup = BeautifulSoup(content, "html.parser")

                try:
                    script = soup.find("pre").string
                    with open(
                        f"data_files/screenplays_online/{rawfile[:-5]}" + ".txt",
                        "w",
                        encoding="utf-8",
                    ) as f:
                        f.write(str(script))
                        worked += 1
                except:
                    with open("test.txt", "a", encoding="utf-8") as f:
                        f.write(f"{rawfile}\n")

    print(worked)
