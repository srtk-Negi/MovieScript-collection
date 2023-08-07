from bs4 import BeautifulSoup
import re

re_tags = re.compile(r"<[^>]+>")


def extract_script(filepath: str, filename: str) -> int:
    """Extracts the script from the html file"""
    with open(filepath, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")
    try:
        script = soup.find("pre")
        if script:
            with open(f"datafiles/{filename}", "w", encoding="utf-8") as f:
                f.write(script.text)
                return 1
        else:
            raise ValueError("No script found")
    except Exception as e:
        return 0
