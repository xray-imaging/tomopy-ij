import os
import sys
from ij import IJ
from os.path import expanduser


home = expanduser("~")
CONFIG_FILE_NAME = os.path.join(home, "tomopy_ui.txt")


class DatasetParameters:

    def __init__(self, fields):

        self.fields = fields
        self.set()

    def set(self):

        self.fname = ""
        self.energy = ""
        self.propagation_distance = ""
        self.pixel_size = ""
        self.height = "2048"
        self.width = "0"
        self.scanType = "Standard"
        self.center = "0"
        self.originalRoiX = "0"

class RecoParameters:

    def __init__(self, fields):

        self.fields = fields
        self.set()

    def set(self):  

        self.pfname = CONFIG_FILE_NAME
        self.fname = ""
        self.algorithm = 0
        self.filterIndex = 0
        self.stripeMethod = 0
        self.center = 0
        self.slice = 0
        self.nsino_x_chunk = 16
        self.centerSearchWidth = 5
        self.energy = 0
        self.propagationDistance = 60
        self.pixel_size = 1
        self.alpha = 0.2
        self.queue = 'local'
        self.nnodes = 4

    def readParametersFromFile(self):
        
        print("Read parameters from ", self.pfname)
        FILE = open(self.pfname,"r")
        for line in FILE:
            linelist = line.split()
            if len(linelist)>0:
                if linelist[0] == "FileName":
                    self.fname = linelist[1]
                elif linelist[0] == "Algorithm":
                    self.algorithm = linelist[1]
                elif linelist[0] == "Filter":
                    self.filterIndex = int(linelist[1])            
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
                elif linelist[0] == "pixel_size":
                    self.pixel_size = linelist[1]
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
        self.pixel_size = self.fields.pixel_sizeField.getText()
        self.alpha = self.fields.alphaField.getText()
        self.filterIndex = self.fields.filterChooser.getSelectedIndex()
        self.filterUsed = self.fields.filterList[self.filterIndex]
        if self.filterIndex == 0:
            self.filterOption = "none"
        elif self.filterIndex == 1:
            self.filterOption = "shepp"
        elif self.filterIndex == 2:
            self.filterOption = "hann"
        elif self.filterIndex == 3:
            self.filterOption = "hammimg"
        elif self.filterIndex == 4:
            self.filterOption = "ramlak"
        elif self.filterIndex == 5:
            self.filterOption = "parzen"
        elif self.filterIndex == 6:
            self.filterOption = "cosine"
        elif self.filterIndex == 7:
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
    
        self.nnodes = self.fields.nnodeChooser.getSelectedIndex()+1
        if self.queue=="ALCF":
            if self.nnodes>8:
                self.nnodes = 8
                self.fields.nnodeChooser.setSelectedIndex(7)
        else:
            if self.nnodes>4:
                self.nnodes = 4
                self.fields.nnodeChooser.setSelectedIndex(3)            
    
    def writeParametersToFile(self, section='recon'):

        print("Write to local file")
        try:
            FILE = open(self.pfname,"w+")
            if section == 'recon':
                FILE.write("FileName                   " + self.fname + '\n')
                FILE.write("Algorithm                  " + str(self.algorithm) +"\n")
                FILE.write("Filter                     " + str(self.filterIndex) + "\n")
                FILE.write("RemoveStripeMethod         " + str(self.stripeMethod) + "\n")
                FILE.write("Center                     " + str(self.center) + "\n")
                FILE.write("Slice                      " + str(self.slice) + "\n")
                FILE.write("nsino_x_chunk              " + str(self.nsino_x_chunk) + "\n")
                FILE.write("SearchWidth                " + str(self.centerSearchWidth) + "\n")
                FILE.write("Energy                     " + str(self.energy) + "\n")
                FILE.write("PropagationDistance        " + str(self.propagationDistance) + "\n")
                FILE.write("pixel_size                 " + str(self.pixel_size) + "\n")
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
        self.fields.pixel_sizeField.setText(str(self.pixel_size))
        self.fields.alphaField.setText(self.alpha)
        self.fields.filterChooser.setSelectedIndex(self.filterIndex)
        self.fields.centerField.setText(str(self.center))
        self.fields.stripeMethodChooser.setSelectedIndex(int(self.stripeMethod))
        self.fields.sliceField.setText(str(self.slice))
        self.fields.centerSearchField.setText(self.centerSearchWidth)
        self.fields.nsino_x_chunkField.setText(self.nsino_x_chunk)
