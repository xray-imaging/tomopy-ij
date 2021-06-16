import os, glob, time, socket, sys, math
from ij.gui import Line
from ij import IJ
from ij import ImagePlus
from ij.io import DirectoryChooser
from ij.plugin import ImageCalculator
from java.awt.event import ActionListener, MouseAdapter
from javax.swing.event import ChangeEvent, ChangeListener
from javax.swing import JButton, JFrame, JPanel, JComboBox, JCheckBox, ButtonGroup, JOptionPane
from script.imglib import ImgLib
from java.awt import event, Font
from ch.psi.imagej.hdf5 import HDF5Reader, HDF5Utilities
from hdf.object.h5 import H5File

global selectedDatasetField, flatFieldBox, world

sys.path.append('/sls/X02DA/data/e11218/Data20/SCRIPTS/PYTHON/GUI/recomanager/RecoManager')
#sys.path.append('/das/work/p11/p11218/recomanager/RecoManager')
#sys.path.append('/sls/X02DA/applications/fiji/Fiji_Java8.app/plugins/TOMCAT')
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
    global img, projectionSelection, datasetAlreadySelected, flatFieldBox, basedir, datasetTmp
    global projectionNumberOfDigits

    datasetAlreadySelected = fields.selectedDatasetField.getText()
    if datasetAlreadySelected!="" and datasetTmp is not None:
        if logfileParameters.datasetValid == True:
            recoParameters.readParametersFromGUI(logfileParameters.originalRoiX)
            recoParameters.writeParametersToFile("local",logfileParameters.dataset,logfileParameters.datasetOut)
            recoParameters.writeParametersToFile("scratch")
        else:
            datasetAlreadySelected=""
    datasetChooser = DirectoryChooser("Select a dataset")
    datasetTmp=datasetChooser.getDirectory()

    if datasetTmp is None:
        print "User canceled the dialog!"
    else:

    	logfileParameters.setToDefaults()
        logfileParameters.dataset=datasetTmp

        datasetIsValid=False
        if os.path.isdir(logfileParameters.dataset):
            datasetIsValid=True
            os.chdir(logfileParameters.dataset)
            if logfileParameters.dataset[len(logfileParameters.dataset)-2]=="f" and logfileParameters.dataset[len(logfileParameters.dataset)-3]=="i" and logfileParameters.dataset[len(logfileParameters.dataset)-4]=="t" and logfileParameters.dataset[len(logfileParameters.dataset)-5]=="/":
                files = glob.glob("*.tif")
                if len(files)==0:
                    datasetIsValid=False
                os.chdir(os.pardir)
            elif os.path.isdir("tif"):
                files = glob.glob("tif/*.tif")
                if len(files)==0:
                    datasetIsValid=False                    
       	    else:
                files = glob.glob("*.h5")
                if len(files)==0:
                    datasetIsValid=False

        if datasetIsValid==True:        
            logfileParameters.dataset=os.path.realpath(os.getcwd())
            logfileParameters.datasetOut=logfileParameters.dataset
            print "Selected dataset " + logfileParameters.dataset
            os.chdir(os.pardir)
            basedir=os.getcwd()
            logfileParameters.logdir=basedir+"/log/"
            os.chdir(logfileParameters.dataset)		
            datasetList = logfileParameters.dataset.split("/")
            datasetListSize = len(datasetList)
            logfileParameters.diskName = datasetList[datasetListSize-2]
            logfileParameters.samplename = os.path.basename(logfileParameters.dataset)

            angleFile=False
            if os.path.isdir("tif"):
                logfileParameters.datasetType="tif"
                if os.path.isfile(logfileParameters.samplename + ".h5"):
                    angleFile=True
            elif os.path.isfile(logfileParameters.samplename + ".h5"):
                logfileParameters.datasetType="h5"
                dataFile = H5File(logfileParameters.dataset+"/"+logfileParameters.samplename+".h5", H5File.READ)
                dataFile.open()
                datasets = HDF5Utilities.getDatasets(dataFile)
                for i in range (0,datasets.size()):
	                if str(datasets.get(i))=="theta":
		                angleFile=True
            else:
                IJ.showMessage("The data formats other than \"tif\" or \"h5\" are not supported yet!")

            if logfileParameters.datasetType!="":
                if world=="offline":
                    linelist=logfileParameters.dataset.split("/")
                    if linelist[1]=="sls":
                        logfileParameters.beamlineStorage=1
                        dataName=linelist[3]
                        eaccount=linelist[4]
                        fullDiskName="/".join(linelist[5:len(linelist)-1])
                        paccount=eaccount.replace("e","p")
                        basedir="/das/work/"+paccount[0:3]+"/"+paccount+"/"+dataName+"/"+fullDiskName
                        logfileParameters.datasetOut=basedir+"/"+logfileParameters.samplename
                        print logfileParameters.datasetOut
                        if logfileParameters.datasetType=="tif":
                            fakeTifDir=logfileParameters.datasetOut+"/tif"
                            fakeLogfile=fakeTifDir+"/"+logfileParameters.samplename+".log"
                            if os.path.isdir(logfileParameters.datasetOut):
                                if os.path.isdir(fakeTifDir):
                                    if os.path.isfile(fakeLogfile):
                                        pass
                                    else:
                                        command="cp "+logfileParameters.dataset + "/tif/" + logfileParameters.samplename + ".log " + fakeTifDir
                                        os.system(command)
                                else:
                                    os.makedirs(logfileParameters.datasetOut+"/tif")
                                    command="cp "+logfileParameters.dataset + "/tif/" + logfileParameters.samplename + ".log " + fakeTifDir
                                    os.system(command)
                            else:
                                os.makedirs(logfileParameters.datasetOut+"/tif")
                                command="cp "+logfileParameters.dataset + "/tif/" + logfileParameters.samplename + ".log " + fakeTifDir
                                os.system(command)
                        else:
				            fakeLogfile=logfileParameters.datasetOut+"/"+logfileParameters.samplename+".log"
				            if os.path.isdir(logfileParameters.datasetOut):
						        if os.path.isfile(fakeLogfile):
							        pass
						        else:
							        command="cp "+logfileParameters.dataset + "/" + logfileParameters.samplename + ".log " + logfileParameters.datasetOut
							        os.system(command)
				            else:
					            os.makedirs(logfileParameters.datasetOut)
					            command="cp "+logfileParameters.dataset + "/" + logfileParameters.samplename + ".log " + logfileParameters.datasetOut
					            os.system(command)
							
                fields.selectedDatasetField.setText("/"+logfileParameters.diskName+"/"+logfileParameters.samplename)
                
                if logfileParameters.datasetType=="tif":
			        os.chdir("tif")
				
                if logfileParameters.beamlineStorage==1:
				    logfileParameters.logfile = fakeLogfile
                else:
                    if logfileParameters.datasetType=="tif":
                        logfileParameters.logfile = logfileParameters.dataset + "/tif/" + logfileParameters.samplename + ".log"
                    else:
                        logfileParameters.logfile = logfileParameters.dataset + "/" + logfileParameters.samplename + ".log"

                # Maybe these 2 lines can be removed but I am not sure yet.
                #recoParameters.overlapCenter="0"
                #recoParameters.realOverlap="0"

                logfileParameters.readLogfile()

                if logfileParameters.datasetValid==True:
                    projectionNumberOfDigits=4
                    projectionList = []

                    if logfileParameters.datasetType=="tif":
			            items = os.listdir(".")
			            for names in items:
				            if names.endswith(".tif"):
					            projectionList.append(names)
			            projectionList.sort()
                    else:
                        for i in range (1,int(logfileParameters.nprj)):
                            projectionList.append(logfileParameters.samplename + str(i).zfill(4))

                    recoParameters.setToDefaults()
                    recoParameters.writeParametersToGUI()

                    if angleFile==True:
                        fields.geometryBox.setSelectedIndex(3)

                    if float(logfileParameters.maxY)-float(logfileParameters.minY)==360:
				        recoParameters.threeSixtyVariable=1
				        fields.threeSixtyLabel.setVisible(True)
				        fields.approachLabel.setVisible(True)
				        fields.approachBox.setVisible(True)
				        fields.axisLabel.setVisible(True)
				        fields.axisBox.setVisible(True)
				        fields.cleanButton.setVisible(True)
				        if fields.approachBox.getSelectedIndex()==0:
				            fields.overlapLabel.setVisible(False)
				            fields.overlapField.setVisible(False)
				            #fields.zeroPaddingField.setText("1.5")
				        else:
				            fields.overlapLabel.setVisible(True)
				            fields.overlapField.setVisible(True)				        
				        recoParameters.overlapCenter=logfileParameters.center
				        logfileParameters.center=logfileParameters.stitchedCenter
				        fields.overlapField.setText(recoParameters.overlapCenter)
				        if logfileParameters.rotationAxisPosition=="Left":
					        fields.axisBox.setSelectedIndex(1)
					        if recoParameters.overlapCenter!="0":
						        recoParameters.realOverlap=str(2*float(recoParameters.overlapCenter))
				        elif logfileParameters.rotationAxisPosition=="Right":
					        fields.axisBox.setSelectedIndex(0)
					        if recoParameters.overlapCenter!="0":
						        recoParameters.realOverlap=str(2*(float(logfileParameters.originalRoiX)-float(recoParameters.overlapCenter)))
				        else:
					        IJ.showMessage("The rotation axis has not been positioned at the side of the field of view or this is not recorded in the log file!" )
				        fields.overlapField.setText(recoParameters.realOverlap)
				        if angleFile==False:
				            fields.geometryBox.setSelectedIndex(2)
				        fields.waveletPaddingBox.setSelectedIndex(2)
                    else:
                        fields.threeSixtyLabel.setVisible(False)
                        fields.axisLabel.setVisible(False)
                        fields.axisBox.setVisible(False)
                        fields.overlapLabel.setVisible(False)
                        fields.overlapField.setVisible(False)
                        fields.approachLabel.setVisible(False)
                        fields.approachBox.setVisible(False)
                        fields.cleanButton.setVisible(False)
				        
                    fields.centerField.setText(logfileParameters.center)

                    if os.path.isfile(logfileParameters.datasetOut+"/GUIParameters.txt") or os.path.isfile(logfileParameters.dataset+"/GUIParameters.txt"):
                        recoParameters.readParametersFromFile("local",logfileParameters.dataset,logfileParameters.datasetOut)
                        recoParameters.writeParametersToGUI()
			
                    if logfileParameters.datasetType == "tif":
                        filenumber=int(logfileParameters.ndrk)+int(logfileParameters.nflt)+1
                    else:
                        filenumber=1


                    fields.chooseDatasetPanel.remove(projectionSelection)
                    projectionSelection = JComboBox(projectionList, actionListener=projectionSelectionAction())
                    projectionSelection.setSelectedIndex(filenumber-1)
                    projectionSelection.setLocation(250,105)
                    projectionSelection.setSize(200,30)
                    fields.chooseDatasetPanel.add(projectionSelection)
                    fields.chooseDatasetPanel.validate()
                    fields.chooseDatasetPanel.repaint()

                    flatFieldBox.setVisible(True)
                    flatFieldBox.setSelected(False)

                    sinogramCalculation.checkAbsorptionSinogram()
                    sinogramCalculation.checkPhaseSinogram()
                    
                    if logfileParameters.scanType=="Standard":
                        fields.sinogramCalculationLabel.setVisible(True)
                        fields.sinogramCalculationButton.setVisible(True)
                        fields.paganinPaddingLabel.setVisible(True)
                        fields.paganinPaddingBox.setVisible(True)
                        fields.paganinDeconvolutionLabel.setVisible(True)
                        fields.paganinStabilizerLabel.setVisible(True)
                        fields.paganinStabilizerField.setVisible(True)
                        fields.paganinWidthLabel.setVisible(True)
                        fields.paganinWidthField.setVisible(True)
                        fields.paganinCalculationLabel.setVisible(True)
                        fields.deltaLabel.setVisible(True)
                        fields.deltaField.setVisible(True)
                        fields.betaLabel.setVisible(True)
                        fields.betaField.setVisible(True)
                        fields.distanceLabel.setVisible(True)
                        fields.distanceField.setVisible(True)
                        fields.paganinCalculationButton.setVisible(True)
                        fields.algoLabel.setVisible(True)
                        fields.algoChooser.setVisible(True)
                        fields.filterLabel.setVisible(True)
                        fields.filterChooser.setVisible(True)
           
            else:
			    IJ.showMessage("Choose a different dataset.\nThe raw projections do not exist for " + logfileParameters.dataset + "." )
        else:
			IJ.showMessage("Choose a different dataset.\nThe raw projections do not exist for " + logfileParameters.dataset + "." )

