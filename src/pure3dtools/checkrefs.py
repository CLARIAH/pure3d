"""
# Check references in articles

All href and src references in articles will be checked.
Only html files are being searched.

They will be listed as

* online references
* local refererences resolvable in the media folder
* unresolvable references

Identical references are grouped, and its occurrences indicated.
"""


import sys
import os
import re
import collections


HELP = """
USAGE
checkrefs --help
checkrefs indir

EFFECT

If --help is present, prints this text and exits.

indir is the input directory, usually an articles directory

The report will be written to stdout.
"""


OUTFILE_DEFAULT = "refs.txt"


REF_RE = re.compile(
    r"""
    \b(src|href)
    =
    ['"]
    ([^'"]*)
    ['"]
    """,
    re.X | re.I,
)

ONLINE_RE = re.compile(r"""^https?://""", re.I)


STATUS = {
    0: "resolved",
    1: "missing",
    2: "online",
    3: "outside",
    4: "exists but indirect reference",
}

SKIP = set(
    """
 .DS_Store
""".strip().split()
)


def checkLinks(inDir, references, mediaFiles):
    links = collections.defaultdict(
        lambda: collections.defaultdict(lambda: collections.defaultdict(list))
    )
    media = {f"{path}{'/' if path else ''}{name}": 0 for (path, name) in mediaFiles}

    for (path, name, ln, kind, url) in references:
        sep = "/" if path else ""
        filePath = f"{path}{sep}{name}"
        refPath = f"{path}{sep}{url}"

        if url.startswith(".."):
            status = 3
        elif ONLINE_RE.match(url):
            status = 2
        elif os.path.exists(f"{inDir}/{refPath}"):
            if refPath not in media:
                status = 4
            else:
                status = 0
                media[refPath] += 1
        else:
            status = 1

        links[status][url][filePath].append(ln)

    printLinks(links)
    printMedia(media)

    linkStatus = 1 if 1 in links else 2 if 2 in links else 0
    mediaStatus = 10 if all(m == 0 for m in media.values()) else 0

    return linkStatus if linkStatus else mediaStatus


def printLinks(links):
    for (status, linkData) in sorted(links.items()):
        statusRep = STATUS[status]
        print(statusRep)
        for (url, locData) in sorted(linkData.items()):
            print(f"\t{url}")
            for (path, lns) in sorted(locData.items()):
                print(f"\t\t{path} ==> {', '.join(str(ln + 1) for ln in lns)}")


def printMedia(media):
    for name in sorted(nm for (nm, m) in media.items() if m == 0):
        print(f"UNREFERENCED: {name}")
    print(f"{len(media):>4} media files of which:")
    print(f"{sum(1 for m in media.values() if m == 1):>4} referenced exactly once")
    print(f"{sum(1 for m in media.values() if m > 1):>4} referenced more than once")
    print(f"{sum(1 for m in media.values() if m == 0):>4} unreferenced")


def checkRef(inDir, path, name, references):
    sep1 = "/" if path and inDir else ""
    sep2 = "/" if path or inDir else ""

    with open(f"{inDir}{sep1}{path}{sep2}{name}") as fh:
        for (i, line) in enumerate(fh):
            for (kind, url) in REF_RE.findall(line):
                references.append((path, name, i, kind, url))


def checkRefs(inDir, path, references, mediaFiles):
    sep = "/" if path and inDir else ""
    with os.scandir(f"{inDir}{sep}{path}") as dh:
        for entry in dh:
            name = entry.name

            if entry.is_file():
                if name.lower().endswith(".html"):
                    checkRef(inDir, path, name, references)
                elif name not in SKIP:
                    mediaFiles.append((path, name))
            elif entry.is_dir():
                sep = "/" if path else ""
                checkRefs(inDir, f"{path}{sep}{name}", references, mediaFiles)


def main():
    args = sys.argv[1:]
    if not args or "--help" in args:
        print(HELP)
        return 0

    inDir = None

    for arg in args:
        if inDir is None:
            inDir = arg
        else:
            print(HELP)
            print(f"Too many input directories: {arg}")
            return -1

    if inDir is None:
        print(HELP)
        print("No input file")
        return -1

    if not os.path.isdir(inDir):
        print(f"Input directory does not exist: {inDir}")
        return -1

    references = []
    mediaFiles = []

    result = checkRefs(inDir, "", references, mediaFiles)
    checkLinks(inDir, references, mediaFiles)

    return result


if __name__ == "__main__":
    main()
