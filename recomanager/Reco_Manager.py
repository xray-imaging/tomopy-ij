import os, glob, time, socket, sys, math, shutil
from os.path import expanduser
from ij.gui import Line
from ij import IJ
from ij import ImagePlus
from ij.io import OpenDialog
from ij.plugin import ImageCalculator
from ij.plugin import FolderOpener
from java.awt.event import ActionListener, MouseAdapter
from javax.swing.event import ChangeEvent, ChangeListener
from javax.swing import JButton, JFrame, JPanel, JComboBox, JCheckBox, ButtonGroup, JOptionPane
from script.imglib import ImgLib
from java.awt import event, Font
from ch.psi.imagej.hdf5 import HDF5Reader, HDF5Utilities
from hdf.object.h5 import H5File

global selectedDatasetField, flatFieldBox, world

sys.path.append('C:/Users/benny/recomanager-ben/recomanager')
#sys.path.append('/local/fast/conda/recomanager/recomanager')

import RecoPanel
import RecoParameters
import Fields
import SimpleFunctions
import SinogramCalculation
import LogfileParameters

def createContentPane():

    panel = JPanel()
    panel.setLayout(None)
    panel.setOpaque(1)
    return panel

def datasetSelector(event):
    global img, projectionSelection, datasetAlreadySelected, flatFieldBox, basedir, datasetFileName
    global projectionNumberOfDigits

    datasetChooser = OpenDialog("Select a dataset")
    datasetFileName=datasetChooser.getFileName()
    datasetGetDirectory=datasetChooser.getDirectory()
    dataLocation = str(datasetGetDirectory) + str(datasetFileName)
    fields.selectedDatasetField.setText(dataLocation)
    recoParameters.FileLocation = dataLocation

    from ch.psi.imagej.hdf5 import HDF5Reader
    reader = HDF5Reader()
    stack = reader.open("",False, dataLocation, "/exchange/data", True)

    if datasetFileName is None:
        print("User canceled the dialog!")
    else:

        logfileParameters.setToDefaults()
        logfileParameters.dataset=datasetFileName
        logfileParameters.filepath = datasetGetDirectory
        