def getClosestSinogram(sliceNumber):
	global numberOfDigits
	print os.getcwd()
	recoParameters.algorithm = fields.algoChooser.getSelectedIndex()
	if os.path.isfile(logfileParameters.samplename + sliceNumber.zfill(numberOfDigits) + ".sin.DMP"):
		closestSinogram=str(sliceNumber)
	else:
		closestSinogram=0
		smallestDifference=999999999
		if numberOfDigits==1:
			pattern="?"
		elif numberOfDigits==2:
			pattern="??"
		elif numberOfDigits==3:
			pattern="???"
		elif numberOfDigits==4:
			pattern="????"
		filenames = glob.glob(logfileParameters.samplename + pattern +".sin.DMP")
		for fnames in filenames:
			fnameslist=fnames.split(".")
			sizefnameslist=len(fnameslist)
			element=fnameslist[sizefnameslist-3]
			elementLength=len(element)
			if numberOfDigits==1:
				fileNumber=int(element[elementLength-1])
			elif numberOfDigits==2:
				fileNumber=int(element[elementLength-2] + element[elementLength-1])
			elif numberOfDigits==3:
				fileNumber=int(element[elementLength-3] + element[elementLength-2] + element[elementLength-1])
			else:	
				fileNumber=int(element[elementLength-4] + element[elementLength-3] + element[elementLength-2] + element[elementLength-1])
			currentDifference=abs(int(sliceNumber)-fileNumber)
			if currentDifference < smallestDifference:
				smallestDifference=currentDifference
				closestSinogram=str(fileNumber)
		print "Closest sinogram " + str(closestSinogram)
	return str(closestSinogram)

