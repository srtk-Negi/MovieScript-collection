from bs4 import BeautifulSoup
import PyPDF2
import re

data_filepath = "scripts"
re_tags = re.compile(r"<[^>]+>")


def extract_script_html(filepath: str) -> list[str]:
    """Extracts the script from the html file"""
    filename = filepath.split("/")[-1]

    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    script = soup.find("pre")
    if script:
        with open(f"{data_filepath}\{filename[:-5]}.txt", "w", encoding="utf-8") as f:
            f.write(script.text)
            return script.text, f"{data_filepath}\{filename[:-5]}.txt"

    script = soup.find("body")
    if script:
        with open(f"{data_filepath}\{filename[:-5]}.txt", "w", encoding="utf-8") as f:
            final_text = re_tags.sub("", script.text)
            f.write(final_text)
            return final_text, f"{data_filepath}\{filename[:-5]}.txt"
    return "", ""


def extract_script_pdf(filepath: str) -> list[str]:
    """Extracts the script from the pdf file"""
    filename = filepath.split("/")[-1]

    try:
        with open(filepath, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text += page.extract_text()

            if text == "":
                with open("error_log.txt", "a", encoding="utf-8") as f:
                    f.write(f"{filename} - NO SCRIPT FOUND.\n")
                return text, ""
    except Exception as e:
        with open("error_log.txt", "a", encoding="utf-8") as f:
            f.write(f"Did not work for {filename}\n{e}\n\n")
        return "", ""

    with open(f"{data_filepath}\{filename[:-4]}.txt", "w", encoding="utf-8") as f:
        f.write(text)

    return text, f"{data_filepath}\{filename[:-4]}.txt"
