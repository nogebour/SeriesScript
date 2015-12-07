import sys
import os
import os.path
import re
import shutil
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")
def representsInt(s):
    try:
        int(s)
        return True, int(s)
    except ValueError:
        return False, 0

def query_choice_list(question, possibleValues, valueNo=-1):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    while True:
        sys.stdout.write(question +'[0-'+str(len(possibleValues)-1)+']:\n')
        anIndex = 0
        for aValue in possibleValues:
            sys.stdout.write(str(anIndex)+'-"'+aValue+'"\n')
            anIndex+=1
        isOk, theValue = representsInt(input())
        if isOk and theValue >= 0 and theValue < len(possibleValues):
            return possibleValues[theValue]
        elif isOk and theValue == valueNo:
            return None
        else:
            sys.stdout.write("Please respond with an integer between 0 and "+str(len(possibleValues)-1)+"\n")

def query_string(question):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    while True:
        sys.stdout.write(question)
        theValue = input()
        sys.stdout.write("Do you confirm this value ? '"+theValue+"'")
        theConfirmValue = input().lower()
        if theConfirmValue in valid:
            return theValue

debug = False
inDirectory = r"C:\Users\nogebour\Videos\Others"
outDirectory = r"\\DLINK-5CA002\Volume_1\Workspace\Nicolas\Série"
if debug:
    inDirectory = r"C:\Users\nogebour\Videos\Others\ExtractSeries"
    #directory = r"C:\Users\nogebour\Videos\Others\Subtitle"
listDir = [os.path.join(inDirectory,o) for o in os.listdir(inDirectory) if (os.path.isdir(os.path.join(inDirectory,o)) and re.search("[0-9][0-9][0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9][0-9][0-9]", o))]
for aDir in listDir:
    listEpisode = [o for o in os.listdir(aDir) if (os.path.isfile(os.path.join(aDir,o)) and not o.endswith('.srt'))]
    for anEpisode in listEpisode:
        listSerieOut = [o for o in os.listdir(outDirectory) if os.path.isdir(os.path.join(outDirectory,o))]
        exportAnswer = query_yes_no("Do you want to export this file '"+anEpisode+"' ?")
        if exportAnswer:
            listSerieOut.sort()
            answer = query_choice_list("For file '"+anEpisode+"', is the show is in the following list ? If yes, please write the corresponding index. If not type -1.", listSerieOut)
            if answer is None:
                answer = query_string("Type the name of the show: ")
                newPath = os.path.join(outDirectory,answer)
                if not os.path.exists(newPath):
                    os.makedirs(newPath)
            showDirectory = os.path.join(outDirectory,answer)
            if os.path.exists(showDirectory):
                listSeasonOut = [o for o in os.listdir(showDirectory) if os.path.isdir(os.path.join(showDirectory,o))]
                answerSeason = query_choice_list("For file '"+anEpisode+"', is the season is in the following list ? If yes, please write the corresponding index. If not type -1.", listSeasonOut)
                if answerSeason is None:
                    answerSeason = query_string("Type the name for the folder corresponding to the season: ")
                    newPath = os.path.join(showDirectory,answerSeason)
                    if not os.path.exists(newPath):
                        os.makedirs(newPath)
                showSeason = os.path.join(showDirectory,answerSeason)
                if os.path.exists(showSeason):
                    if query_yes_no("Do you want to copy episode '"+anEpisode+"' and subtitle to this folder : '"+showSeason+"' ?"):
                        videoPath = os.path.join(aDir, anEpisode)
                        subPath = None
                        if os.path.exists(os.path.join(showSeason, anEpisode)):
                            print("File already transferred")
                        else:
                            shutil.copy(videoPath, showSeason)
                            print("Copy '"+videoPath+"' to '"+showSeason+"'")
                        if os.path.exists(os.path.join(aDir, anEpisode[:-4]+".srt")):
                            if os.path.exists(os.path.join(showSeason, anEpisode[:-4]+".srt")):
                                print("File already transferred")
                            else:
                                subPath = os.path.join(aDir, anEpisode[:-4]+".srt")
                                print("Copy '"+subPath+"' to '"+showSeason+"'")
                                shutil.copy(subPath, showSeason)
