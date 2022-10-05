import os
import yaml


def readPath(filePath, mode="r"):
    if os.path.isfile(filePath):
        with open(filePath, mode) as fh:
            text = fh.read()
        return text
    return ""


def readFile(fileDir, fileName, mode="r"):
    filePath = f"{fileDir}/{fileName}"
    if not os.path.isfile(filePath):
        return f"No file {fileName} in {fileDir}"
    return open(filePath, mode)


def readYaml(path):
    if not os.path.isfile(path):
        return None
    with open(path) as fh:
        data = yaml.load(fh, Loader=yaml.FullLoader)
    return data


def dirExists(path):
    return os.path.isdir(path)


def listFiles(path, ext):
    if not os.path.isdir(path):
        return []

    files = []

    nExt = len(ext)
    with os.scandir(path) as dh:
        for entry in dh:
            name = entry.name
            if name.endswith(ext) and entry.is_file():
                files.append(name[0:-nExt])

    return files
