import os


def get_script_savant_scripts():
    rawfiles = os.listdir("rawfiles/script_savant")
    print(len(rawfiles))
