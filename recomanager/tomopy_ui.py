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

sys.path.append('/Users/decarlo/conda/recomanager-decarlof/recomanager')
#sys.path.append('/local/fast/conda/recomanager/recomanager')

import panel
import fields
import utils
import SinogramCalculation
import config

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
    flds.selectedDatasetField.setText(dataLocation)
    recoParameters.FileLocation = dataLocation

    from ch.psi.imagej.hdf5 import HDF5Reader
    reader = HDF5Reader()
    stack = reader.open("",False, dataLocation, "/exchange/data", True)

    if datasetFileName is None:
        print("User canceled the dialog!")
    else:

        logfileParameters.set()
        logfileParameters.dataset=datasetFileName
        logfileParameters.filepath = datasetGetDirectory
        
def reconstruct(event):
    global numberOfDigits
    
    print("I am reconstructing!")
    if event.getSource() == oneSliceButton:
        print("Preview one slice")
        recoParameters.algorithm = flds.algoChooser.getSelectedIndex()
        

        if recoParameters.algorithm==0:

            recoParameters.sliceNumber=flds.sliceField.getText()
            recoParameters.centerNumber=flds.centerField.getText()
            recoParameters.nsinoperchunk=flds.nsinochunkField.getText()
            recoParameters.centerSearchWidth=flds.searchWidthField.getText()
            recoParameters.gridrecPadding=flds.gridrecChooser.getSelectedIndex()
            recoParameters.stripeMethod=flds.stripeMethodChooser.getSelectedIndex()
            recoParameters.fwpad=flds.fwpadChooser.getSelectedIndex()

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
            reconfilelocation = flds.selectedDatasetField.getText()
            recoParameters.FileLocation = flds.selectedDatasetField.getText()
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

        recoParameters.sliceNumber=flds.sliceField.getText()
        recoParameters.centerNumber=flds.centerField.getText()
        recoParameters.nsinoperchunk=flds.nsinochunkField.getText()
        slicenum = float(recoParameters.sliceNumber)/float(920)
        reconfilelocation = flds.selectedDatasetField.getText()
        recoParameters.FileLocation = flds.selectedDatasetField.getText()
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
        recoParameters.sliceNumber=flds.sliceField.getText()
        recoParameters.centerNumber=flds.centerField.getText()
        recoParameters.nsinoperchunk=flds.nsinochunkField.getText()
        recoParameters.centerSearchWidth=flds.searchWidthField.getText()
        slicenum = float(recoParameters.sliceNumber)/float(920)
        reconfilelocation = flds.selectedDatasetField.getText()
        recoParameters.FileLocation = flds.selectedDatasetField.getText()
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

GUI = panel.Panel()
flds = fields.Fields(GUI)
recoParameters = config.RecoParameters(world, flds)
logfileParameters = config.Config()
sinogramCalculation = SinogramCalculation.SinogramCalculation(recoParameters,flds,logfileParameters)
originalRotationCenter = utils.OriginalRotationCenter(logfileParameters,recoParameters,flds)

contentPane.add(flds.recoSettingsPanel)
flds.recoSettingsPanel.add(flds.recoSettingsLabel)

# Algorithm selection
flds.recoSettingsPanel.add(flds.algoLabel)
flds.recoSettingsPanel.add(flds.algoChooser)

# Gridrec Padding
flds.recoSettingsPanel.add(flds.gridrecLabel)
flds.recoSettingsPanel.add(flds.gridrecChooser)

# Remove Stripe Method
flds.recoSettingsPanel.add(flds.stripeMethodLabel)
flds.recoSettingsPanel.add(flds.stripeMethodChooser)

# fw-pad
flds.recoSettingsPanel.add(flds.fwpadLabel)
flds.recoSettingsPanel.add(flds.fwpadChooser)

#flds.getLastParametersButton.action = getLastParameters
flds.recoSettingsPanel.add(flds.getLastParametersButton)

# Branch selection
flds.recoSettingsPanel.add(flds.branchLabel)
flds.recoSettingsPanel.add(flds.masterButton)
flds.recoSettingsPanel.add(flds.develButton)
branchGroup = ButtonGroup()
branchGroup.add(flds.masterButton)
branchGroup.add(flds.develButton)

# Queue selection
flds.recoSettingsPanel.add(flds.queueLabel)