def reconstruct(event):
    global numberOfDigits
    
    print("I am reconstructing!")
    if event.getSource() == oneSliceButton:
        print("Preview one slice")
        recoParameters.algorithm = fields.algoChooser.getSelectedIndex()
        

        if recoParameters.algorithm==0:

            recoParameters.sliceNumber=fields.sliceField.getText()
            recoParameters.centerNumber=fields.centerField.getText()
            recoParameters.nsinoperchunk=fields.nsinochunkField.getText()
            recoParameters.centerSearchWidth=fields.searchWidthField.getText()
            recoParameters.gridrecPadding=fields.gridrecChooser.getSelectedIndex()
            recoParameters.stripeMethod=fields.stripeMethodChooser.getSelectedIndex()
            recoParameters.fwpad=fields.fwpadChooser.getSelectedIndex()

            if recoParameters.gridrecPadding == 0:
                tempstring = "True"
            elif recoParameters.gridrecPadding == 1:
                tempstring = "False"

            if recoParameters.stripeMethod == 0:
                stripestring = "none"
            elif recoParameters.stripeMethod == 1:
                stripestring = "fw"
            elif recoParameters.stripeMethod == 2:
                stripestring = "ti"
            elif recoParameters.stripeMethod == 3:
                stripestring = "sf"
            elif recoParameters.stripeMethod == 4:
                stripestring = "vo-all"

            if recoParameters.fwpad == 0:
                fwstring = "True"
            elif recoParameters.fwpad == 1:
                fwstring = "False"

            slicenum = float(recoParameters.sliceNumber)/float(920)
            reconfilelocation = fields.selectedDatasetField.getText()
            recoParameters.FileLocation = fields.selectedDatasetField.getText()
            head_tail = os.path.split(reconfilelocation)
            command = "tomopy recon --file-name " + reconfilelocation + " --rotation-axis " + recoParameters.centerNumber + " --rotation-axis-auto manual " + "--reconstruction-type slice " + "--nsino " + str(slicenum) + " --gridrec-padding " + tempstring + " --remove-stripe-method " + stripestring + " --fw-pad " + fwstring
            print(command)
            recoParameters.writeParametersToFile("GUIParameters.txt")
            os.system(command)
            tempfilepath = os.path.normpath(head_tail[0]) + "_rec"
            tempdataset = "recon_" + logfileParameters.dataset.rstrip(".h5") + ".tiff"

            list_of_files = glob.glob(os.path.join(tempfilepath, "slice_rec", "*"))
            latest_file = max(list_of_files, key=os.path.getctime)
            recon_filename = os.path.join(tempfilepath, "slice_rec", tempdataset)
            imageResult = IJ.openImage(latest_file)
            imageResult.show()

    elif event.getSource() == submitButton:

        recoParameters.readParametersFromGUI(logfileParameters.originalRoiX)
        print("Submit full stack")
        nprjForReconstruction = logfileParameters.nprj

        recoParameters.sliceNumber=fields.sliceField.getText()
        recoParameters.centerNumber=fields.centerField.getText()
        recoParameters.nsinoperchunk=fields.nsinochunkField.getText()
        slicenum = float(recoParameters.sliceNumber)/float(920)
        reconfilelocation = fields.selectedDatasetField.getText()
        recoParameters.FileLocation = fields.selectedDatasetField.getText()
        head_tail = os.path.split(reconfilelocation)
        command = "tomopy recon --file-name " + reconfilelocation + " --rotation-axis " + recoParameters.centerNumber + " --rotation-axis-auto manual " + "--reconstruction-type full " + "--nsino " + str(slicenum) + " --nsino-per-chunk " + recoParameters.nsinoperchunk
        print(command)
        recoParameters.writeParametersToFile("GUIParameters.txt")
        os.system(command)
        tempfilepath = os.path.normpath(head_tail[0]) + "_rec"
        tempdataset = head_tail[1].rstrip(".h5") + "_rec"
        
        fullstring = os.path.join(tempfilepath, tempdataset)
        tifffullstring = os.path.join(fullstring, "tiff_files")

        if os.path.isdir(tifffullstring) == True:
            shutil.rmtree(tifffullstring)

        os.mkdir(tifffullstring)

        for filename in os.listdir(fullstring):
            if filename.endswith(".tiff"):
                source = os.path.join(fullstring, filename)
                destination = os.path.join(tifffullstring, filename)
                shutil.move(source, destination)
            else:
                continue

        options = "virtual"
        imp = FolderOpener.open(tifffullstring, options)
        imp.show()

    elif event.getSource() == tryButton:

        print("Try Reconstruction")
        recoParameters.sliceNumber=fields.sliceField.getText()
        recoParameters.centerNumber=fields.centerField.getText()
        recoParameters.nsinoperchunk=fields.nsinochunkField.getText()
        recoParameters.centerSearchWidth=fields.searchWidthField.getText()
        slicenum = float(recoParameters.sliceNumber)/float(920)
        reconfilelocation = fields.selectedDatasetField.getText()
        recoParameters.FileLocation = fields.selectedDatasetField.getText()
        head_tail = os.path.split(reconfilelocation)
        command = "tomopy recon --file-name " + reconfilelocation + " --rotation-axis " + recoParameters.centerNumber + " --rotation-axis-auto manual " + "--reconstruction-type try " + "--nsino " + str(slicenum) + " --center-search-width " + recoParameters.centerSearchWidth
        print(command)
        recoParameters.writeParametersToFile("GUIParameters.txt")
        os.system(command)
        tempfilepath = os.path.normpath(head_tail[0]) + "_rec"
        tempdataset = head_tail[1].rstrip(".h5")

        trystring = os.path.join(tempfilepath, "try_center", tempdataset)
        tifftrystring = os.path.join(trystring, "tiff_files")

        if os.path.isdir(tifftrystring) == True:
            shutil.rmtree(tifftrystring)

        os.mkdir(tifftrystring)

        for filename in os.listdir(trystring):
            if filename.endswith(".tiff"):
                source = os.path.join(trystring, filename)
                destination = os.path.join(tifftrystring, filename)
                shutil.move(source, destination)
            else:
                continue

        options = "virtual"
        imp = FolderOpener.open(tifftrystring, options)
        imp.show()
    
