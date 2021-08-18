import os
import glob
import sys
import shutil
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
from hdf.object import Dataset
import hdf 

global selectedDatasetField, flatFieldBox

sys.path.append('/Users/decarlo/conda/tomopy_ui/tomopy_ui')

import panel
import fields
import utils
import config

def createContentPane():

    panel = JPanel()
    panel.setLayout(None)
    panel.setOpaque(1)
    return panel

def read_hdf_meta(file_name, hdf_path):
    
    dataFile = H5File(file_name, H5File.READ)
    fp = dataFile.get(hdf_path)

    if fp is not None:
        return fp.getData()[0]
    else:
        return 0

def datasetSelector(event):

    datasetChooser = OpenDialog("Select a dataset")
    file_name = datasetChooser.getFileName()
    folder = datasetChooser.getDirectory()
    full_file_name = str(folder) + str(file_name)
    flds.selectedDatasetField.setText(full_file_name)
    reco_parameters.FileLocation = full_file_name

    from ch.psi.imagej.hdf5 import HDF5Reader
    reader = HDF5Reader()
    stack = reader.open("",False, full_file_name, "/exchange/data", True)

    if file_name is None:
        print("User canceled the dialog!")
    else:
        dataset_parameters.set()
        dataset_parameters.fname = full_file_name
        dataset_parameters.energy = read_hdf_meta(full_file_name, "/measurement/instrument/monochromator/energy")
        dataset_parameters.propagation_distance = read_hdf_meta(full_file_name, "/measurement/instrument/camera_motor_stack/setup/camera_distance")
        dataset_parameters.resolution = read_hdf_meta(full_file_name, "/measurement/instrument/detection_system/objective/resolution")
        dataset_parameters.height = stack.height
        dataset_parameters.width = stack.width
        flds.energyField.setText(str(dataset_parameters.energy))
        flds.propagationDistanceField.setText(str(dataset_parameters.propagation_distance))
        flds.resolutionField.setText(str(dataset_parameters.resolution))



def reconstruct(event):

    reco_parameters.readParametersFromGUI(dataset_parameters.originalRoiX)
    
    tomo_slice = flds.sliceField.getText()
    center = flds.centerField.getText()
    nsino_x_chunk = flds.nsino_x_chunkField.getText()
    center_search_width = flds.centerSearchField.getText()

    reco_parameters.algo = flds.algorithmChooser.getSelectedIndex()
    if reco_parameters.algo == 0:
        algostring = "gridrec"

    reco_parameters.stripeMethod = flds.stripeMethodChooser.getSelectedIndex()
    if reco_parameters.stripeMethod == 0:
        stripestring = "none"
    elif reco_parameters.stripeMethod == 1:
        stripestring = "fw"
    elif reco_parameters.stripeMethod == 2:
        stripestring = "ti"
    elif reco_parameters.stripeMethod == 3:
        stripestring = "sf"
    elif reco_parameters.stripeMethod == 4:
        stripestring = "vo-all"

    reco_parameters.filters = flds.filtersChooser.getSelectedIndex()
    if reco_parameters.filters == 0:
        filtersstring = "none"
    elif reco_parameters.filters == 1:
        filtersstring = "shepp"
    elif reco_parameters.filters == 2:
        filtersstring = "hann"
    elif reco_parameters.filters == 3:
        filtersstring = "hamming"
    elif reco_parameters.filters == 4:
        filtersstring = "ramlak"
    elif reco_parameters.filters == 5:
        filtersstring = "parzen"
    elif reco_parameters.filters == 6:
        filtersstring = "cosine"
    elif reco_parameters.filters == 7:
        filtersstring = "butterworth"

    if int(tomo_slice) < 0:
        tomo_slice = 1
    elif int(tomo_slice) > dataset_parameters.height:
        tomo_slice = dataset_parameters.height - 1

    nsino = float(tomo_slice)/float(dataset_parameters.height)

    full_file_name = flds.selectedDatasetField.getText()
    reco_parameters.FileLocation = flds.selectedDatasetField.getText()
    head_tail = os.path.split(full_file_name)
    rec_folder = os.path.normpath(head_tail[0]) + "_rec"

    print("Reconstructing")
    if event.getSource() == oneSliceButton:
        print("Preview one slice")

        command = "tomopy recon --file-name " + full_file_name + " --rotation-axis " + center + " --rotation-axis-auto manual " + "--reconstruction-algorithm " + algostring + " --gridrec-filter " + filtersstring + " --reconstruction-type slice " + "--nsino " + str(nsino) + " --gridrec-padding " + " --remove-stripe-method " + stripestring + " --fw-pad "
        print(command)
        os.system(command)

 
        list_of_files = glob.glob(os.path.join(rec_folder, "slice_rec", "*"))
        latest_file = max(list_of_files, key = os.path.getctime)
        imageResult = IJ.openImage(latest_file)
        imageResult.show()

    elif event.getSource() == tryButton:

        print("Try center")
        rec_file_name = head_tail[1].rstrip(".h5")
        try_folder = os.path.join(rec_folder, "try_center", rec_file_name)
        if os.path.isdir(try_folder) == True:
            shutil.rmtree(try_folder)

        command = "tomopy recon --file-name " + full_file_name + " --rotation-axis " + center + " --rotation-axis-auto manual " + "--reconstruction-algorithm " + algostring + " --gridrec-filter " + filtersstring + " --reconstruction-type try " + "--center-search-width " + str(center_search_width) + " --nsino " + str(nsino) + " --gridrec-padding " + " --remove-stripe-method " + stripestring + " --fw-pad "
        print(command)
        os.system(command)
        imp = FolderOpener.open(try_folder, "virtual")
        imp.show()

    elif event.getSource() == fullButton:

        print("Full")

        rec_folder = head_tail[1].rstrip(".h5") + "_rec"
        if os.path.isdir(rec_folder) == True:
            shutil.rmtree(rec_folder)

        command = "tomopy recon --file-name " + full_file_name + " --rotation-axis " + center + " --rotation-axis-auto manual " + "--reconstruction-algorithm " + algostring + " --gridrec-filter " + filtersstring + " --reconstruction-type full " + " --gridrec-padding " + " --nsino-per-chunk " + nsino_x_chunk
        print(command)
        os.system(command)
        
        imp = FolderOpener.open(rec_folder, "virtual")
        imp.show()

    reco_parameters.writeParametersToFile()