#logfileParameters.scanType = "Standard"
flds.recoSettingsPanel.add(flds.NBButton)
flds.recoSettingsPanel.add(flds.wholeButton)
flds.recoSettingsPanel.add(flds.oldButton)
queueGroup = ButtonGroup()
queueGroup.add(flds.NBButton)
queueGroup.add(flds.oldButton)
queueGroup.add(flds.wholeButton)
if world == "online":
    flds.NBButton.setSelected(True)
else:
    flds.oldButton.setSelected(True)

# Number of nodes
flds.recoSettingsPanel.add(flds.nnodeLabel)
flds.recoSettingsPanel.add(flds.nnodeChooser)
    
# Rotation center
flds.recoSettingsPanel.add(flds.centerLabel)
flds.recoSettingsPanel.add(flds.centerField)
flds.getRotationCenterButton.actionPerformed=originalRotationCenter.getOriginalRotationCenter
flds.recoSettingsPanel.add(flds.getRotationCenterButton)

# Slice number
flds.recoSettingsPanel.add(flds.sliceLabel)
flds.recoSettingsPanel.add(flds.sliceField)

# Center Search Width
flds.recoSettingsPanel.add(flds.searchWidthLabel)
flds.recoSettingsPanel.add(flds.searchWidthField)

# nsinoPerChunk
flds.recoSettingsPanel.add(flds.nsinochunkLabel)
flds.recoSettingsPanel.add(flds.nsinochunkField)

# One slice reconstruction
oneSliceButton = GUI.createButton("Preview one slice",10,225,200,40,12,True)
oneSliceButton.actionPerformed=reconstruct
flds.recoSettingsPanel.add(oneSliceButton)

# Try Reconstruction
tryButton = GUI.createButton("Try Reconstruction",10,325,200,40,12,True)
tryButton.actionPerformed=reconstruct
flds.recoSettingsPanel.add(tryButton)

# Submit to the cluster
submitButton = GUI.createButton("Submit full stack",10,425,200,40,12,True)
submitButton.actionPerformed=reconstruct
flds.recoSettingsPanel.add(submitButton)

# Create a panel for choosing a dataset
contentPane.add(flds.chooseDatasetPanel)
flds.chooseDatasetPanel.add(flds.datasetSelectionLabel)

# Expert box
flds.chooseDatasetPanel.add(flds.expertBox)

flds.datasetSelectionButton.actionPerformed = datasetSelector
flds.chooseDatasetPanel.add(flds.datasetSelectionButton)
flds.chooseDatasetPanel.add(flds.selectedDatasetField)

# Change selected projection
projectionSelectionLabel = GUI.createLabel("Projection",10,105,200,30,2,12,True)
flds.chooseDatasetPanel.add(projectionSelectionLabel)

# Sinogram generation (sinooff_tomcat_j.py)
flds.chooseDatasetPanel.add(flds.sinogramCalculationLabel)
flds.chooseDatasetPanel.add(flds.sinogramCalculationButton)
flds.sinogramCalculationButton.actionPerformed = sinogramCalculation.absorptionSinogram

frame.setSize(810,830)      
frame.setVisible(1)

# Actions

getLastParametersHandler = utils.GetLastParameters(recoParameters)
flds.getLastParametersButton.actionListener = getLastParametersHandler

cutOffFrequencyHandler = utils.CutOffFrequency(flds.filterChooser,flds.cutOffLabel,flds.cutOffField)
flds.filterChooser.actionListener=cutOffFrequencyHandler

algorithmParametersHandler = utils.AlgorithmParameters(flds.algoChooser,flds.filterChooser)
flds.algoChooser.actionListener = algorithmParametersHandler

zingerHandler = utils.ZingerParameters(flds.zingerBox,flds.zingerThresholdLabel,flds.zingerThresholdField,flds.zingerKernelWidthLabel,flds.zingerKernelWidthField)
flds.zingerBox.actionListener=zingerHandler

ringRemovalHandler = utils.RingParameters(flds)
flds.ringChooser.actionListener=ringRemovalHandler

outputChooserHandler = utils.LevelParameters(flds.outputChooser,flds.minLabel,flds.minField,flds.maxLabel,flds.maxField,flds.getBothButton,flds.applyBothButton)
flds.outputChooser.actionListener=outputChooserHandler

expertSelectionHandler = utils.ExpertSelection(world,flds)
flds.expertBox.itemListener=expertSelectionHandler

approachSelectionHandler = utils.ApproachSelection(flds)
flds.approachBox.actionListener=approachSelectionHandler

cleanButtonHandler = utils.CleanButton(logfileParameters)
flds.cleanButton.actionListener=cleanButtonHandler

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