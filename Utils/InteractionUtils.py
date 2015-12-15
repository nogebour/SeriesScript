import sys

class InteractionUtils:
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

    def query_choice_list(question, possibleValues, returnIndex = False, valueNo=-1):
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
            isOk, theValue = InteractionUtils.representsInt(input())
            if isOk and theValue >= 0 and theValue < len(possibleValues):
                if returnIndex:
                    return theValue
                else:
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

    def query_int(question):
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
            isInt, theIntValue = InteractionUtils.representsInt(theValue)
            while not isInt:
                sys.stdout.write(question)
                theValue = input()
                isInt, theIntValue = InteractionUtils.representsInt(theValue)
            sys.stdout.write("Do you confirm this value ? '"+theValue+"'")
            theConfirmValue = input().lower()
            if theConfirmValue in valid:
                return theIntValue