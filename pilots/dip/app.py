from flask import Flask, render_template, url_for, abort, make_response
import os
import sys
import json
from markdown import markdown

from helpers.messages import Messages
from helpers.files import readFile, dirExists

# create and configure app
app = Flask(__name__)
app.secret_key = "dev"
title = "PURE3D: An Infrastructure for Publication and Preservation of 3D Scholarship"
heading = "Pure 3D website"

# variables
BASE = os.path.expanduser("~/github/clariah/pure3d")
DATA_DIR = f"{BASE}/data"
PROJECT_DIR = f"{DATA_DIR}/projects"


# functions
def getProjectsList(M):
    # to get enumeration of top level directories
    # these are joined with the "project" directory path to get
    # path of each project
    numbers = []

    if not dirExists(PROJECT_DIR):
        M.addMessage("error", f"Project directory {PROJECT_DIR} does not exist")
        return numbers

    with os.scandir(PROJECT_DIR) as ed:
        for entry in ed:
            if entry.is_dir():
                name = entry.name
                if name.isdigit():
                    numbers.append(int(name))
    return sorted(numbers)


def getEditionsList(M, projectN):
    # to get enumeration of sub-directories under folder "editions"
    editionNs = []
    editionDir = f"{PROJECT_DIR}/{projectN}/editions"
    with os.scandir(editionDir) as md:
        for edition in md:
            if edition.is_dir():
                name = edition.name
                if name.isdigit():
                    editionNs.append(int(name))
    return sorted(editionNs)


def render_md(M, mdPath, mdFile):
    # to render markdown files
    fileDir = f"{mdPath}/texts"
    fh = readFile(fileDir, mdFile)
    if type(fh) is str:
        M.addMessage("error", fh)
        html = ""
    else:
        text = fh.read()
        html = markdown(text)
    return html


def dcReaderJSON(M, dcDir, dcField):
    # to read different values from the Dublin core file
    dcFile = "dc.json"
    fh = readFile(dcDir, dcFile)
    if type(fh) is str:
        M.addMessage("error", fh)
        dcJson = {}
    else:
        dcJson = json.load(fh)

    if dcField in dcJson:
        dcFieldValue = dcJson[dcField]
    else:
        M.addMessage("warning", "No 'dc.title' in Dublin Core metadata")
        dcFieldValue = "Requested information not avilable"
    return dcFieldValue


def debug(msg):
    sys.stderr.write(f"{msg}\n")
    sys.stderr.flush()


def projectUrls():
    pass


def editionUrls():
    pass


# app url routes start here


@app.route("/")
@app.route("/home")
# Display home page
def home():
    M = Messages(app)

    return render_template(
        "index.html",
    )


@app.route("/about")
# Display the About page
def about():
    M = Messages(app)

    fileDir = f"{BASE}/src/dip"
    fileName = "about.md"
    fh = readFile(fileDir, fileName)
    if type(fh) is str:
        M.addMessage("error", fh)
        text = ""
    else:
        text = fh.read()

    html = markdown(text)

    return render_template(
        "about.html",
        about=html,
        messages=M.generateMessages(),
    )


@app.route("/projects")
def projects():
    M = Messages(app)

    # display list of projects on home page
    # used "dc.title" from the Dublin Core metadata
    projectNumbers = getProjectsList(M)

    projectData = {}

    for i in projectNumbers:
        jsonDir = f"{PROJECT_DIR}/{i}/meta"
        jsonField = "dc.title"
        title = dcReaderJSON(M, jsonDir, jsonField)

        url = f"""/{i}"""

        candy = f"projects/{i}/candy/icon.png"

        # display project logo as banner
        logo = url_for("data", path=candy)

        projectData[i] = dict(title=title, url=url, logo=logo)

    projectLinks = []  # to get url redirections of individual pages of each project

    for (i, data) in sorted(projectData.items()):
        title = data["title"]
        url = data["url"]
        logo = data["logo"]
        projectLinks.append(
            f"""
            <a href="{url}"><img src="{logo}"></a><br>
            <a href="{url}">{title}</a><br>
        """
        )

    projectLinks = "\n".join(projectLinks)

    return render_template(
        "projectList.html",
        url=url,
        title=title,
        projectLinks=projectLinks,
        messages=M.generateMessages(),
    )


@app.route("/suprise-me")
def supriseme():
    # M = Messages(app)

    pass


@app.route("/login")
def login():
    # M = Messages(app)

    pass


@app.route("/register")
def register():
    # M = Messages(app)

    pass


@app.route("/<int:projectN>/about")
# Display about page for specific project
def projectAbout(projectN):
    M = Messages(app)

    aboutDir = f"{PROJECT_DIR}/{projectN}"
    aboutFile = "about.md"
    aboutHtml = render_md(M, aboutDir, aboutFile)

    homeUrl = url_for("project_page", projectN=projectN)
    bgUrl = url_for("projectBackground", projectN=projectN)

    return render_template(
        "projectTexts.html",
        text=aboutHtml,
        homeUrl=homeUrl,
        bgUrl=bgUrl,
        messages=M.generateMessages(),
    )


