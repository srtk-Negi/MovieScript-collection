from bs4 import BeautifulSoup
import os
import re

RE_HTML_TAG = re.compile(r"<[^>]*>")


def get_daily_script_scripts():
    rawfiles = os.listdir("rawfiles/daily_script")

    html_count = 0
    pdf_doc_count = 0
    for rawfile in rawfiles:
        if rawfile.endswith(".html"):
            html_count += 1
            with open("rawfiles/daily_script/" + rawfile, "r", encoding="utf-8") as f:
                content = f.read()
                soup = BeautifulSoup(content, "html.parser")

            try:
                script = soup.find("pre").text
            except:
                script = soup.find("body")
                script = RE_HTML_TAG.sub("", str(script))

            with open(
                "data_files/daily_script/" + rawfile[:-5] + ".txt",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(script)

        elif rawfile.endswith(".pdf") or rawfile.endswith(".doc"):
            pdf_doc_count += 1

    print("HTML files: " + str(html_count))
    print("PDF or DOC files: " + str(pdf_doc_count))
