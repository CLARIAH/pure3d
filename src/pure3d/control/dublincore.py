import json
from control.helpers.files import readPath


def dcReaderJSON(dcPath, dcField):
    data = readPath(dcPath)
    value = None

    if data:
        dcJson = json.loads(data)
        value = dcJson.get(dcField, None)

    return value
