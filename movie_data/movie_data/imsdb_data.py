from bs4 import BeautifulSoup
import os
import re

RE_HTML_TAG = re.compile(r"<[^>]*>")


def get_imsdb_scripts():
    rawfiles = os.listdir("rawfiles/imsdb")

    for rawfile in rawfiles:
        with open(f"rawfiles/imsdb/{rawfile}", "r", encoding="utf-8") as f:
            content = f.read()
            soup = BeautifulSoup(content, "html.parser")

            script = soup.find("pre")
            script = RE_HTML_TAG.sub("", str(script))

        with open(
            f"data_files/imsdb/{rawfile[:-5]}" + ".txt", "w", encoding="utf-8"
        ) as f:
            f.write(str(script))
