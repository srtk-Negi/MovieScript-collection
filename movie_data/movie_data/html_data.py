from bs4 import BeautifulSoup
import re

re_tags = re.compile(r"<[^>]+>")


def extract_script(filepath: str, filename: str) -> None:
    """Extracts the script from the html file"""
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    script = soup.find("pre")
    if script:
        with open(f"datafiles/{filename}", "w", encoding="utf-8") as f:
            f.write(script.text)
            return

    script = soup.find("body")
    if script:
        with open(f"datafiles_1/{filename}", "w", encoding="utf-8") as f:
            final_text = re_tags.sub("", script.text)
            f.write(final_text)
            return

    with open("record.txt", "a", encoding="utf-8") as f:
        f.write(f"{filename}\n")