def reconstructSinogram():

	global samplenameForReconstruction, numberOfDigits
	
	recoParameters.readParametersFromGUI(logfileParameters.originalRoiX)

	if recoParameters.zingerOption=="False":
		zingerLine=" "
	elif recoParameters.zingerOption=="True":
		zingerLine= "-z s"
	else:
		print "The zinger option " + recoParameters.zingerOption + " is not implemented"
		sys.exit()
			
	angleFileOption="-g " + str(recoParameters.geometryIndex) + " "
        if recoParameters.geometryIndex==0:
                IJ.showMessage("This option is not implemented yet")

	if recoParameters.geometryIndex==6:
		if recoParameters.algorithm==0:
			if os.path.isfile(sinogramCalculation.absSinogramLocation +"/sin/angles.txt"):
				angleFileOption="-g 0 -a " + sinogramCalculation.absSinogramLocation + "/sin"
			else:
				IJ.showMessage("Geometry Option: The angles.txt file is not in the sin folder\nProbably something went wrong during the sinogram calculation")
				recoParameters.algorithm=99
		elif recoParameters.algorithm==1:
			if os.path.isfile(sinogramCalculation.phaseSinogramLocation +"/sin_phase/angles.txt"):
				angleFileOption="-g 0 -a " + sinogramCalculation.phaseSinogramLocation + "/sin_phase"
			else:
				IJ.showMessage("Geometry Option: The angles.txt file is not in the sin_phase folder\nProbably something went wrong during the sinogram calculation")
				recoParameters.algorithm=99
        elif recoParameters.geometryIndex==0:
                recoParameters.algorithm=99

	samplenameForReconstruction = logfileParameters.samplename

	os.chdir(logfileParameters.datasetOut)
	if os.path.isdir("viewrec"):
		pass
	else:
		os.mkdir("viewrec")

	if recoParameters.algorithm==0:
		os.chdir(sinogramCalculation.absSinogramLocation + "/sin")
	elif recoParameters.algorithm==1:
		os.chdir(sinogramCalculation.phaseSinogramLocation + "/sin_phase")
	if os.path.isfile(logfileParameters.datasetOut + "/viewrec/x" + logfileParameters.samplename + recoParameters.sliceNumber.zfill(numberOfDigits) + ".sin.DMP"):
		os.system("rm " + logfileParameters.datasetOut + "/viewrec/x" + logfileParameters.samplename + recoParameters.sliceNumber.zfill(numberOfDigits) + ".sin.DMP")
	if os.path.isfile(logfileParameters.datasetOut + "/viewrec/xcropped" + logfileParameters.samplename + recoParameters.sliceNumber.zfill(numberOfDigits) + ".sin.DMP"):
		os.system("rm " + logfileParameters.datasetOut + "/viewrec/xcropped" + logfileParameters.samplename + recoParameters.sliceNumber.zfill(numberOfDigits) + ".sin.DMP")
	if os.path.isfile("cropped" + logfileParameters.samplename + recoParameters.sliceNumber.zfill(numberOfDigits) + ".sin.DMP"):
		os.system("rm " + "cropped" + logfileParameters.samplename + recoParameters.sliceNumber.zfill(numberOfDigits) + ".sin.DMP")

	threeSixtyOptionSlice = " "
	if recoParameters.threeSixtyVariable!=0:
		if recoParameters.approachBoxIndex==0:
			threeSixtyOptionSlice = " -L 1 "
			if recoParameters.axisBoxIndex==0:
				axisPos = "R"
				sinoSize = float(recoParameters.guiCenter)
			else:
				axisPos = "L"
				print projectionWidth
				print recoParameters.guiCenter
				sinoSize = float(projectionWidth) - float(recoParameters.guiCenter) - 1.0
			command = "/sls/X02DA/applications/tomcat-operation-scripts/reco_tools/sinogramCut.py " + logfileParameters.samplename + recoParameters.sliceNumber.zfill(numberOfDigits) + ".sin.DMP " + recoParameters.guiCenter + " " + axisPos
			print command
			os.system(command)
			samplenameForReconstruction = "cropped_" + logfileParameters.samplename
			print samplenameForReconstruction

			counter=0
			while os.path.isfile(samplenameForReconstruction + recoParameters.sliceNumber.zfill(numberOfDigits) + ".sin.DMP")==False and counter<10:
				print "Waiting ..."
				time.sleep(1)
				counter=counter+1
			if counter>=10:
				IJ.showMessage("Sinogram cropping has failed")
				recoParameters.algorithm=99

			if recoParameters.axisBoxIndex==1:
				if float(recoParameters.guiCenter) - math.floor(float(recoParameters.guiCenter))!=0.:
					recoParameters.guiCenter = str(float(recoParameters.guiCenter) - math.floor(float(recoParameters.guiCenter)))
				else:
					recoParameters.guiCenter = "0.001"
				print recoParameters.guiCenter

			### Automatic crop
			print sinoSize
			sinoPadSize = math.floor(sinoSize + sinoSize * 2 * float(recoParameters.zeroPadding))
			totalPadSize = 2**(math.floor(math.log(sinoPadSize,2))+1)
			print totalPadSize
			recoParameters.roiX1 = str(int(math.floor((totalPadSize - 2*sinoSize)/2) + int(recoParameters.roiX1)))
			recoParameters.roiY1 = str(int(math.floor((totalPadSize - 2*sinoSize)/2) + int(recoParameters.roiY1)))
			if recoParameters.roiX2=="0":
				recoParameters.roiX2 = str(int(math.floor((totalPadSize - 2*sinoSize)/2) + 2*sinoSize))
			else:
				recoParameters.roiX2 = str(int(math.floor((totalPadSize - 2*sinoSize)/2) + int(recoParameters.roiX2)))
			if recoParameters.roiY2=="0":
				recoParameters.roiY2 = str(int(math.floor((totalPadSize - 2*sinoSize)/2) + 2*sinoSize))
			else:
				recoParameters.roiY2 = str(int(math.floor((totalPadSize - 2*sinoSize)/2) + int(recoParameters.roiY2)))

	if recoParameters.ringOption != "0" and recoParameters.ringOption != "1":
		if recoParameters.ringOption == "3":
			command = "python /afs/psi/project/TOMCAT_pipeline/" + recoParameters.usedBranch + "/tomcat_pipeline/bin/Reconstruction/waveletFFT.pyc -t " + recoParameters.waveletType + " -d " + recoParameters.waveletMinComponent + ":" + recoParameters.waveletMaxComponent + " -f " + recoParameters.waveletFilterWidth + " -M " + recoParameters.waveletPadding + " -o " + logfileParameters.datasetOut + "/viewrec " + samplenameForReconstruction + recoParameters.sliceNumber.zfill(numberOfDigits) + ".sin.DMP"
			os.system(command)
		elif recoParameters.ringOption == "2":
			command = "python /afs/psi/project/TOMCAT_pipeline/" + recoParameters.usedBranch + "/tomcat_pipeline/bin/Reconstruction/sarepy.pyc -t s -s " + recoParameters.windowSize + " -o " + logfileParameters.datasetOut + "/viewrec " + samplenameForReconstruction + recoParameters.sliceNumber.zfill(numberOfDigits) + ".sin.DMP"
			os.system(command)
		elif recoParameters.ringOption == "4":
			command = "python /afs/psi/project/TOMCAT_pipeline/" + recoParameters.usedBranch + "/tomcat_pipeline/bin/Reconstruction/sarepy.pyc -t a -s " + recoParameters.windowSizeSM + " -l " + recoParameters.windowSizeL + " -n " + recoParameters.snr + " -o " + logfileParameters.datasetOut + "/viewrec " + samplenameForReconstruction + recoParameters.sliceNumber.zfill(numberOfDigits) + ".sin.DMP"
			os.system(command)
		
		samplenameForReconstruction = "x" + samplenameForReconstruction
		counter=0
		while os.path.isfile(logfileParameters.datasetOut + "/viewrec/" + samplenameForReconstruction + recoParameters.sliceNumber.zfill(numberOfDigits) + ".sin.DMP")==False and counter<10:
			print "Waiting ..."
			time.sleep(1)
			counter=counter+1
		if counter>=10:
			IJ.showMessage("Ring removal of the selected sinogram has failed")
			recoParameters.algorithm=99
		sinogramRingLocation = logfileParameters.datasetOut + "/viewrec"
			
	if os.path.isfile(logfileParameters.datasetOut + "/viewrec/" + samplenameForReconstruction + recoParameters.sliceNumber.zfill(numberOfDigits) + ".rec.DMP"):
		os.system("rm " + logfileParameters.datasetOut + "/viewrec/" + samplenameForReconstruction + recoParameters.sliceNumber.zfill(numberOfDigits) + ".rec.DMP")

	ringTextOption = " -i 0 "
	if recoParameters.algorithm==0:
		print "Absorption"
		if recoParameters.ringOption=="0" or recoParameters.ringOption=="1":
			sinogramRingLocation = sinogramCalculation.absSinogramLocation + "/sin"
		if recoParameters.ringOption=="1":
			ringTextOption = " -i 1 "
		command = "module load intel/19.5; /afs/psi/project/TOMCAT_pipeline/" + recoParameters.usedBranch + "/tomcat_pipeline/bin/Reconstruction/lib/gridRec -c " + recoParameters.guiCenter + " -f " + recoParameters.filterOption + " -Z " + recoParameters.zeroPadding + " -q " + recoParameters.cutOffFrequency + ringTextOption + angleFileOption + threeSixtyOptionSlice + " " + zingerLine + " -T " + recoParameters.threshold + " -k " + recoParameters.kernelWidth + " -t 0 -r " + recoParameters.rotation + " -R " + recoParameters.roiX1 + "," + recoParameters.roiY1 + "," + recoParameters.roiX2 + "," + recoParameters.roiY2 + " -D " + sinogramRingLocation + " -O " + logfileParameters.datasetOut + "/viewrec/ " + samplenameForReconstruction + recoParameters.sliceNumber.zfill(numberOfDigits) + ".sin.DMP"
	elif recoParameters.algorithm==1:
		print "Paganin"
		print recoParameters.roiX1
		print recoParameters.roiY2
		if recoParameters.ringOption=="0" or recoParameters.ringOption=="1":
			sinogramRingLocation = sinogramCalculation.phaseSinogramLocation + "/sin_phase"
		if recoParameters.ringOption=="1":
			ringTextOption = " -i 1 "
		command = "module load intel/19.5; /afs/psi/project/TOMCAT_pipeline/" + recoParameters.usedBranch + "/tomcat_pipeline/bin/Reconstruction/lib/gridRec -c " + recoParameters.guiCenter + " -f " + recoParameters.filterOption + " -Z " + recoParameters.zeroPadding + " -q " + recoParameters.cutOffFrequency + ringTextOption + angleFileOption + threeSixtyOptionSlice + " " + zingerLine + " -T " + recoParameters.threshold + " -k " + recoParameters.kernelWidth + " -t 0 -r " + recoParameters.rotation + " -R " + recoParameters.roiX1 + "," + recoParameters.roiY1 + "," + recoParameters.roiX2 + "," + recoParameters.roiY2 + " -D " + sinogramRingLocation + " -O " + logfileParameters.datasetOut + "/viewrec/ " + samplenameForReconstruction + recoParameters.sliceNumber.zfill(numberOfDigits) + ".sin.DMP"

	if recoParameters.algorithm!=99:
		print command
		os.system(command)

		counter=0
		while os.path.isfile(logfileParameters.datasetOut + "/viewrec/" + samplenameForReconstruction + recoParameters.sliceNumber.zfill(numberOfDigits) + ".rec.DMP")==False and counter<10:
			print "Waiting ..."
			time.sleep(1)
			counter=counter+1
		if counter>=10:
			IJ.showMessage("The reconstruction of the selected sinogram has failed")

