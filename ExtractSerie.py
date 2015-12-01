import os
import os.path
import shutil
import re
debug = False
directory = r"C:\Users\nogebour\Videos\Others"
if debug:
    directory = r"C:\Users\nogebour\Videos\Others\ExtractSeries"
    #directory = r"C:\Users\nogebour\Videos\Others\Subtitle"
listDir = [os.path.join(directory,o) for o in os.listdir(directory) if (os.path.isdir(os.path.join(directory,o)) and re.search("[0-9][0-9][0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9][0-9][0-9]", o))]
for aDir in listDir:
    listEpisodes = [os.path.join(aDir,o) for o in os.listdir(aDir) if os.path.isdir(os.path.join(aDir,o))]
    for anEpisode in listEpisodes:
        listFiles = [f for f in os.listdir(anEpisode) if os.path.isfile(os.path.join(anEpisode, f))]
        print(listFiles)
        for file in listFiles:
            if file.endswith('.mp4') \
            or file.endswith('.MP4') \
            or file.endswith('.AVI') \
            or file.endswith('.avi') \
            or file.endswith('.MKV') \
            or file.endswith('.mkv') :
                print (os.path.join(anEpisode,file))
                shutil.copy(os.path.join(anEpisode,file), aDir)