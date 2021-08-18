import os
import sys
from ij import IJ
from os.path import expanduser

class DatasetParameters:

    def __init__(self):

        self.set()

    def set(self):

        self.dataset = ""
        self.filepath = ""
        self.energy = ""
        self.propagation_distance = ""
        self.resolution = ""
        self.height = "100"
        self.width = "0"
        self.scanType = "Standard"
        self.center = "0"
        self.originalRoiX = "0"


class RecoParameters:

    def __init__(self, fields):

        self.fields = fields
        self.set()

    def set(self):  

        home = expanduser("~")
        self.pfname = os.path.join(home, "tomopy_ui.txt")
        self.fname = ""
        self.algorithm = 0
        self.filtersIndex = 0
        self.stripeMethod = 0
        self.center = 0
        self.slice = 0
        self.nsino_x_chunk = 16
        self.centerSearchWidth = 5
        self.energy = 0
        self.propagationDistance = 60
        self.resolution = 1
        self.alpha = 0.2
        self.queue = 'local'
        self.nnodes = 4

    def readParametersFromFile(self):
        
        print("Read parameters from ", self.pfname)
        FILE = open(self.pfname,"r")
        for line in FILE:
            linelist=line.split()
            if len(linelist)>0:
                if linelist[0] == "FileName":
                    self.fname = linelist[1]
                elif linelist[0] == "Algorithm":
                    self.algorithm = linelist[1]
                elif linelist[0] == "Filter":
                    self.filtersIndex=int(linelist[1])            
                elif linelist[0] == "RemoveStripeMethod":
                    self.stripeMethod = linelist[1]
                elif linelist[0] == "Center":
                    self.center = linelist[1]
                elif linelist[0] == "Slice":
                    self.slice = linelist[1]
                elif linelist[0] == "nsino_x_chunk":
                    self.nsino_x_chunk = linelist[1]
                elif linelist[0] == "SearchWidth":
                    self.centerSearchWidth = linelist[1]
                elif linelist[0] == "Energy":
                    self.energy = linelist[1]
                elif linelist[0] == "PropagationDistance":
                    self.propagationDistance = linelist[1]
                elif linelist[0] == "Resolution":
                    self.resolution = linelist[1]
                elif linelist[0] == "Alpha":
                    self.alpha = linelist[1]
                elif linelist[0] == "Queue":
                    self.queue = linelist[1]
                elif linelist[0] == "Nnodes":
                    self.nnodes = linelist[1]
        FILE.close()        
        

    def readParametersFromGUI(self,originalRoiX):
    
        self.fname = self.fields.selectedDatasetField.getText()
        self.algorithm = self.fields.algorithmChooser.getSelectedIndex()
        self.energy = self.fields.energyField.getText()
        self.propagationDistance = self.fields.propagationDistanceField.getText()
        self.resolution = self.fields.resolutionField.getText()
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
        self.nsino_x_chunk = self.fields.nsino_x_chunkField.getText()

        if self.fields.localButton.isSelected():
            self.queue="local"
            print("local cluster is selected")
        elif self.fields.lcrcButton.isSelected():
            self.queue="LCRC"
            print("LCRC cluster is selected")
        elif self.fields.alcfButton.isSelected():
            self.queue="ALCF"
            print("ALCF cluster is selected")
        else:
            print("This queue option is not implemented yet")
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
    

    def writeParametersToFile(self, section='recon'):

        print("Write to local file")
        try:
            FILE = open(self.pfname,"w+")
            if section == 'recon':
                FILE.write("FileName                   " + self.fname + '\n')
                FILE.write("Algorithm                  " + str(self.algorithm) +"\n")
                FILE.write("Filter                     " + str(self.filtersIndex) + "\n")
                FILE.write("RemoveStripeMethod         " + str(self.stripeMethod) + "\n")
                FILE.write("Center                     " + str(self.center) + "\n")
                FILE.write("Slice                      " + str(self.slice) + "\n")
                FILE.write("nsino_x_chunk              " + str(self.nsino_x_chunk) + "\n")
                FILE.write("SearchWidth                " + str(self.centerSearchWidth) + "\n")
                FILE.write("Energy                     " + str(self.energy) + "\n")
                FILE.write("PropagationDistance        " + str(self.propagationDistance) + "\n")
                FILE.write("Resolution                 " + str(self.resolution) + "\n")
                FILE.write("Alpha                      " + str(self.alpha) + "\n")
                FILE.write("Queue                      " + str(self.queue) +"\n")
                FILE.write("Nnodes                     " + str(self.nnodes) +"\n")
                FILE.write("\n")
                FILE.close()
            elif section == 'dataset':
                pass
        except IOError:
            pass
     
    def writeParametersToGUI(self):

        self.fields.selectedDatasetField.setText(self.fname)
        self.fields.algorithmChooser.setSelectedIndex(int(self.algorithm))
        self.fields.energyField.setText(self.energy)
        self.fields.propagationDistanceField.setText(self.propagationDistance)
        self.fields.resolutionField.setText(str(self.resolution))
        self.fields.alphaField.setText(self.alpha)
        self.fields.filtersChooser.setSelectedIndex(self.filtersIndex)
        self.fields.centerField.setText(str(self.center))
        self.fields.stripeMethodChooser.setSelectedIndex(int(self.stripeMethod))
        self.fields.sliceField.setText(str(self.slice))
        self.fields.centerSearchField.setText(self.centerSearchWidth)
        self.fields.nsino_x_chunkField.setText(self.nsino_x_chunk)