def showReconstructedSlice(reconstructedSliceFilename):
	global reconstructedSlice
	if os.path.isfile(reconstructedSliceFilename):
		print reconstructedSliceFilename
		reconstructedSlice=IJ.openImage(reconstructedSliceFilename)
		reconstructedSlice.show()
		minLevel=fields.minField.getText()
		maxLevel=fields.maxField.getText()
		if minLevel!=0 and maxLevel!=0:
			print "applying both"
			reconstructedSlice.setDisplayRange(float(minLevel),float(maxLevel))
			reconstructedSlice.updateAndDraw()

		optimizeRecoSliceHandler = SimpleFunctions.OptimizeRecoSlice(reconstructedSlice,fields)
		fields.getBothButton.actionPerformed=optimizeRecoSliceHandler.GetBoth
		fields.applyBothButton.actionPerformed=optimizeRecoSliceHandler.ApplyBoth
		fields.setRoiButton.actionPerformed=optimizeRecoSliceHandler.SetRoi
		fields.doneRoiButton.actionPerformed=optimizeRecoSliceHandler.DoneRoi
		fields.resetRoiButton.actionPerformed=optimizeRecoSliceHandler.ResetRoi

		winReco=reconstructedSlice.getWindow()
		canvasReco = winReco.getCanvas()
		desiredMagnification = 0.30
		currentMagnification = canvasReco.getMagnification()
		canvasReco.setMagnification(desiredMagnification)
		canvasReco.setImageUpdated()
		winRecoHeight=int(winReco.getHeight()*desiredMagnification/currentMagnification)
		winRecoWidth=int(winReco.getWidth()*desiredMagnification/currentMagnification)
		if winReco==None:
			print "WIN NULL!"
		winReco.setLocationAndSize(810,350,winRecoWidth,winRecoHeight)
		winReco.toFront()
	else:
		pass
		
