import os
import sys
from ij import IJ
from os.path import expanduser

class Config:

    def __init__(self):

        self.set()

    def set(self):

        self.dataset = ""
        self.filepath = ""
        self.scanType = "Standard"
        self.center = "0"
        self.originalRoiX = "0"


class RecoParameters:

    def __init__(self, fields):

        self.fields = fields
        self.set()

    def set(self):  

        self.FileLocation = ""
        self.algorithm = 0
        self.energy = "10"
        self.propagationDistance = "60"
        self.pixelSize = "1.34"
        self.alpha = "0.2"
        self.filtersIndex = 5
        # self.filtersUsed = "Parzen"
        # self.cutOffFrequency = "0.5"
        # self.filterOption = "parzen"
        self.center = "1024"
        self.stripeMethod = 0
        # self.stripeMethodIndex = 0
        self.slice = "1"
        self.centerSearchWidth= "10"
        self.nsinoperchunk = "256"
        # self.guiCenter = "0"
        home = expanduser("~")
        self.pfname = os.path.join(home, "GUIParameters.txt")

    def readParametersFromFile(self):
        
        print("Read from local file")
        FILE = open(self.pfname,"r")
        for line in FILE:
            linelist=line.split()
            if len(linelist)>0:
                if linelist[0] == "FileName":
                    self.FileLocation = linelist[1]
                elif linelist[0] == "Algorithm":
                    self.algorithm = linelist[1]
                elif linelist[0] == "Energy":
                    self.energy = linelist[1]
                elif linelist[0] == "PropagationDistance":
                    self.propagationDistance = linelist[1]
                elif linelist[0] == "PixelSize":
                    self.pixelSize = linelist[1]
                elif linelist[0] == "Alpha":
                    self.alpha = linelist[1]
                elif linelist[0] == "Filter":
                    self.filtersIndex=int(linelist[1])            
                elif linelist[0] == "Center":
                    self.center = linelist[1]
                elif linelist[0] == "RemoveStripeMethod":
                    self.stripeMethod = linelist[1]
                elif linelist[0] == "Slice":
                    self.slice = linelist[1]
                elif linelist[0] == "SearchWidth":
                    self.centerSearchWidth = linelist[1]
                elif linelist[0] == "nsino-per-chunk":
                    self.nsinoperchunk = linelist[1]
        FILE.close()        
        

    def readParametersFromGUI(self,originalRoiX):
    
        self.FileLocation = self.fields.selectedDatasetField.getText()
        self.algorithm = self.fields.algoChooser.getSelectedIndex()
        self.energy = self.fields.energyField.getText()
        self.propagationDistance = self.fields.propagationDistanceField.getText()
        self.pixelSize = self.fields.pixelSizeField.getText()
        self.alpha = self.fields.alphaField.getText()
        self.filtersIndex = self.fields.filtersChooser.getSelectedIndex()
        self.filtersUsed = self.fields.filtersList[self.filtersIndex]
        if self.filtersIndex==0:
            self.filtersOption = "none"
        elif self.filtersIndex==1:
            self.filtersOption = "shepp"
        elif self.filtersIndex==2:
            self.filtersOption = "hann"
        elif self.filtersIndex==3:
            self.filtersOption = "hammimg"
        elif self.filtersIndex==4:
            self.filtersOption = "ramlak"
        elif self.filtersIndex==5:
            self.filtersOption = "parzen"
        elif self.filtersIndex==6:
            self.filtersOption = "cosine"
        elif self.filtersIndex==7:
            self.filterOption = "butterworth"

        self.center = self.fields.centerField.getText()
        self.stripeMethod = self.fields.stripeMethodChooser.getSelectedIndex()
        self.slice = self.fields.sliceField.getText()
        self.centerSearchWidth = self.fields.centerSearchField.getText()
        self.nsinoperchunk = self.fields.nsinochunkField.getText()

        if self.fields.localButton.isSelected():
            self.queue="local"
            print "local cluster is selected"
        elif self.fields.lcrcButton.isSelected():
            self.queue="LCRC"
            print "LCRC cluster is selected"
        elif self.fields.alcfButton.isSelected():
            self.queue="ALCF"
            print "ALCF cluster is selected"
        else:
            print "This queue option is not implemented yet"
            sys.exit()
    
        self.nnodes=self.fields.nnodeChooser.getSelectedIndex()+1
        if self.queue=="ALCF":
            if self.nnodes>8:
                self.nnodes=8
                self.fields.nnodeChooser.setSelectedIndex(7)
        else:
            if self.nnodes>4:
                self.nnodes=4
                self.fields.nnodeChooser.setSelectedIndex(3)            
    

    def writeParametersToFile(self):

        print("Write to local file")
        try:
            FILE = open(self.pfname,"w+")
            FILE.write("FileName                   " + self.FileLocation + '\n')
            FILE.write("Algorithm                  " + str(self.algorithm) +"\n")
            FILE.write("Energy                     " + str(self.energy) + "\n")
            FILE.write("PropagationDistance        " + str(self.propagationDistance) + "\n")
            FILE.write("PixelSize                  " + str(self.pixelSize) + "\n")
            FILE.write("Alpha                      " + str(self.alpha) + "\n")
            FILE.write("Filter                     " + str(self.filtersIndex) + "\n")
            FILE.write("Center                     " + str(self.center) + "\n")
            FILE.write("RemoveStripeMethod         " + str(self.stripeMethod) + "\n")
            FILE.write("Slice                      " + str(self.slice) + "\n")
            FILE.write("SearchWidth                " + str(self.centerSearchWidth) + "\n")
            FILE.write("nsino-per-chunk            " + str(self.nsinoperchunk) + "\n")

            FILE.write("Queue                      " + str(self.queue) +"\n")
            FILE.write("Nnodes                     " + str(self.nnodes) +"\n")
            FILE.write("\n")
            FILE.close()
        except IOError:
            pass
     
    def writeParametersToGUI(self):

        self.fields.selectedDatasetField.setText(str(self.FileLocation))
        self.fields.algoChooser.setSelectedIndex(int(self.algorithm))
        self.fields.energyField.setText(self.energy)
        self.fields.propagationDistanceField.setText(self.propagationDistance)
        self.fields.pixelSizeField.setText(self.pixelSize)
        self.fields.alphaField.setText(self.alpha)
        self.fields.filtersChooser.setSelectedIndex(self.filtersIndex)
        self.fields.centerField.setText(str(self.center))
        self.fields.stripeMethodChooser.setSelectedIndex(int(self.stripeMethod))
        self.fields.sliceField.setText(str(self.slice))
        self.fields.centerSearchField.setText(self.centerSearchWidth)
        self.fields.nsinochunkField.setText(self.nsinoperchunk)