@app.route("/<int:projectN>/<int:editionN>")
# Display page for individual editions in an project
def edition_page(projectN, editionN):
    M = Messages(app)

    ed = f"{PROJECT_DIR}/{projectN}/editions/{editionN}"  # edition directory on filesystem
    root = f"data/projects/{projectN}/editions/{editionN}/"  # edition root url

    candyLogo = f"projects/{projectN}/candy/logo.png"

    # display project logo as banner
    logo = url_for("data", path=candyLogo)

    # render About information
    aboutFile = "about.md"
    aboutHtml = render_md(M, ed, aboutFile)

    # urls for different tabs on the project page
    homeUrl = url_for("project_page", projectN=projectN)
    aboutUrl = url_for("projectAbout", projectN=projectN)
    bgUrl = url_for("projectBackground", projectN=projectN)

    # displaying 3d editions
    # accesses the scene file
    for file in os.listdir(ed):
        if file.endswith(".json"):
            scene = file

    return render_template(
        "edition.html",
        aboutHtml=aboutHtml,
        projectN=projectN,
        editionN=editionN,
        scene=scene,
        height="600px",
        width="600px",
        homeUrl=homeUrl,
        aboutUrl=aboutUrl,
        bgUrl=bgUrl,
        root=root,
        logo=logo,
        messages=M.generateMessages(),
    )


@app.route("/voyager/<string:scene>/<path:root>")
def voyager(scene, root):
    # url for voyager in explorer mode
    M = Messages(app)
    ext = "min"
    root = f"/{root}"
    return render_template(
        "voyager.html", ext=ext, root=root, scene=scene, messages=M.generateMessages()
    )


@app.route("/data/<path:path>")
def data(path):
    # url accesing data from the projects
    dataPath = f"{DATA_DIR}/{path}"
    if not os.path.isfile(dataPath):
        debug(f"File does not exist: {dataPath}")
        abort(404)

    with open(dataPath, "rb") as fh:
        textData = fh.read()

    return make_response(textData)


@app.route("/<int:projectN>", methods=["GET", "POST"])
# Display for projects page(s)
def project_page(projectN):
    M = Messages(app)

    pd = f"{PROJECT_DIR}/{projectN}"
    candyLogo = f"projects/{projectN}/candy/logo.png"

    # display title
    jsonDir = f"{PROJECT_DIR}/{projectN}/meta"
    jsonField = "dc.title"
    pd_title = dcReaderJSON(M, jsonDir, jsonField)

    # display project logo as banner
    logo = url_for("data", path=candyLogo)

    # rendering texts
    introFile = "intro.md"
    usageFile = "usage.md"

    introHtml = render_md(M, pd, introFile)
    usageHtml = render_md(M, pd, usageFile)

    # url variables for tabs on page
    aboutUrl = url_for("projectAbout", projectN=projectN)
    bgUrl = url_for("projectBackground", projectN=projectN)

    # hyper-linked editions list
    editionNumbers = getEditionsList(M, projectN)
    editionData = {}

    for j in editionNumbers:
        editionDir = f"{pd}/editions/{j}"
        editionFile = "title.txt"
        nameFile = os.path.join(editionDir, editionFile)
        with open(nameFile) as f:
            title = f.read()

        url = f"""/{projectN}/{j}"""
        candyIcon = f"projects/{projectN}/editions/{j}/candy/icon.png"
        icon = url_for("data", path=candyIcon)
        editionData[j] = dict(title=title, url=url, icon=icon)

    editionLinks = []

    for (i, data) in sorted(editionData.items()):
        title = data["title"]
        url = data["url"]
        icon = data["icon"]
        editionLinks.append(
            f"""
            <a href="{url}"><img src="{icon}" alt="edition icon"><br>
            <a href="{url}">{title}</a><br>
        """
        )

    editionLinks = "\n".join(editionLinks)

    # show metadata
    dcDir = f"{pd}/meta"
    metaTitle = dcReaderJSON(M, dcDir, "dc.title")
    metaCreator = dcReaderJSON(M, dcDir, "dc.creator")
    metadata = f"""<div class="metafield">
                        <span class="metalabel">Title - {metaTitle}</span><br>
                        <span class="metavalue">Creator - {metaCreator}</span>
                    </div>"""

    editUrl = url_for("editMetadata", projectN=projectN)

    return render_template(
        "project.html",
        usage=usageHtml,
        intro=introHtml,
        editioN=projectN,
        aboutUrl=aboutUrl,
        bgUrl=bgUrl,
        editionLinks=editionLinks,
        logo=logo,
        icon=icon,
        pd_title=pd_title,
        metadata=metadata,
        editUrl=editUrl,
        messages=M.generateMessages(),
    )


@app.route("/<int:projectN>/editMetadata/", methods=("GET", "POST"))
def editMetadata(projectN):
    # adding metadata for projects
    M = Messages(app)
    return render_template(
        "editMetadata.html",
        projectN=projectN,
        messages=M.generateMessages(),
    )


@app.route("/<int:projectN>/project_background")
# Display about page for specific project
def projectBackground(projectN):
    M = Messages(app)
    ed = f"{PROJECT_DIR}/{projectN}"
    backgroundFile = "description.md"
    backgroundHtml = render_md(M, ed, backgroundFile)

    aboutUrl = url_for("projectAbout", projectN=projectN)
    homeUrl = url_for("project_page", projectN=projectN)

    return render_template(
        "projectTexts.html",
        text=backgroundHtml,
        homeUrl=homeUrl,
        aboutUrl=aboutUrl,
        messages=M.generateMessages(),
    )


@app.route("/<int:projectN>/sources")
# Display about page for specific project
def projectSources(projectN):
    # M = Messages(app)
    pass


if __name__ == "__main__":
    app.run()