# To have the same look on all platforms
JFrame.setDefaultLookAndFeelDecorated(1)
frame = JFrame("Reconstruction User Interface")

contentPane = createContentPane()
frame.setContentPane(contentPane)

GUI = panel.Panel()
flds = fields.Fields(GUI)

dataset_parameters = config.DatasetParameters(flds)
reco_parameters = config.RecoParameters(flds)

# Create a panel for choosing a dataset
contentPane.add(flds.chooseDatasetPanel)
flds.chooseDatasetPanel.add(flds.datasetSelectionLabel)
flds.chooseDatasetPanel.add(flds.selectedDatasetField)

flds.chooseDatasetPanel.add(flds.datasetSelectionButton)
flds.datasetSelectionButton.actionPerformed = datasetSelector

# Expert box
flds.chooseDatasetPanel.add(flds.expertBox)

# Create a panel for reconstrution settings
contentPane.add(flds.recoSettingsPanel)
flds.recoSettingsPanel.add(flds.recoSettingsLabel)

# Create a panel for reconstrution settings
contentPane.add(flds.recoSettingsPanel)
flds.recoSettingsPanel.add(flds.recoSettingsLabel)

# Algorithm selection
flds.recoSettingsPanel.add(flds.algorithmLabel)
flds.recoSettingsPanel.add(flds.algorithmChooser)

# Paganin
flds.recoSettingsPanel.add(flds.energyLabel)
flds.recoSettingsPanel.add(flds.energyField)
flds.recoSettingsPanel.add(flds.energyUnitsLabel)
flds.recoSettingsPanel.add(flds.propagationDistanceLabel)
flds.recoSettingsPanel.add(flds.propagationDistanceField)
flds.recoSettingsPanel.add(flds.propagationDistanceUnitsLabel)
flds.recoSettingsPanel.add(flds.resolutionLabel)
flds.recoSettingsPanel.add(flds.resolutionField)
flds.recoSettingsPanel.add(flds.resolutionUnitsLabel)
flds.recoSettingsPanel.add(flds.alphaLabel)
flds.recoSettingsPanel.add(flds.alphaField)

# Paganin box
flds.recoSettingsPanel.add(flds.paganinBox)

# Filters
flds.recoSettingsPanel.add(flds.filtersLabel)
flds.recoSettingsPanel.add(flds.filtersChooser)

# Rotation center
flds.recoSettingsPanel.add(flds.centerLabel)
flds.recoSettingsPanel.add(flds.centerField)

