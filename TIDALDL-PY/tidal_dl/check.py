import os
from aigpy import fileHelper

class CheckTool(object):
    def __init__(self):
        self.paths    = []

    def isInErr(self, index, errIndex):
        for i in errIndex:
            if i == index:
                return True
        return False
    def clear(self):
        self.paths    = []
    def addPath(self, path):
        self.paths.append(path)
    def checkPaths(self): 
        index    = 0
        flag     = False
        errIndex = []
        for path in self.paths:
            if fileHelper.getFileSize(path) <= 0:
                errIndex.append(index)
                flag = True
            index = index + 1
        return flag, errIndex

