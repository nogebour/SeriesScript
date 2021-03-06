import sys
import os
import os.path
import re
import operator
from difflib import SequenceMatcher
from Utils.InteractionUtils import InteractionUtils

debug = False
directory = r"C:\Users\nogebour\Videos\Others"
if debug:
    #directory = r"C:\Users\nogebour\Videos\Others\ExtractSeries"
    directory = r"C:\Users\nogebour\Videos\Others\Subtitle"
listDir = [os.path.join(directory,o) for o in os.listdir(directory) if (os.path.isdir(os.path.join(directory,o)) and re.search("[0-9][0-9][0-9][0-9][0-9][0-9]_[0-9][0-9][0-9][0-9][0-9][0-9]", o))]
for aDir in listDir:
    excludedSub = []
    association = {}
    tmpEpisode = []
    listSubtitle = []
    for o in os.listdir(aDir) :
        if not os.path.isdir(os.path.join(aDir,o)):
            #aFile = os.path.join(aDir,o)
            aFile = o
            aLowerfile = aFile.lower()
            if aLowerfile.endswith('.mp4') \
            or aLowerfile.endswith('.mkv') \
            or aLowerfile.endswith('.avi'):
                tmpEpisode.append(aFile)
            if aLowerfile.endswith('.srt'):
                listSubtitle.append(aFile)
    for aVideo in tmpEpisode:
        truncatedVideo = aVideo[:-4]
        alreadySync = False
        for aSubtitle in listSubtitle:
            if truncatedVideo in aSubtitle:
                alreadySync = True
                break
        if alreadySync:
            listSubtitle.remove(truncatedVideo+'.srt')
        else:
            result = {}
            title = ''
            if re.match('.*[.|\s]S[0-9][0-9]E[0-3][0-9]', truncatedVideo, re.IGNORECASE):
                title = re.search('(.*)[.|\s]S[0-9][0-9]E[0-3][0-9]', truncatedVideo, re.IGNORECASE).group(1)
            if re.match('.*[.|\s][0-9]?[0-9][0-3][0-9]', truncatedVideo, re.IGNORECASE):
                title = re.search('(.*)[.|\s][0-9]?[0-9][0-3][0-9]', truncatedVideo, re.IGNORECASE).group(1)
            title = title.replace(' ','')
            title = title.replace('.','')
            title = title.lower()
            for aSub in listSubtitle:
                subTitle = None
                if re.match('.* - [0-9][0-9]x[0-3][0-9]', aSub, re.IGNORECASE):
                    subTitle = re.search('(.*) - [0-9][0-9]x[0-3][0-9]', aSub, re.IGNORECASE).group(1)
                if subTitle is not None:
                    subTitle = subTitle.lower()
                    subTitle = subTitle.replace(' ','')
                    seq=SequenceMatcher(None,title, subTitle)
                    result[aSub]=seq.ratio()
            sortedSub = reversed(sorted(result.items(), key=operator.itemgetter(1)))
            print ("##################################")
            print ("For episode : "+aVideo)
            for aResult in sortedSub:
                if aResult[0] not in excludedSub and InteractionUtils.query_yes_no("Associate '"+aResult[0]+"' with this episode ?"):
                    association[aVideo] = aResult[0]
                    excludedSub.append(aResult[0])
                    break
    for anAsso in association.keys():
        newSrtFileName = (anAsso[:-4])+".srt"
        if InteractionUtils.query_yes_no("Rename '"+association[anAsso]+"' to "+newSrtFileName):
            os.rename(os.path.join(aDir,association[anAsso]), os.path.join(aDir,newSrtFileName))