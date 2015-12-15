class DisplayListUtils:
    def displayList(self, objectList, titleList, formatTitle):
        maxLength = {}
        for aTitle in titleList:
            maxLength[aTitle] = len(aTitle)
        for anObject in objectList:
            for aTitle in titleList:
                if not isinstance(anObject[aTitle], str):
                    maxLength[aTitle] = max(len(str(anObject[aTitle])), maxLength[aTitle])
                else:
                    maxLength[aTitle] = max(len(anObject[aTitle]), maxLength[aTitle])
        strResult = '|'
        for aTitle in titleList:
            strResult += aTitle.center(maxLength[aTitle])
            strResult += '|'
        print(strResult)
        strResult = '|'
        for aTitle in titleList:
            blanckChar = ''
            strResult += blanckChar.center(maxLength[aTitle],'_')
            strResult += '|'
        print(strResult)
        for anObject in objectList:
            strResult = '|'
            for aTitle in titleList:
                value = None
                if not isinstance(anObject[aTitle], str):
                    value = str(anObject[aTitle])
                else:
                    value = anObject[aTitle]
                if formatTitle[aTitle] == 'l':
                    value = value.ljust(maxLength[aTitle])
                elif formatTitle[aTitle] == 'c':
                    value = value.center(maxLength[aTitle])
                elif formatTitle[aTitle] == 'r':
                    value = value.rjust(maxLength[aTitle])
                strResult += value
                strResult += '|'
            print(strResult)

if __name__ == '__main__':
    object1 = {'id':108530,
              'title':'Remove infinite loop in getOwner()',
              'urgency':'Normal',
              'validationDate':'2015-12-15 15:02:58'}
    object2 = {'id':108427,
              'title':'fix cascading',
              'urgency':'Normal',
              'validationDate':'2015-12-15 13:02:58'}
    objectList = [object1,object2]
    titleList = ['id','title','urgency','validationDate']
    formatTitle = {'id':'l','title':'c','urgency':'r','validationDate':'l'}
    aDisplayObject = DisplayListUtils()
    aDisplayObject.displayList(objectList,titleList,formatTitle)