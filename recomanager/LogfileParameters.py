import os
from ij import IJ

class LogfileParameters:

    def __init__(self):

        self.setToDefaults()

    def setToDefaults(self):

        self.dataset = ""
        self.filepath = ""
        self.datasetOut = ""
        self.datasetValid = False
        self.logdir = ""
        self.logfile = ""
        self.diskName = ""
        self.samplename = ""
        self.datasetType = ""
        self.beamlineStorage = 0
        self.scanType = "Standard"
        self.spOption = "False"

        self.center = "0"
        self.stitchedCenter = "0"
        self.foundOriginal = 0
        self.foundStitched = 0
        self.originalRoiX = "0"
        self.nprj = "0"
        self.ndrk = "0"
        self.nflt = "0"
        self.minY = 0
        self.maxY = 180
        self.rotationAxisPosition = "Standard"

    def readLogfile(self):

        try:
            FILE = open(self.logfile,"r")
            self.datasetValid = True
            for line in FILE:
                linelist=line.split()
                if len(linelist)>0:
                    if linelist[0]=="Original" and linelist[1]=="rotation" and len(linelist)==5 and self.foundOriginal==0:
                        self.center=linelist[4]
                        self.foundOriginal=1
                    elif linelist[0]=="Original" and linelist[1]=="rotation" and len(linelist)==4 and self.foundOriginal==0:
                        self.center=linelist[3]
                        self.foundOriginal=1
                    elif linelist[0]=="Rotation" and linelist[1]=="center" and len(linelist)==7 and self.foundStitched==0:
                        self.stitchedCenter=linelist[6]
                        self.foundStitched=1
                    elif linelist[0]=="X-ROI" and len(linelist)==5:
                        self.originalRoiX=str(int(linelist[4]) - int(linelist[2]) + 1)
                    elif linelist[0]=="Number" and linelist[2]=="projections":
                        self.nprj=linelist[4]
                    elif linelist[0]=="Number" and linelist[2]=="darks":
                        self.ndrk=linelist[4]
                    elif linelist[0]=="Number" and linelist[2]=="flats":
                        self.nflt=linelist[4]
                    elif linelist[0]=="Rot" and linelist[2]=="min":
                        self.minY=linelist[6]
                    elif linelist[0]=="Rot" and linelist[2]=="max":
                        self.maxY=linelist[6]
                    elif linelist[0]=="Rotation" and linelist[1]=="axis":
                        self.rotationAxisPosition=linelist[4]
                    elif linelist[0]=="Double":
                        self.spOption=linelist[4]
            FILE.close()

        except IOError:
            IJ.showMessage("The file " + self.logfile + " could not be opened!")
