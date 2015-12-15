import json
import os.path
class FileUtils:
    def importFile(path):
        file = open(path, 'r')
        result = json.loads(file.read())
        file.close()
        return result

    def importFileOrCreateArray(path):
        result = []
        if os.path.exists(path) and os.path.isfile(path):
            result = FileUtils.importFile(path)
        return result

    def importFileOrCreateDict(path):
        result = {}
        if os.path.exists(path) and os.path.isfile(path):
            result = FileUtils.importFile(path)
        return result

    def writeFile (pathToFile, objectToWrite):
        file = open(pathToFile, 'w')
        file.write(json.dumps(objectToWrite))
        file.close()