# Set correct path
myHost=socket.gethostname()
a=myHost.split("-")

world = "online"

# To have the same look on all platforms
JFrame.setDefaultLookAndFeelDecorated(1)
frame = JFrame("Reconstruction User Interface")

contentPane = createContentPane()
frame.setContentPane(contentPane)

GUI = RecoPanel.RecoPanel()
fields = Fields.Fields(GUI)
recoParameters = RecoParameters.RecoParameters(world, fields)
logfileParameters = LogfileParameters.LogfileParameters()
sinogramCalculation = SinogramCalculation.SinogramCalculation(recoParameters,fields,logfileParameters)
originalRotationCenter = SimpleFunctions.OriginalRotationCenter(logfileParameters,recoParameters,fields)

contentPane.add(fields.recoSettingsPanel)
fields.recoSettingsPanel.add(fields.recoSettingsLabel)

# Algorithm selection
fields.recoSettingsPanel.add(fields.algoLabel)
fields.recoSettingsPanel.add(fields.algoChooser)

# Gridrec Padding
fields.recoSettingsPanel.add(fields.gridrecLabel)
fields.recoSettingsPanel.add(fields.gridrecChooser)

# Remove Stripe Method
fields.recoSettingsPanel.add(fields.stripeMethodLabel)
fields.recoSettingsPanel.add(fields.stripeMethodChooser)

# fw-pad
fields.recoSettingsPanel.add(fields.fwpadLabel)
fields.recoSettingsPanel.add(fields.fwpadChooser)

#fields.getLastParametersButton.actionPerformed = getLastParameters
fields.recoSettingsPanel.add(fields.getLastParametersButton)

# Branch selection
fields.recoSettingsPanel.add(fields.branchLabel)
fields.recoSettingsPanel.add(fields.masterButton)
fields.recoSettingsPanel.add(fields.develButton)
branchGroup = ButtonGroup()
branchGroup.add(fields.masterButton)
branchGroup.add(fields.develButton)

# Queue selection
fields.recoSettingsPanel.add(fields.queueLabel)

#logfileParameters.scanType = "Standard"
fields.recoSettingsPanel.add(fields.NBButton)
fields.recoSettingsPanel.add(fields.wholeButton)
fields.recoSettingsPanel.add(fields.oldButton)
queueGroup = ButtonGroup()
queueGroup.add(fields.NBButton)
queueGroup.add(fields.oldButton)
queueGroup.add(fields.wholeButton)
if world == "online":
    fields.NBButton.setSelected(True)
else:
    fields.oldButton.setSelected(True)

# Number of nodes
fields.recoSettingsPanel.add(fields.nnodeLabel)
fields.recoSettingsPanel.add(fields.nnodeChooser)
    
# Rotation center
fields.recoSettingsPanel.add(fields.centerLabel)
fields.recoSettingsPanel.add(fields.centerField)
fields.getRotationCenterButton.actionPerformed=originalRotationCenter.getOriginalRotationCenter
fields.recoSettingsPanel.add(fields.getRotationCenterButton)

# Slice number
fields.recoSettingsPanel.add(fields.sliceLabel)
fields.recoSettingsPanel.add(fields.sliceField)

# Center Search Width
fields.recoSettingsPanel.add(fields.searchWidthLabel)
fields.recoSettingsPanel.add(fields.searchWidthField)

# nsinoPerChunk
fields.recoSettingsPanel.add(fields.nsinochunkLabel)
fields.recoSettingsPanel.add(fields.nsinochunkField)

# One slice reconstruction
oneSliceButton = GUI.createButton("Preview one slice",10,225,200,40,12,True)
oneSliceButton.actionPerformed=reconstruct
fields.recoSettingsPanel.add(oneSliceButton)

# Try Reconstruction
tryButton = GUI.createButton("Try Reconstruction",10,325,200,40,12,True)
tryButton.actionPerformed=reconstruct
fields.recoSettingsPanel.add(tryButton)

