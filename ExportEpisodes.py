import sys
import os
import os.path
import re
import shutil
import json
import copy
import filecmp
from Utils.InteractionUtils import InteractionUtils
from Utils.FileUtils import FileUtils

def buildExportJobs(inDirectory, outDirectory, tempDirectory):
    listDir = [o for o in os.listdir(inDirectory) if (os.path.isdir(os.path.join(inDirectory,o)) and re.search("[0-9][0-9][0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9][0-9][0-9]", o))]
    allArray = []
    targetedArray = []
    if len(listDir)>0:
        allArray = ["All"]
    dirChoiceList = allArray + listDir + ["Return to Main menu"]
    theBuildDirectoryChoice = 0
    while (theBuildDirectoryChoice != -1 and theBuildDirectoryChoice != (len(dirChoiceList)-1)):
        theBuildDirectoryChoice = InteractionUtils.query_choice_list("Choose the targeted directory(ies).", dirChoiceList, True)
        if (theBuildDirectoryChoice > 0 and theBuildDirectoryChoice != (len(dirChoiceList)-1)):
            targetedArray.append(listDir[theBuildDirectoryChoice - 1])
        elif theBuildDirectoryChoice == 0:
            targetedArray = listDir
        elif (theBuildDirectoryChoice == -1 or theBuildDirectoryChoice == (len(dirChoiceList)-1)):
            break
        for aDir in targetedArray:
            print ("##########################################################################")
            print ("We build the export Jobs for directory '"+aDir+"' with file '"+aDir+".fej'")
            exportJobDoneFileName = os.path.join(tempDirectory,aDir+".ejd")
            jobOrderFileName = os.path.join(tempDirectory,aDir+".fej")
            associationTable = FileUtils.importFileOrCreateDict(jobOrderFileName)
            excludedArray = FileUtils.importFileOrCreateArray(exportJobDoneFileName)
            aWeekDirPath = os.path.join(inDirectory, aDir)
            listEpisode = [o for o in os.listdir(aWeekDirPath) if (os.path.isfile(os.path.join(aWeekDirPath,o)) and not o.endswith('.srt'))]
            for anEpisode in listEpisode:
                if(anEpisode not in excludedArray and os.path.join(aDir, anEpisode) not in associationTable.keys()):
                    episodeChoiceList = ["Build export for this episode", "Skip the episode", "Ignore the episode", "Return to folder choice"]
                    exportAnswer = int(InteractionUtils.query_choice_list("Choose your action for '"+anEpisode+"'.", episodeChoiceList, True))
                    if exportAnswer == 0:
                        buildJobForEpisode(aDir, anEpisode, associationTable, outDirectory)
                    elif exportAnswer == 2:
                        excludedAnEpisode(anEpisode, excludedArray, aWeekDirPath)
                    elif exportAnswer == 3:
                        break
            FileUtils.writeFile(jobOrderFileName, associationTable)
            FileUtils.writeFile(exportJobDoneFileName, excludedArray)



def excludedAnEpisode(anEpisode, excludedArray, aDirPath):
    if anEpisode not in excludedArray:
        excludedArray.append(anEpisode)
    if(os.path.exists(os.path.join(aDirPath, (anEpisode[:-4]+".srt")))) and ((anEpisode[:-4]+".srt") not in excludedArray):
        excludedArray.append(anEpisode[:-4]+".srt")

