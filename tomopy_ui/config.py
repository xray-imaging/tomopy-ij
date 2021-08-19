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
        self.fname = "Select_an_HDF_file"
        self.algorithm = 0
        self.filter_index = 0
        self.stripe_method = 0
        self.center = 0
        self.slice = 0
        self.nsino_x_chunk = 16
        self.center_search_width = 5
        self.energy = 0
        self.propagation_distance = 60
        self.pixel_size = 1
        self.alpha = 0.2
        self.queue = 'local'
        self.nnodes = 4

    def readParametersFromFile(self):

        FILE = open(self.pfname,"r")
        for line in FILE:
            linelist = line.split()
            if len(linelist)>0:
                if linelist[0] == "FileName":
                    self.fname = linelist[1]
                elif linelist[0] == "Algorithm":
                    self.algorithm = linelist[1]
                elif linelist[0] == "Filter":
                    self.filter_index = int(linelist[1])            
                elif linelist[0] == "RemoveStripeMethod":
                    self.stripe_method = linelist[1]
                elif linelist[0] == "Center":
                    self.center = linelist[1]
                elif linelist[0] == "Slice":
                    self.slice = linelist[1]
                elif linelist[0] == "NsinoPerChunk":
                    self.nsino_x_chunk = linelist[1]
                elif linelist[0] == "SearchWidth":
                    self.center_search_width = linelist[1]
                elif linelist[0] == "Energy":
                    self.energy = linelist[1]
                elif linelist[0] == "PropagationDistance":
                    self.propagation_distance = linelist[1]
                elif linelist[0] == "PixelSize":
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
        self.propagation_distance = self.fields.propagation_distanceField.getText()
        self.pixel_size = self.fields.pixel_sizeField.getText()
        self.alpha = self.fields.alphaField.getText()
        self.filter_index = self.fields.filterChooser.getSelectedIndex()
        self.filterUsed = self.fields.filterList[self.filter_index]
        if self.filter_index == 0:
            self.filterOption = "none"
        elif self.filter_index == 1:
            self.filterOption = "shepp"
        elif self.filter_index == 2:
            self.filterOption = "hann"
        elif self.filter_index == 3:
            self.filterOption = "hammimg"
        elif self.filter_index == 4:
            self.filterOption = "ramlak"
        elif self.filter_index == 5:
            self.filterOption = "parzen"
        elif self.filter_index == 6:
            self.filterOption = "cosine"
        elif self.filter_index == 7:
            self.filterOption = "butterworth"

        self.center = self.fields.centerField.getText()
        self.stripe_method = self.fields.stripe_methodChooser.getSelectedIndex()
        self.slice = self.fields.sliceField.getText()
        self.center_search_width = self.fields.centerSearchField.getText()
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
                FILE.write("Filter                     " + str(self.filter_index) + "\n")
                FILE.write("RemoveStripeMethod         " + str(self.stripe_method) + "\n")
                FILE.write("Center                     " + str(self.center) + "\n")
                FILE.write("Slice                      " + str(self.slice) + "\n")
                FILE.write("NsinoPerChunk              " + str(self.nsino_x_chunk) + "\n")
                FILE.write("SearchWidth                " + str(self.center_search_width) + "\n")
                FILE.write("Energy                     " + str(self.energy) + "\n")
                FILE.write("PropagationDistance        " + str(self.propagation_distance) + "\n")
                FILE.write("PixelSize                  " + str(self.pixel_size) + "\n")
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
        self.fields.propagation_distanceField.setText(self.propagation_distance)
        self.fields.pixel_sizeField.setText(str(self.pixel_size))
        self.fields.alphaField.setText(self.alpha)
        self.fields.filterChooser.setSelectedIndex(self.filter_index)
        self.fields.centerField.setText(str(self.center))
        self.fields.stripe_methodChooser.setSelectedIndex(int(self.stripe_method))
        self.fields.sliceField.setText(str(self.slice))
        self.fields.centerSearchField.setText(self.center_search_width)
        self.fields.nsino_x_chunkField.setText(str(self.nsino_x_chunk))
