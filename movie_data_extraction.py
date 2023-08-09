from movie_data import extract_script_pdf, extract_script_html
import os


def main():
    rawfiles = os.listdir("rawfiles")

    html_count = 0
    pdf_count = 0
    script = ""
    for rawfile in rawfiles:
        if (
            rawfile.endswith("html")
            or rawfile.endswith("htm")
            or rawfile.endswith("txt")
        ):
            script, filepath = extract_script_html(f"rawfiles/{rawfile}")
            html_count += 1
        elif rawfile.endswith("pdf"):
            script, filepath = extract_script_pdf(f"rawfiles/{rawfile}")
            pdf_count += 1
        elif rawfile.endswith("doc") or rawfile.endswith("docx"):
            continue
        else:
            print(f"{rawfile} not processed")
            continue

        if script == "":
            continue

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(script)

    print(f"{html_count} scripts extracted")
    print(f"{pdf_count} scripts extracted")


if __name__ == "__main__":
    main()