# Remove Stripe Method
flds.recoSettingsPanel.add(flds.stripeMethodLabel)
flds.recoSettingsPanel.add(flds.stripeMethodChooser)

# Slice number
flds.recoSettingsPanel.add(flds.sliceLabel)
flds.recoSettingsPanel.add(flds.sliceField)

# Center Search Width
flds.recoSettingsPanel.add(flds.centerSearchLabel)
flds.recoSettingsPanel.add(flds.centerSearchField)
flds.recoSettingsPanel.add(flds.centerSearchUnitsLabel)

# nsino_x_chunk
flds.recoSettingsPanel.add(flds.nsinochunkLabel)
flds.recoSettingsPanel.add(flds.nsino_x_chunkField)

# Queue selection
flds.recoSettingsPanel.add(flds.queueLabel)
flds.recoSettingsPanel.add(flds.localButton)
flds.recoSettingsPanel.add(flds.alcfButton)
flds.recoSettingsPanel.add(flds.lcrcButton)
queueGroup = ButtonGroup()
queueGroup.add(flds.localButton)
queueGroup.add(flds.lcrcButton)
queueGroup.add(flds.alcfButton)

# Number of nodes
flds.recoSettingsPanel.add(flds.nnodeLabel)
flds.recoSettingsPanel.add(flds.nnodeChooser)

# One slice reconstruction
oneSliceButton = GUI.createButton("Preview one slice",10, 275, 200, 40, 12, True)
oneSliceButton.actionPerformed = reconstruct
flds.recoSettingsPanel.add(oneSliceButton)

# Try Reconstruction
tryButton = GUI.createButton("Try Reconstruction",10, 325, 200, 40, 12, True)
tryButton.actionPerformed = reconstruct
flds.recoSettingsPanel.add(tryButton)

# Submit to the cluster
fullButton = GUI.createButton("Full Reconstruction",10, 375, 200, 40, 12, True)
fullButton.actionPerformed = reconstruct
flds.recoSettingsPanel.add(fullButton)

frame.setSize(810, 830)      
frame.setVisible(1)

# Actions
algorithmParametersHandler = utils.AlgorithmParameters(flds.algorithmChooser, flds.filtersChooser)
flds.algorithmChooser.actionListener = algorithmParametersHandler

expertSelectionHandler = utils.ExpertSelection(flds)
flds.expertBox.itemListener = expertSelectionHandler

paganinSelectionHandler = utils.PaganinSelection(flds)
flds.paganinBox.itemListener = paganinSelectionHandler

if os.path.exists(reco_parameters.pfname):
    print("************************************************")
    print("************************************************")
    print("************************************************")
    print("************************************************")
    print("************************************************")
    print("Using previous parameter file")
    print("************************************************")
    print("************************************************")
    print("************************************************")
    print("************************************************")
    print("************************************************")
    print("************************************************")

else:
    print("Creating default parameter file %s", reco_parameters.pfname)       
    try:
        FILE = open(reco_parameters.pfname,"w+")
        FILE.write("FileName                   " + str(reco_parameters.fname) +"\n")
        FILE.write("Algorithm                  " + str(reco_parameters.algorithm) +"\n")
        FILE.write("Filter                     " + str(reco_parameters.filtersIndex) +"\n")
        FILE.write("RemoveStripeMethod         " + str(reco_parameters.stripeMethod) +"\n")
        FILE.write("Center                     " + str(reco_parameters.center) +"\n")
        FILE.write("Slice                      " + str(reco_parameters.slice) +"\n")
        FILE.write("nsino_x_chunk              " + str(reco_parameters.nsino_x_chunk) +"\n")
        FILE.write("SearchWidth                " + str(reco_parameters.centerSearchWidth) +"\n")
        FILE.write("Energy                     " + str(reco_parameters.energy) +"\n")
        FILE.write("PropagationDistance        " + str(reco_parameters.propagationDistance) +"\n")
        FILE.write("Resolution                 " + str(reco_parameters.resolution) +"\n")
        FILE.write("Alpha                      " + str(reco_parameters.alpha) +"\n")
        FILE.write("Queue                      " + str(reco_parameters.queue) +"\n")
        FILE.write("Nnodes                     " + str(reco_parameters.nnodes) +"\n")
        FILE.write("\n")
        FILE.close()
    except IOError:
        pass

reco_parameters.readParametersFromFile()
reco_parameters.writeParametersToGUI()