def buildJobForEpisode(aDir, anEpisode, associationTable, outDirectory):
    listSerieOut = [o for o in os.listdir(outDirectory) if os.path.isdir(os.path.join(outDirectory, o))]
    listSerieOut.sort()
    answer = InteractionUtils.query_choice_list(
        "For file '" + anEpisode + "', is the show is in the following list ? If yes, please write the corresponding index. If not type -1.",
        listSerieOut)
    if answer is None:
        answer = InteractionUtils.query_string("Type the name of the show: ")
        newPath = os.path.join(outDirectory, answer)
        if not os.path.exists(newPath):
            os.makedirs(newPath)
    showDirectory = os.path.join(outDirectory, answer)
    if os.path.exists(showDirectory):
        listSeasonOut = [o for o in os.listdir(showDirectory) if os.path.isdir(os.path.join(showDirectory, o))]
        answerSeason = InteractionUtils.query_choice_list(
            "For file '" + anEpisode + "', is the season is in the following list ? If yes, please write the corresponding index. If not type -1.",
            listSeasonOut)
        if answerSeason is None:
            answerSeason = InteractionUtils.query_string("Type the name for the folder corresponding to the season: ")
            newPath = os.path.join(showDirectory, answerSeason)
            if not os.path.exists(newPath):
                os.makedirs(newPath)
        showSeason = os.path.join(showDirectory, answerSeason)
        if os.path.exists(showSeason):
            if InteractionUtils.query_yes_no("Do you want to copy episode '" + anEpisode + "' and subtitle to this folder : '" + showSeason + "' ?"):
                videoPath = os.path.join(aDir, anEpisode)
                subPath = None
                if os.path.exists(os.path.join(showSeason, anEpisode)):
                    print("Video file already transferred")
                else:
                    associationTable[videoPath] = showSeason
                    print("Copy '" + videoPath + "' to '" + showSeason + "'")
                if not os.path.exists(os.path.join(showSeason, anEpisode[:-4] + ".srt")):
                    if os.path.exists(os.path.join(aDir, anEpisode[:-4] + ".srt")):
                        print("Sub file already transferred")
                    else:
                        subPath = os.path.join(aDir, anEpisode[:-4] + ".srt")
                        print("Copy '" + subPath + "' to '" + showSeason + "'")
                        associationTable[subPath] = showSeason
                else:
                    print ("No Sub file found")


def runExportJobs(inDirectory, tempDirectory):
    listJob = [o for o in os.listdir(tempDirectory) if (os.path.isfile(os.path.join(tempDirectory,o)) and o.endswith('.fej'))]
    allArray = []
    if len(listJob)>0:
        allArray = ["All"]
    dirChoiceList = allArray + listJob + ["Return to Main menu"]
    theRunDirectoryChoice = 0
    while (theRunDirectoryChoice != -1 and theRunDirectoryChoice != (len(dirChoiceList)-1)):
        targetedJob = []
        theRunDirectoryChoice = InteractionUtils.query_choice_list("Choose the targeted directory(ies).", dirChoiceList, True)
        if (theRunDirectoryChoice > 0 and theRunDirectoryChoice != (len(dirChoiceList)-1)):
            targetedJob.append(listJob[theRunDirectoryChoice - 1])
        elif theRunDirectoryChoice == 0:
            targetedJob = listJob
        elif (theRunDirectoryChoice == -1 or theRunDirectoryChoice == (len(dirChoiceList)-1)):
            break
        for aJobFile in targetedJob:
            excludedEpisodePath = os.path.join(tempDirectory,aJobFile[:-4]+'.ejd')
            jobListPath = os.path.join(tempDirectory,aJobFile)
            excludedEpisode = FileUtils.importFileOrCreateArray(excludedEpisodePath)
            jobList = FileUtils.importFileOrCreateDict(jobListPath)
            print(jobList)
            jobListBis = copy.deepcopy(jobList)
            indexJobList = 1
            for src, dest in jobList.items():
                print ("["+str(indexJobList)+"/"+str(len(jobList.items()))+"]Move '"+src[14:]+"' to '"+dest+"'.")
                newDest = os.path.join(dest, src[14:])
                oldDest = os.path.join(inDirectory,src)
                if os.path.exists(newDest) and not filecmp.cmp(oldDest,newDest):
                    os.remove(newDest)
                if not os.path.exists(newDest):
                    shutil.copy(oldDest,dest)
                excludedEpisode.append(src[14:])
                del jobListBis[src]
                FileUtils.writeFile(jobListPath, jobListBis)
                FileUtils.writeFile(excludedEpisodePath, excludedEpisode)
                indexJobList +=1
debug = False
inDirectory = r"C:\Users\nogebour\Videos\Others"
outDirectory = r"\\DLINK-5CA002\Volume_1\Workspace\Nicolas\Série"
tempDirectory = r"C:\Users\nogebour\Videos\ScriptFolder\ExportEpisodes"
if debug:
    inDirectory = r"C:\Users\nogebour\Videos\Others\ExtractSeries"
    #directory = r"C:\Users\nogebour\Videos\Others\Subtitle"
mainMenuChoice = ["Build export orders","Launch export jobs","Quit"]
theMainChoice = 0
while (theMainChoice != -1 and theMainChoice != (len(mainMenuChoice)-1)):
    theMainChoice = int(InteractionUtils.query_choice_list("Welcome in Export Episodes. Choose your mode:", mainMenuChoice, True))
    if theMainChoice == 0:
        buildExportJobs(inDirectory, outDirectory, tempDirectory)
    elif theMainChoice == 1:
        runExportJobs(inDirectory, tempDirectory)