def reconstruct(event):
	global numberOfDigits
	
	print "I am reconstructing!"
	if event.getSource() == oneSliceButton:
		print "Preview one slice"
		recoParameters.algorithm = fields.algoChooser.getSelectedIndex()

		if recoParameters.algorithm==0:
			sinogramCalculation.checkAbsorptionSinogram()
			currentSinogramLocation=sinogramCalculation.absSinogramLocation
		else:
			sinogramCalculation.checkPhaseSinogram()
			currentSinogramLocation=sinogramCalculation.phaseSinogramLocation

		if sinogramCalculation.absSinogramFound==0 and recoParameters.algorithm==0:
			IJ.showMessage("The absorption sinograms for " + logfileParameters.samplename + " do not exist yet and need to be (or are currently being) computed." )
		elif sinogramCalculation.phaseSinogramFound==0 and recoParameters.algorithm==1:
			IJ.showMessage("The Paganin sinograms for " + logfileParameters.samplename + " do not exist yet and need to be (or are currently being) computed." )
		else:

			recoParameters.sliceNumber=fields.sliceField.getText()

			closestSinogram = getClosestSinogram(recoParameters.sliceNumber)
			recoParameters.sliceNumber=closestSinogram

			if closestSinogram!="0":
				
				fields.sliceField.setText(str(recoParameters.sliceNumber))
				reconstructSinogram()

				reconstructedSliceFile = logfileParameters.datasetOut + "/viewrec/" + samplenameForReconstruction + closestSinogram.zfill(numberOfDigits) + ".rec.DMP"

				if recoParameters.algorithm!=99:
					showReconstructedSlice(reconstructedSliceFile)
	        # TODO - I am not sure this is necessary, I need for sure the same command in sinogramCalculation (pag)	
				os.chdir(logfileParameters.datasetOut)

	elif event.getSource() == submitButton:

		recoParameters.readParametersFromGUI(logfileParameters.originalRoiX)
		print "Submit full stack"
		nprjForReconstruction = logfileParameters.nprj

		if recoParameters.algorithm==1:
			fltpPattern="####"
		
		threeSixtyOption="-d"
		if recoParameters.threeSixtyVariable==1:
			if recoParameters.approachBoxIndex==1:
				if recoParameters.algorithm==0:
					if recoParameters.axisBoxIndex==0:
						threeSixtyOption="-d -S R"
					else:
						threeSixtyOption="-d -S L"
		
				if recoParameters.algorithm==1:
					nprjForReconstruction=str((int(logfileParameters.nprj)+1)/2)
					if len(nprjForReconstruction)==3:
						fltpPattern="###"
					elif len(nprjForReconstruction)==2:
						fltpPattern="##"
					elif len(nprjForReconstruction)==1:
						fltpPattern="#"
			elif recoParameters.approachBoxIndex==0:
				if recoParameters.axisBoxIndex==0:
					threeSixtyOption="-d -LL -r 0," + str(int(float(projectionWidth) - float(recoParameters.guiCenter))) + ",0,0"
					sinoSize = float(recoParameters.guiCenter)
				elif recoParameters.axisBoxIndex==1:
					threeSixtyOption="-d -LL -r " + str(int(float(recoParameters.guiCenter)-1)) + ",0,0,0"
					sinoSize = float(projectionWidth) - float(recoParameters.guiCenter) - 1.0

				### Automatic crop
				sinoPadSize = math.floor(sinoSize + sinoSize * 2 * float(recoParameters.zeroPadding))
				totalPadSize = 2**(math.floor(math.log(sinoPadSize,2))+1)
				print totalPadSize
				recoParameters.roiX1 = str(int(math.floor((totalPadSize - 2*sinoSize)/2) + int(recoParameters.roiX1)))
				recoParameters.roiY1 = str(int(math.floor((totalPadSize - 2*sinoSize)/2) + int(recoParameters.roiY1)))
				if recoParameters.roiX2=="0":
					recoParameters.roiX2 = str(int(math.floor((totalPadSize - 2*sinoSize)/2) + 2*sinoSize))
				else:
					recoParameters.roiX2 = str(int(math.floor((totalPadSize - 2*sinoSize)/2) + int(recoParameters.roiX2)))
				if recoParameters.roiY2=="0":
					recoParameters.roiY2 = str(int(math.floor((totalPadSize - 2*sinoSize)/2) + 2*sinoSize))
				else:
					recoParameters.roiY2 = str(int(math.floor((totalPadSize - 2*sinoSize)/2) + int(recoParameters.roiY2)))

		if recoParameters.shifting=="True":
			shiftingOption="-q"
		elif recoParameters.shifting=="False":
			shiftingOption=""
		else:
			print "The shifting option " + recoParameters.shifting + " is not implemented"
			sys.exit()
			
		if logfileParameters.spOption=="True":
			sp="-sp"
		else:
			sp=""
        	
		if recoParameters.zingerOption=="False":
			zingerLine=""
		elif recoParameters.zingerOption=="True":
			zingerLine= "-z s -H " + recoParameters.threshold + " -w " + recoParameters.kernelWidth
		else:
			print "The zinger option " + recoParameters.zingerOption + " is not implemented"
			sys.exit()

		angleFileOption=" "
		if recoParameters.geometryIndex==6:
			if os.path.isfile(logfileParameters.dataset+"/"+logfileParameters.samplename+".h5"):
				angleFileOption=" --separateAngles " + logfileParameters.dataset+"/"+logfileParameters.samplename+".h5"
			else:
				print "With tif files, the HDF5 angle file needs to exist"
				
		if recoParameters.paganinPaddingIndex!="0":
			paganinPaddingOption = "-p " + str(recoParameters.paganinPaddingIndex)
		else:
			paganinPaddingOption = ""
		if recoParameters.stabilizer!="" and recoParameters.width !="":
			deconvolutionOption = "-s " + str(recoParameters.stabilizer) + " -g " + str(recoParameters.width)
		else:
			deconvolutionOption = ""

		if recoParameters.guiCenter=="0":
			centerOption=""
		else:
			if recoParameters.threeSixtyVariable==1 and recoParameters.algorithm==0 and recoParameters.approachBoxIndex==1:
				centerOption="-c " + recoParameters.overlapCenter + "," + recoParameters.guiCenter
			else:
				centerOption="-c " + recoParameters.guiCenter

		ringOptionText = ""
		if recoParameters.ringOption=="0" or recoParameters.ringOption=="3":
			ringOptionText = " -L 0 "
		elif recoParameters.ringOption=="1":
			ringOptionText = " -L 1 "
		elif recoParameters.ringOption=="2":
			ringOptionText = " -L 0 -sr " + recoParameters.windowSize
		elif recoParameters.ringOption=="4":
			ringOptionText = " -L 0 -sr " + recoParameters.snr + "," + recoParameters.windowSizeL + "," + recoParameters.windowSizeSM
		
		if recoParameters.outputFormat=="0":
			firstStringPart="rec_DMP_"
		elif recoParameters.outputFormat=="8":
			firstStringPart="rec_8bit_"
		elif recoParameters.outputFormat=="16":
			firstStringPart="rec_16bit_"
		else:
			IJ.showMessage("The selected output format has not been implemented yet!")

		if recoParameters.algorithm==0:
			secondStringPart=""
			fltpOnlyReconstruction=2
		elif recoParameters.algorithm==1:
			secondStringPart="Paganin_"
			if os.path.isdir(logfileParameters.datasetOut + "/fltp"):
				if os.listdir(logfileParameters.datasetOut + "/fltp")!=[]:
					fltpOnlyReconstruction=1
				else:
					os.rmdir(logfileParameters.datasetOut + "/fltp")
					fltpOnlyReconstruction=0
					if recoParameters.shifting=="True":
						shiftingOption="-Q"
					else:
						shiftingOption=""
					if recoParameters.zingerOption=="False":
						zingerLine=""
					else:
						zingerLine= "-z -H " + recoParameters.threshold + " -w " + recoParameters.kernelWidth
			else:
				fltpOnlyReconstruction=0
				if recoParameters.shifting=="True":
					shiftingOption="-Q"
				else:
					shiftingOption=""
				if recoParameters.zingerOption=="False":
					zingerLine=""
				else:
					zingerLine= "-z -H " + recoParameters.threshold + " -w " + recoParameters.kernelWidth
		else:
			IJ.showMessage("The selected algorithm has not been implemented yet!")

		selectedReconstructionDirectory=logfileParameters.datasetOut + "/" + firstStringPart + secondStringPart + recoParameters.postfix

		chosenResponseOption=JOptionPane.YES_OPTION
		if os.path.isdir(selectedReconstructionDirectory):
			chosenResponseOption = JOptionPane.showConfirmDialog(None, "The directory " + selectedReconstructionDirectory + " already exist and is going to be overwritten!\n\n                                                                           Do you want to continue?", "Existing reconstruction directory", JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE);

		if chosenResponseOption == JOptionPane.YES_OPTION:
		
			if recoParameters.outputFormat!="0" and recoParameters.minimum=="0" and recoParameters.maximum=="0":
				IJ.showMessage("The grey level limits have not been set!")

			elif (recoParameters.delta=="" or recoParameters.beta=="" or recoParameters.distance=="") and fltpOnlyReconstruction==0:
				IJ.showMessage("The parameters for the Paganin phase retrieval have not been set!")

			elif fltpOnlyReconstruction==0 and recoParameters.threeSixtyVariable==1:
				IJ.showMessage("For 360 degree scans, the fltp need to be first created!")

			else:

				if world=="offline":
					script = "/afs/psi/project/TOMCAT_pipeline/" + recoParameters.usedBranch + "/tomcat_pipeline/bin/prj2sinSLURM.sh --queue=hour "
				else:
					script = "/afs/psi/project/TOMCAT_pipeline/" + recoParameters.usedBranch + "/tomcat_pipeline/bin/prj2sinSLURM.sh --queue=" + recoParameters.queue + " --nnodes=" + str(recoParameters.nnodes)
			
				if recoParameters.algorithm==0:
					print "Absorption"
					if logfileParameters.datasetType=="tif":
						command = script + " --jobname=x" + logfileParameters.samplename + " --logdir=" + basedir + "/logs/ " + threeSixtyOption + " -k 0 -R " + recoParameters.postfix + " -Q " + logfileParameters.logfile + " " + centerOption + " -a " + recoParameters.rotation + " -G " + str(recoParameters.geometryIndex) + " " + angleFileOption + " -e " + recoParameters.roiX1 + "," + recoParameters.roiY1 + "," + recoParameters.roiX2 + "," + recoParameters.roiY2 + " -t " + recoParameters.outputFormat + " -n " + recoParameters.minimum + " -x " + recoParameters.maximum  + " -F " + recoParameters.filterOption + " -U " + recoParameters.cutOffFrequency + " -I 1 -Z " + recoParameters.zeroPadding + " -f " + nprjForReconstruction + "," + logfileParameters.ndrk + "," + logfileParameters.nflt + ",0,0 " + zingerLine + ringOptionText + " -y " + recoParameters.waveletType + " -V " + recoParameters.waveletMinComponent + ":" + recoParameters.waveletMaxComponent + " -E " + recoParameters.waveletFilterWidth + " -M " + recoParameters.waveletPadding + " " + shiftingOption + " " + sp + " -p " + logfileParameters.samplename + "####.tif -o " + logfileParameters.datasetOut + "/sin/ " + logfileParameters.dataset + "/tif/"			
					else:
						command = script + " --jobname=x" + logfileParameters.samplename + " --logdir=" + basedir + "/logs/ " + threeSixtyOption + " -k 0 -R " + recoParameters.postfix + " -Q " + logfileParameters.logfile + " " + centerOption + " -a " + recoParameters.rotation + " -G " + str(recoParameters.geometryIndex) + " " + angleFileOption + " -e " + recoParameters.roiX1 + "," + recoParameters.roiY1 + "," + recoParameters.roiX2 + "," + recoParameters.roiY2 + " -t " + recoParameters.outputFormat + " -n " + recoParameters.minimum + " -x " + recoParameters.maximum  + " -F " + recoParameters.filterOption + " -U " + recoParameters.cutOffFrequency + " -I 2 -Z " + recoParameters.zeroPadding + " -f " + nprjForReconstruction + "," + logfileParameters.ndrk + "," + logfileParameters.nflt + ",0,0 " + zingerLine + ringOptionText + " -y " + recoParameters.waveletType + " -V " + recoParameters.waveletMinComponent + ":" + recoParameters.waveletMaxComponent + " -E " + recoParameters.waveletFilterWidth + " -M " + recoParameters.waveletPadding + " " + shiftingOption + " " + sp + " -p " + logfileParameters.samplename + " -o " + logfileParameters.datasetOut + "/sin/ " + logfileParameters.dataset + "/" + logfileParameters.samplename + ".h5"		
				elif recoParameters.algorithm==1:
					print "Paganin"
					if fltpOnlyReconstruction==1:
						command = script + " --jobname=x" + logfileParameters.samplename + " --logdir=" + basedir + "/logs/ " + threeSixtyOption + " -k 0 -g 0 -R Paganin_" + recoParameters.postfix + " -Q " + logfileParameters.logfile + " " + centerOption + " -a " + recoParameters.rotation + " -G " + str(recoParameters.geometryIndex) + " " + angleFileOption + " -e " + recoParameters.roiX1 + "," + recoParameters.roiY1 + "," + recoParameters.roiX2 + "," + recoParameters.roiY2 + " -t " + recoParameters.outputFormat + " -n " + recoParameters.minimum + " -x " + recoParameters.maximum  + " -F " + recoParameters.filterOption + " -U " + recoParameters.cutOffFrequency + " -I 0 -Z " + recoParameters.zeroPadding + " -f " + nprjForReconstruction + ",0,0,0,0 " + zingerLine + ringOptionText + " -y " + recoParameters.waveletType + " -V " + recoParameters.waveletMinComponent + ":" + recoParameters.waveletMaxComponent + " -E " + recoParameters.waveletFilterWidth + " -M " + recoParameters.waveletPadding + " " + shiftingOption + " " + sp + " -p " + logfileParameters.samplename + fltpPattern + ".fltp.DMP -o " + logfileParameters.datasetOut + "/sin/ " + logfileParameters.datasetOut + "/fltp/"			
					else:
						if recoParameters.paganinPaddingIndex!="0":
							paganinPaddingOption = "-p " + str(recoParameters.paganinPaddingIndex)
						else:
							paganinPaddingOption = " "
						if recoParameters.stabilizer!="" and recoParameters.width !="":
							deconvolutionOption = "-s " + str(recoParameters.stabilizer) + " -g " + str(recoParameters.width)
						else:
							deconvolutionOption = ""
							
						if logfileParameters.datasetType=="tif":
							command = "/sls/X02DA/applications/tomcat-operation-scripts/reco_tools/recooff_paganin.py -b " + recoParameters.branch + " -q " + recoParameters.queue + " -N " + str(recoParameters.nnodes) + " -R " + recoParameters.postfix + " " + centerOption + " -a " + recoParameters.rotation + " -G " + str(recoParameters.geometryIndex) + " " + angleFileOption + " -r " + recoParameters.roiX1 + "," + recoParameters.roiY1 + "," + recoParameters.roiX2 + "," + recoParameters.roiY2 + " -t " + recoParameters.outputFormat + " -n " + recoParameters.minimum + " -x " + recoParameters.maximum + " -U " + recoParameters.cutOffFrequency + " -Z " + recoParameters.zeroPadding + ringOptionText + " -y " + recoParameters.waveletType + " -V " + recoParameters.waveletMinComponent + ":" + recoParameters.waveletMaxComponent + " -E " + recoParameters.waveletFilterWidth + " -M " + recoParameters.waveletPadding + " " + deconvolutionOption + " " + paganinPaddingOption + " " + shiftingOption + " " + zingerLine + " " + logfileParameters.dataset + "/tif " + recoParameters.delta + " " + recoParameters.beta + " " + recoParameters.distance
						else:
							command = "/sls/X02DA/applications/tomcat-operation-scripts/reco_tools/recooff_paganin.py -b " + recoParameters.branch + " -q " + recoParameters.queue + " -N " + str(recoParameters.nnodes) + " -R " + recoParameters.postfix + " " + centerOption + " -a " + recoParameters.rotation + " -G " + str(recoParameters.geometryIndex) + " " + angleFileOption + " -r " + recoParameters.roiX1 + "," + recoParameters.roiY1 + "," + recoParameters.roiX2 + "," + recoParameters.roiY2 + " -t " + recoParameters.outputFormat + " -n " + recoParameters.minimum + " -x " + recoParameters.maximum + " -U " + recoParameters.cutOffFrequency + " -Z " + recoParameters.zeroPadding + ringOptionText + " -y " + recoParameters.waveletType + " -V " + recoParameters.waveletMinComponent + ":" + recoParameters.waveletMaxComponent + " -E " + recoParameters.waveletFilterWidth + " -M " + recoParameters.waveletPadding + " " + deconvolutionOption + " " + paganinPaddingOption + " " + shiftingOption + " " + zingerLine + " " + logfileParameters.dataset + " " + recoParameters.delta + " " + recoParameters.beta + " " + recoParameters.distance						
				else:
					IJ.showMessage("This option has not been implemented yet!" )
					
				print command
				os.system(command)
		
				if os.path.isdir(basedir + "/log")==True:
					pass
				else:
					os.mkdir(basedir + "/log")
	
				FILELIST = open(basedir + "/log/command_list.txt","a")
				FILELIST.write(command + "\n")
				FILELIST.close()
				recoParameters.writeParametersToFile("local",logfileParameters.dataset,logfileParameters.datasetOut)
				recoParameters.writeParametersToFile("scratch")

