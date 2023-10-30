import os


def get_hoggerfiles(dir_or_file: str) -> list[str]:
    hoggerfiles = []
    if os.path.isfile(dir_or_file):
        hoggerfiles.append(os.path.abspath(dir_or_file))
    elif os.path.isdir(dir_or_file):
        for root, dirs, files in os.walk(".", topdown=False):
            for name in files:
                if name.endswith(".hogger"):
                    hoggerfiles.append(os.path.abspath(os.path.join(root, name)))
    else:
        raise Exception("Path provided is neither a dir, nor a file.")
    return hoggerfiles