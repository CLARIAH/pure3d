import os
import json

BASE = os.path.expanduser("~/github/clariah/pure3d/pilots/testing-users")
DATA_DIR = f"{BASE}/data"
PROJECT_DIR = f"{DATA_DIR}/projects"
users = ['user1', 'user2', 'user3', 'user4']


def user_buttons():

    html = []
    for user in users:
        html.append(
                f"""<a href = {user}>
                <button type="submit" class=cv_btn>{user}</button>
                </a>
                """
        )
    html = '\n'.join(html)
    return html


def readFile(fileDir, fileName):
    filePath = f"{fileDir}/{fileName}"
    if not os.path.isfile(filePath):
        return f"No file {fileName} in {fileDir}"
    return open(filePath)


def getProjectsList(userN):
    numbers = []
    USER_DIR = f"{PROJECT_DIR}/{userN}"
    with os.scandir(USER_DIR) as ed:
        for entry in ed:
            if entry.is_dir():
                name = entry.name
                if name.isdigit():
                    numbers.append(int(name))
    return sorted(numbers)


def dcReaderJSON(dcDir, dcField):
    # to read different values from the Dublin core file
    dcFile = "dc.json"
    fh = readFile(dcDir, dcFile)
    if type(fh) is str:
        dcJson = {}
    else:
        dcJson = json.load(fh)

    if dcField in dcJson:
        dcFieldValue = dcJson[dcField]
    else:
        dcFieldValue = "Requested information not available"
    return dcFieldValue