class sliceSelection(MouseAdapter):
	def mousePressed(self,event):
		global numberOfDigits
		magnification = canvas.getMagnification()
		img.setRoi(Line(1,int(event.getY()/magnification),img.getWidth(), int(event.getY()/magnification)))
		fields.sliceField.setText(str(int(event.getY()/magnification)))
		recoParameters.algorithm = fields.algoChooser.getSelectedIndex()

		if recoParameters.algorithm==0:
			sinogramCalculation.checkAbsorptionSinogram()
		else:
			sinogramCalculation.checkPhaseSinogram()

		if sinogramCalculation.absSinogramFound==0 and recoParameters.algorithm==0:
			IJ.showMessage("The absorption sinograms for " + logfileParameters.samplename + " do not exist yet and need to be (or are currently being) computed." )
		elif sinogramCalculation.phaseSinogramFound==0 and recoParameters.algorithm==1:
			IJ.showMessage("The Paganin sinograms for " + logfileParameters.samplename + " do not exist yet and need to be (or are currently being) computed." )

		else:
			closestSinogram = getClosestSinogram(str(int(event.getY()/magnification)))
			print closestSinogram
			recoParameters.sliceNumber=closestSinogram
			if closestSinogram!="0":
				fields.sliceField.setText(str(recoParameters.sliceNumber))
				reconstructSinogram()
				reconstructedSliceFile = logfileParameters.datasetOut + "/viewrec/" + samplenameForReconstruction + recoParameters.sliceNumber.zfill(numberOfDigits) + ".rec.DMP"
				print reconstructedSliceFile
				if recoParameters.algorithm!=99:
					showReconstructedSlice(reconstructedSliceFile)
		
