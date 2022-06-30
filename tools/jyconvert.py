"""
# Convert JSON to YAML and back

"""

import sys
import json
import yaml


HELP = """
USAGE

jyconvert --help
jyconvert infile
jyconvert -o outfile infile

EFFECT

If --help is present, prints this text and exits.

If infile has extension .json it will converted to yaml format;
if it has extension .yaml, it will be converted to json format.

If -o outfile is specified, the resulting file will be saved there,
otherwise the resulting file will be saved in the same directory as infile
with the appropriate extension.
"""


def toYaml(fileIn, fileOut):
    """Converts a json file to a yaml file.

    Parameters
    ----------
    fileIn: str
        Input file, should contain json data
    fileOut: str
        Output file, will contain yaml data.
        If the directory for this file does not exist,
        it will be created.
        If this file already exists, it will be overwritten.

    Returns
    -------
    int
        0 if successfule, else 1
    """

    good = True
    try:
        # here comes the conversion code
        pass
    except Exception as e:
        print(str(e))
        good = False
    return 0 if good else 1


def toJson(fileIn, fileOut):
    """Converts a yaml file to a json file.

    Parameters
    ----------
    fileIn: str
        Input file, should contain yaml data
    fileOut: str
        Output file, will contain json data.
        If the directory for this file does not exist,
        it will be created.
        If this file already exists, it will be overwritten.

    Returns
    -------
    int
        0 if successfule, else 1
    """

    good = True
    try:
        # here comes the conversion code
        pass
    except Exception as e:
        print(str(e))
        good = False
    return 0 if good else 1


def main():
    args = sys.args[1:]
    if not args or "--help" in args:
        print(HELP)
        return 0

    seenO = False

    outFile = None
    inFile = None

    for arg in args:
        if arg == "-o":
            if seenO:
                print(HELP)
                print("Multiple -o in a row")
                return -1
            else:
                seenO = True
        else:
            if seenO:
                if outFile is None:
                    outFile = arg
                    seenO = False
                else:
                    print(HELP)
                    print(f"Too many output files: {arg}")
                    return -1
            else:
                if inFile is None:
                    inFile = arg
                else:
                    print(HELP)
                    print(f"Too many input files: {arg}")
                    return -1

    if inFile is None:
        print(HELP)
        print("No many input file")
        return -1

    if inFile.endswith(".json"):
        inExtension = ".json"
        outExtension = ".yaml"
    elif inFile.endswith(".yaml"):
        inExtension = ".yaml"
        outExtension = ".json"
    else:
        print(HELP)
        print(f"{inFile} should have extension .json or .yaml")
        return -1

    if outFile is None:
        outFile = f"{inFile.removesuffix(inExtension)}{outExtension}"

    if inExtension == ".json":
        return toYaml(inFile, outFile)
    elif inExtension == ".yaml":
        return toJson(inFile, outFile)

    print(HELP)
    print("An unexpected error has occurred")
    return -1


if __name__ == "__main__":
    main()