# Submit to the cluster
submitButton = GUI.createButton("Submit full stack",10,425,200,40,12,True)
submitButton.actionPerformed=reconstruct
fields.recoSettingsPanel.add(submitButton)

# Create a panel for choosing a dataset
contentPane.add(fields.chooseDatasetPanel)
fields.chooseDatasetPanel.add(fields.datasetSelectionLabel)

# Expert box
fields.chooseDatasetPanel.add(fields.expertBox)

fields.datasetSelectionButton.actionPerformed = datasetSelector
fields.chooseDatasetPanel.add(fields.datasetSelectionButton)
fields.chooseDatasetPanel.add(fields.selectedDatasetField)

# Change selected projection
projectionSelectionLabel = GUI.createLabel("Projection",10,105,200,30,2,12,True)
fields.chooseDatasetPanel.add(projectionSelectionLabel)

# Sinogram generation (sinooff_tomcat_j.py)
fields.chooseDatasetPanel.add(fields.sinogramCalculationLabel)
fields.chooseDatasetPanel.add(fields.sinogramCalculationButton)
fields.sinogramCalculationButton.actionPerformed = sinogramCalculation.absorptionSinogram

frame.setSize(810,830)      
frame.setVisible(1)

# Actions

getLastParametersHandler = SimpleFunctions.GetLastParameters(recoParameters)
fields.getLastParametersButton.actionListener = getLastParametersHandler

cutOffFrequencyHandler = SimpleFunctions.CutOffFrequency(fields.filterChooser,fields.cutOffLabel,fields.cutOffField)
fields.filterChooser.actionListener=cutOffFrequencyHandler

algorithmParametersHandler = SimpleFunctions.AlgorithmParameters(fields.algoChooser,fields.filterChooser)
fields.algoChooser.actionListener = algorithmParametersHandler

zingerHandler = SimpleFunctions.ZingerParameters(fields.zingerBox,fields.zingerThresholdLabel,fields.zingerThresholdField,fields.zingerKernelWidthLabel,fields.zingerKernelWidthField)
fields.zingerBox.actionListener=zingerHandler

ringRemovalHandler = SimpleFunctions.RingParameters(fields)
fields.ringChooser.actionListener=ringRemovalHandler

outputChooserHandler = SimpleFunctions.LevelParameters(fields.outputChooser,fields.minLabel,fields.minField,fields.maxLabel,fields.maxField,fields.getBothButton,fields.applyBothButton)
fields.outputChooser.actionListener=outputChooserHandler

expertSelectionHandler = SimpleFunctions.ExpertSelection(world,fields)
fields.expertBox.itemListener=expertSelectionHandler

approachSelectionHandler = SimpleFunctions.ApproachSelection(fields)
fields.approachBox.actionListener=approachSelectionHandler

cleanButtonHandler = SimpleFunctions.CleanButton(logfileParameters)
fields.cleanButton.actionListener=cleanButtonHandler

home = expanduser("~")
if os.path.exists(os.path.join(home, "GUIParameters.txt")) == True:
    print("GUIParameters.txt")
elif os.path.exists(os.path.join(home, "GUIParameters.txt")) == False:
    home = expanduser("~")

    localFile = os.path.join(home, "GUIParameters.txt")

    print localFile
    print "Write to local file"
        
    try:
        FILE = open(localFile,"w+")
        FILE.write("Algorithm                  " + "0" +"\n")
        FILE.write("RemoveStripeMethod         " + "0" +"\n")
        FILE.write("fw-pad-setting             " + "0" +"\n")
        FILE.write("Rotation                   " + "0" + "\n")
        FILE.write("Center                     " + "1224" + "\n")
        FILE.write("Slice                      " + "460" + "\n")
        FILE.write("nsino-per-chunk            " + "256" + "\n")
        FILE.write("centerSearchWidth          " + "10" + "\n")
        FILE.write("\n")
        FILE.close()

    except IOError:
        pass

else:
    pass


recoParameters.readParametersFromFile("scratch")
recoParameters.writeParametersToGUI()