listener = sliceSelection()

class projectionSelectionAction(event.ActionListener):
    def actionPerformed(e,e1):
        global img, projectionSelection, datasetAlreadySelected
        global flatFieldBox, size
        global canvas
        global numberOfDigits, projectionNumberOfDigits, projectionWidth

        if datasetAlreadySelected != "":
			img.close()
        chosenSlice = projectionSelection.getSelectedIndex()
        if flatFieldBox.isSelected() == True:
			flatFieldBox.setSelected(False)
        else:
            if logfileParameters.datasetType=="tif":

			    projection = logfileParameters.dataset +  "/tif/" + logfileParameters.samplename + str(int(chosenSlice)+1).zfill(projectionNumberOfDigits) + ".tif"
			    img=IJ.openImage(projection)

            else:
			    reader = HDF5Reader()
			    stack = reader.open("",False, logfileParameters.dataset+"/"+logfileParameters.samplename+".h5", "/exchange/data", True, False)
			    projection = stack.getProcessor(int(chosenSlice+1))
			    img = ImagePlus(logfileParameters.samplename+str(int(chosenSlice)+1).zfill(projectionNumberOfDigits), projection)
            img.show()
            height=img.getHeight()
            projectionWidth=img.getWidth()
            if height<10:
				numberOfDigits=1
            elif height>=10 and height<100:
				numberOfDigits=2
            elif height>=100 and height<1000:
				numberOfDigits=3
            elif height>=1000 and height<10000:
				numberOfDigits=4
            else:
				print "This projection size is not supported"
				sys.exit()
            win=img.getWindow()
            canvas = win.getCanvas()
            canvas.addMouseListener(listener)
            desiredMagnification = 0.15
            currentMagnification = canvas.getMagnification()
            canvas.setMagnification(desiredMagnification)
            canvas.setImageUpdated()
            winHeight=int(win.getHeight()*desiredMagnification/currentMagnification)
            winWidth=int(win.getWidth()*desiredMagnification/currentMagnification)
            if win==None:
				print "WIN NULL!"
            win.setLocationAndSize(810,0,winWidth,winHeight)
            win.toFront()
        datasetAlreadySelected = fields.selectedDatasetField.getText()
		
class flatFieldSelection(event.ItemListener):
	def itemStateChanged(e,e1):
		global flatFieldBox, img
		img.close()
		if flatFieldBox.isSelected() == True:
			print "selected"
			chosenSlice = projectionSelection.getSelectedIndex()
			if logfileParameters.datasetType=="tif":
			    projection = logfileParameters.dataset +  "/tif/" + logfileParameters.samplename + str(int(chosenSlice)+1).zfill(4) + ".tif"
			    proj=IJ.openImage(projection)
			    darkProjection = logfileParameters.dataset +  "/tif/" + logfileParameters.samplename + str(1).zfill(4) + ".tif"
			    darkImg=IJ.openImage(darkProjection)
			    flatProjection = logfileParameters.dataset +  "/tif/" + logfileParameters.samplename + str(int(logfileParameters.ndrk)+1).zfill(4) + ".tif"
			    flatImg=IJ.openImage(flatProjection)
			else:
			    reader = HDF5Reader()
			    stack = reader.open("",False, logfileParameters.dataset+"/"+logfileParameters.samplename+".h5", "/exchange/data", True, False)
			    projection = stack.getProcessor(int(chosenSlice+1))
			    proj = ImagePlus(logfileParameters.samplename+str(int(chosenSlice)+1).zfill(projectionNumberOfDigits), projection)
			    stack = reader.open("",False, logfileParameters.dataset+"/"+logfileParameters.samplename+".h5", "/exchange/data_dark", True, False)
			    projection = stack.getProcessor(1)
			    darkImg = ImagePlus(logfileParameters.samplename+str(1).zfill(projectionNumberOfDigits), projection)
			    stack = reader.open("",False, logfileParameters.dataset+"/"+logfileParameters.samplename+".h5", "/exchange/data_white", True, False)
			    projection = stack.getProcessor(int(logfileParameters.ndrk)+1)
			    flatImg = ImagePlus(logfileParameters.samplename+str(int(logfileParameters.ndrk)+1).zfill(projectionNumberOfDigits), projection)			    
			num = ImageCalculator().run("subtract create 32-bit float", proj, darkImg)
			den = ImageCalculator().run("subtract create 32-bit float", flatImg, darkImg)
			num = ImageCalculator().run("subtract create 32-bit float", proj, darkImg)
			img = ImageCalculator().run("divide create 32-bit float", num, den)
			title = "Flat-field corrected " + logfileParameters.samplename + str(int(chosenSlice)+1).zfill(4) + ".tif"
			img.setTitle(title)			
			img.show()
			win=img.getWindow()
			canvas = win.getCanvas()
			canvas.addMouseListener(listener)
			desiredMagnification = 0.15
			currentMagnification = canvas.getMagnification()
			canvas.setMagnification(desiredMagnification)
			canvas.setImageUpdated()
			winHeight=int(win.getHeight()*desiredMagnification/currentMagnification)
			winWidth=int(win.getWidth()*desiredMagnification/currentMagnification)
			if win==None:
				print "WIN NULL!"
			win.setLocationAndSize(810,0,winWidth,winHeight)
			win.toFront()
		else:
			print "not selected"
			chosenSlice = projectionSelection.getSelectedIndex()
			if logfileParameters.datasetType=="tif":
			    projection = logfileParameters.dataset +  "/tif/" + logfileParameters.samplename + str(int(chosenSlice)+1).zfill(4) + ".tif"
			    img=IJ.openImage(projection)
			else:
			    reader = HDF5Reader()
			    stack = reader.open("",False, logfileParameters.dataset+"/"+logfileParameters.samplename+".h5", "/exchange/data", True, False)
			    projection = stack.getProcessor(int(chosenSlice+1))
			    img = ImagePlus(logfileParameters.samplename+str(int(chosenSlice)+1).zfill(projectionNumberOfDigits), projection)
			img.show()
			win=img.getWindow()
			canvas = win.getCanvas()
			canvas.addMouseListener(listener)
			desiredMagnification = 0.15
			currentMagnification = canvas.getMagnification()
			canvas.setMagnification(desiredMagnification)
			canvas.setImageUpdated()
			winHeight=int(win.getHeight()*desiredMagnification/currentMagnification)
			winWidth=int(win.getWidth()*desiredMagnification/currentMagnification)
			if win==None:
				print "WIN NULL!"
			win.setLocationAndSize(810,0,winWidth,winHeight)
			win.toFront()
	

# Set correct path
myHost=socket.gethostname()
a=myHost.split("-")
if a[0] == "ra":
	world = "offline"
elif a[0] == "x02da":
	world = "online"
else:
	print "Unknown environment " + a + "!"
	sys.exit()

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

# Filter selection
fields.recoSettingsPanel.add(fields.cutOffLabel)
fields.recoSettingsPanel.add(fields.cutOffField)
fields.recoSettingsPanel.add(fields.filterLabel)
fields.recoSettingsPanel.add(fields.filterChooser)

