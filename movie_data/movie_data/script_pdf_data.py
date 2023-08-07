import os
from PyPDF2 import PdfReader


def get_script_pdf_scripts():
    rawfiles = os.listdir("rawfiles/script_pdf")

    for rawfile in rawfiles:
        try:
            reader = PdfReader(f"rawfiles/script_pdf/{rawfile}")
            pages = reader.pages

            for page in pages:
                text = page.extract_text()
                with open(
                    f"data_files/script_pdf/{rawfile[:-4]}.txt", "a", encoding="utf-8"
                ) as f:
                    f.write(text)

        except Exception as e:
            with open("test.txt", "a", encoding="utf-8") as f:
                f.write(f"Could not read {rawfile}\n{e}\n")
            continue
