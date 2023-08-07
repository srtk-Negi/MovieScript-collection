from bs4 import BeautifulSoup
import os
import re

RE_HTML_TAG = re.compile(r"<[^>]*>")


def get_awesome_film_scripts():
    rawfiles = os.listdir("rawfiles/awesome_film")
    pdf_doc_counter = 0
    html_counter = 0

    for rawfile in rawfiles:
        if rawfile.endswith(".html"):
            html_counter += 1
            with open("rawfiles/awesome_film/" + rawfile, "r", encoding="utf-8") as f:
                content = f.read()
                soup = BeautifulSoup(content, "html.parser")

            try:
                script = soup.find("pre").text
            except:
                script = RE_HTML_TAG.sub("", str(soup))

            with open(
                "data_files/awesome_film/" + rawfile[:-5] + ".txt",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(script)

        elif rawfile.endswith("pdf") or rawfile.endswith("doc"):
            pdf_doc_counter += 1

    print("HTML files: " + str(html_counter))
    print("PDF or DOC files: " + str(pdf_doc_counter))