# Algorithm selection
fields.recoSettingsPanel.add(fields.algoLabel)
fields.recoSettingsPanel.add(fields.algoChooser)

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

# Rotation
fields.recoSettingsPanel.add(fields.rotLabel)
fields.recoSettingsPanel.add(fields.rotField)

# Zero padding
fields.recoSettingsPanel.add(fields.zeroPaddingLabel)
fields.recoSettingsPanel.add(fields.zeroPaddingField)

# Geometry
fields.recoSettingsPanel.add(fields.geometryLabel)
fields.recoSettingsPanel.add(fields.geometryBox)

# Zingers
fields.recoSettingsPanel.add(fields.zingerThresholdLabel)
fields.recoSettingsPanel.add(fields.zingerThresholdField)
fields.recoSettingsPanel.add(fields.zingerKernelWidthLabel)
fields.recoSettingsPanel.add(fields.zingerKernelWidthField)
fields.recoSettingsPanel.add(fields.zingerLabel)
fields.recoSettingsPanel.add(fields.zingerBox)

# Ring removal
fields.recoSettingsPanel.add(fields.wsLabel)
fields.recoSettingsPanel.add(fields.wsField)
fields.recoSettingsPanel.add(fields.wslLabel)
fields.recoSettingsPanel.add(fields.wslField)
fields.recoSettingsPanel.add(fields.wssmLabel)
fields.recoSettingsPanel.add(fields.wssmField)
fields.recoSettingsPanel.add(fields.snrLabel)
fields.recoSettingsPanel.add(fields.snrField)
fields.recoSettingsPanel.add(fields.sarepyRef)
fields.recoSettingsPanel.add(fields.waveletTypeLabel)
fields.recoSettingsPanel.add(fields.waveletTypeChooser)
fields.recoSettingsPanel.add(fields.waveletComponentMinLabel)
fields.recoSettingsPanel.add(fields.waveletComponentMinField)
fields.recoSettingsPanel.add(fields.waveletComponentMaxLabel)
fields.recoSettingsPanel.add(fields.waveletComponentMaxField)
fields.recoSettingsPanel.add(fields.waveletFilterWidthLabel)
fields.recoSettingsPanel.add(fields.waveletFilterWidthField)
fields.recoSettingsPanel.add(fields.waveletPaddingLabel)
fields.recoSettingsPanel.add(fields.waveletPaddingBox)
fields.recoSettingsPanel.add(fields.muenchRef)
fields.recoSettingsPanel.add(fields.ringLabel)
fields.recoSettingsPanel.add(fields.ringChooser)

# Output
fields.recoSettingsPanel.add(fields.minLabel)
fields.recoSettingsPanel.add(fields.minField)
fields.recoSettingsPanel.add(fields.maxLabel)
fields.recoSettingsPanel.add(fields.maxField)
fields.recoSettingsPanel.add(fields.getBothButton)
fields.recoSettingsPanel.add(fields.applyBothButton)
fields.recoSettingsPanel.add(fields.outputLabel)
fields.recoSettingsPanel.add(fields.outputChooser)

# ROI
fields.recoSettingsPanel.add(fields.roiLabel)
fields.recoSettingsPanel.add(fields.setRoiButton)
fields.recoSettingsPanel.add(fields.doneRoiButton)
fields.recoSettingsPanel.add(fields.x1Label)
fields.recoSettingsPanel.add(fields.x1Field)
fields.recoSettingsPanel.add(fields.y1Label)
fields.recoSettingsPanel.add(fields.y1Field)
fields.recoSettingsPanel.add(fields.x2Label)
fields.recoSettingsPanel.add(fields.x2Field)
fields.recoSettingsPanel.add(fields.y2Label)
fields.recoSettingsPanel.add(fields.y2Field)
fields.recoSettingsPanel.add(fields.resetRoiButton)

# Block
fields.recoSettingsPanel.add(fields.blockLabel)

#setBlockButton = JButton("Set", actionPerformed=setBlock)
#setBlockButton.setLocation(50,340)
#setBlockButton.setSize(50,20)
#setBlockButton.setFont(Font("Dialog",Font.BOLD,10))
#recoSettingsPanel.add(setBlockButton)

#doneBlockButton = JButton("Update", actionPerformed=doneBlock)
#doneBlockButton.setLocation(110,340)
#doneBlockButton.setSize(80,20)
#doneBlockButton.setFont(Font("Dialog",Font.BOLD,10))
#recoSettingsPanel.add(doneBlockButton)

# Shifting
fields.recoSettingsPanel.add(fields.shiftingLabel)
fields.recoSettingsPanel.add(fields.shiftingBox)

# Postfix
fields.recoSettingsPanel.add(fields.postfixLabel)
fields.recoSettingsPanel.add(fields.postfixField)

# One slice reconstruction
oneSliceButton = GUI.createButton("Preview one slice",10,495,200,40,12,True)
oneSliceButton.actionPerformed=reconstruct
fields.recoSettingsPanel.add(oneSliceButton)

# Submit to the cluster
submitButton = GUI.createButton("Submit full stack",580,495,200,40,12,True)
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

# 360 degree scans
fields.chooseDatasetPanel.add(fields.threeSixtyLabel)
fields.chooseDatasetPanel.add(fields.axisLabel)
fields.chooseDatasetPanel.add(fields.axisBox)
fields.chooseDatasetPanel.add(fields.overlapLabel)
fields.chooseDatasetPanel.add(fields.overlapField)
fields.chooseDatasetPanel.add(fields.approachLabel)
fields.chooseDatasetPanel.add(fields.approachBox)
fields.chooseDatasetPanel.add(fields.cleanButton)

# Change selected projection
projectionSelectionLabel = GUI.createLabel("Projection",10,105,200,30,2,12,True)
fields.chooseDatasetPanel.add(projectionSelectionLabel)

projectionList = []
datasetAlreadySelected = ""
projectionSelection = JComboBox(projectionList, actionListener=projectionSelectionAction())
projectionSelection.setLocation(250,105)
projectionSelection.setSize(200,30)
fields.chooseDatasetPanel.add(projectionSelection)

flatFieldBox = JCheckBox("Flat-field correction", itemListener=flatFieldSelection())
flatFieldBox.setLocation(480,105)
flatFieldBox.setSize(160,30)
flatFieldBox.setVisible(False)
fields.chooseDatasetPanel.add(flatFieldBox)

# Sinogram generation (sinooff_tomcat_j.py)
fields.chooseDatasetPanel.add(fields.sinogramCalculationLabel)
fields.chooseDatasetPanel.add(fields.sinogramCalculationButton)
fields.sinogramCalculationButton.actionPerformed = sinogramCalculation.absorptionSinogram

# Sinogram Paganin generation (sinooff_tomcat_Paganin.py)
fields.chooseDatasetPanel.add(fields.paganinCalculationLabel)
fields.chooseDatasetPanel.add(fields.deltaLabel)
fields.chooseDatasetPanel.add(fields.deltaField)
fields.chooseDatasetPanel.add(fields.betaLabel)
fields.chooseDatasetPanel.add(fields.betaField)
fields.chooseDatasetPanel.add(fields.distanceLabel)
fields.chooseDatasetPanel.add(fields.distanceField)
fields.chooseDatasetPanel.add(fields.paganinCalculationButton)
fields.paganinCalculationButton.actionPerformed = sinogramCalculation.paganinSinogram
fields.chooseDatasetPanel.add(fields.paganinPaddingLabel)
fields.chooseDatasetPanel.add(fields.paganinPaddingBox)
fields.chooseDatasetPanel.add(fields.paganinDeconvolutionLabel)
fields.chooseDatasetPanel.add(fields.paganinStabilizerLabel)
fields.chooseDatasetPanel.add(fields.paganinStabilizerField)
fields.chooseDatasetPanel.add(fields.paganinWidthLabel)
fields.chooseDatasetPanel.add(fields.paganinWidthField)

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
