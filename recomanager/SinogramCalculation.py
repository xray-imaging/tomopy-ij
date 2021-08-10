import os, sys, glob
from javax.swing import JOptionPane

class SinogramCalculation():

    def __init__ (self,recoParameters,fields,logfileParameters):

        self.recoParameters = recoParameters
        self.fields = fields
        self.logfileParameters = logfileParameters
        
        self.setToDefaults()
        
    def setToDefaults(self):
    
        self.absSinogramFound=0
        self.phaseSinogramFound=0
        self.absSinogramLocation=""
        self.phaseSinogramLocation=""
        
    def absorptionSinogram(self,event):

        self.recoParameters.readParametersFromGUI(self.logfileParameters.originalRoiX)
        if self.recoParameters.threeSixtyVariable!=0:
            if self.recoParameters.approachBoxIndex==0:
                overlapOption = " -t "
            else:
                if self.recoParameters.overlapCenter !="0":
                    overlapOption = " -c " + self.recoParameters.overlapCenter
                    self.fields.centerField.setText(self.recoParameters.guiGuessCenter)
                else:
                    overlapOption = ""
        else:
            overlapOption = ""
	
        angleFileOption=" "
        if self.recoParameters.geometryIndex==6:
            if os.path.isfile(self.logfileParameters.dataset+"/"+self.logfileParameters.samplename+".h5"):
                angleFileOption=" -G --separateAngles " + self.logfileParameters.dataset+"/"+self.logfileParameters.samplename+".h5"
            else:
                if self.logfileParameters.datasetType=="tif":
                    print "With tif files, the HDF5 angle file needs to exist"
                    sys.exit()
                else:
                    angleFileOption=" -G"
	
        if self.logfileParameters.datasetType=="tif":
            command = "/sls/X02DA/applications/tomcat-operation-scripts/reco_tools/sinooff.py " + self.logfileParameters.dataset + "/tif -q " + self.recoParameters.queue + " -N " + str(self.recoParameters.nnodes) + " -b " + self.recoParameters.branch + overlapOption + angleFileOption
        else:
	        command = "/sls/X02DA/applications/tomcat-operation-scripts/reco_tools/sinooff.py " + self.logfileParameters.dataset + " -q " + self.recoParameters.queue + " -N " + str(self.recoParameters.nnodes) + " -b " + self.recoParameters.branch + overlapOption + angleFileOption
        print(os.getcwd())
        os.system(command)
        print command

    def paganinSinogram(self,event):

        self.recoParameters.readParametersFromGUI(self.logfileParameters.originalRoiX)
        doPaganin=1
        if os.path.isdir(self.logfileParameters.datasetOut+"/fltp"):
		    if self.recoParameters.threeSixtyVariable!=0 and self.recoParameters.approachBoxIndex==1:
			    chosenResponseOptionPaganin = JOptionPane.showConfirmDialog(None, "          WARNING!!!   For optimization of the overlap parameter, please click \"Cancel\" and work in absorption mode!\n\nThe directory " + self.logfileParameters.datasetOut + "/fltp already exists and is going to be overwritten!\n\n                                                        Please click \"No\" for automatic renaming.\n\n", "Existing fltp directory", JOptionPane.YES_NO_CANCEL_OPTION,JOptionPane.QUESTION_MESSAGE);		
		    else:
			    chosenResponseOptionPaganin = JOptionPane.showConfirmDialog(None, "The directory " + self.logfileParameters.datasetOut + "/fltp already exists and is going to be overwritten!\n\n                                                        Please click \"No\" for automatic renaming.\n\n", "Existing fltp directory", JOptionPane.YES_NO_CANCEL_OPTION,JOptionPane.QUESTION_MESSAGE);

		    if chosenResponseOptionPaganin==JOptionPane.YES_OPTION:
			    if os.path.isdir(self.logfileParameters.datasetOut+"/fltp"):
				    os.system("rm -r " + self.logfileParameters.datasetOut + "/fltp")
		    elif chosenResponseOptionPaganin==JOptionPane.NO_OPTION:
			    fltpList = glob.glob(self.logfileParameters.datasetOut + "/fltp*")
			    numberExistingFltpDirectories = len(fltpList)
			    newDirectory = self.logfileParameters.datasetOut + "/fltp" + str(numberExistingFltpDirectories)
			    newSinDirectory = self.logfileParameters.datasetOut + "/sin_phase" + str(numberExistingFltpDirectories)
			    if os.path.isdir(newDirectory):
				    print IJ.showMessage("The renamed fltp directory already exists")
				    doPaganin=0
			    if os.path.isdir(newSinDirectory):
				    print IJ.showMessage("The renamed sin directory already exists")
				    doPaganin=0
			    else:
				    chosenResponseOptionRenaming = JOptionPane.showConfirmDialog(None, "The directory " + self.logfileParameters.datasetOut + "/fltp will be renamed to " + newDirectory +  "!\n\n", "Renaming fltp directory", JOptionPane.YES_NO_OPTION,JOptionPane.QUESTION_MESSAGE);
				    if chosenResponseOptionRenaming==JOptionPane.YES_OPTION:
					    os.system("mv " + self.logfileParameters.datasetOut + "/fltp " + newDirectory)
					    os.system("mv " + self.logfileParameters.datasetOut + "/sin_phase " + newSinDirectory)
				    elif chosenResponseOptionRenaming==JOptionPane.NO_OPTION:
					    doPaganin=0
		    elif chosenResponseOptionPaganin==JOptionPane.CANCEL_OPTION:
			    doPaganin=0

        angleFileOption=" "
        if self.recoParameters.geometryIndex==6:
            if os.path.isfile(self.logfileParameters.dataset+"/"+self.logfileParameters.samplename+".h5"):
			    angleFileOption="-G --separateAngles " + self.logfileParameters.dataset+"/"+self.logfileParameters.samplename+".h5"
            else:
                if self.logfileParameters.datasetType=="tif":
                    print IJ.showMessage("With tif files, the HDF5 angle file needs to exist")
                    doPaganin=0
                else:
                    angleFileOption="-G"

        if doPaganin==1:
            if self.recoParameters.threeSixtyVariable!=0:
                if self.recoParameters.approachBoxIndex==0:
                    overlapOption = " -t "
                else:
                    if self.recoParameters.overlapCenter!="0":
				        overlapOption = " -c " + self.recoParameters.overlapCenter
				        self.fields.centerField.setText(self.recoParameters.guiGuessCenter)
                    else:
				        overlapOption = ""
            else:
			    overlapOption = ""

            if self.recoParameters.paganinPaddingIndex!="0":
			    paganinPaddingOption = "-p " + str(self.recoParameters.paganinPaddingIndex)
            else:
			    paganinPaddingOption = ""
            if self.recoParameters.stabilizer!="" and self.recoParameters.width !="":
			    deconvolutionOption = "-s " + str(self.recoParameters.stabilizer) + " -w " + str(self.recoParameters.width)
            else:
			    deconvolutionOption = ""

            if self.logfileParameters.datasetType=="tif":
		        command = "/sls/X02DA/applications/tomcat-operation-scripts/reco_tools/sinooff_paganin.py " + self.logfileParameters.dataset + "/tif -q " + self.recoParameters.queue + " -N " + str(self.recoParameters.nnodes) + " -b " + self.recoParameters.branch + overlapOption + " " + paganinPaddingOption + " " + angleFileOption + " " + deconvolutionOption + " " + self.recoParameters.delta + " " + self.recoParameters.beta + " " + self.recoParameters.distance
            else:
		        command = "/sls/X02DA/applications/tomcat-operation-scripts/reco_tools/sinooff_paganin.py " + self.logfileParameters.dataset + " -q " + self.recoParameters.queue + " -N " + str(self.recoParameters.nnodes) + " -b " + self.recoParameters.branch + overlapOption + " " + paganinPaddingOption + " " + angleFileOption + " " + deconvolutionOption + " " + self.recoParameters.delta + " " + self.recoParameters.beta + " " + self.recoParameters.distance
		
            os.chdir(self.logfileParameters.datasetOut)
            os.system(command)
            print command
            self.fields.algoChooser.setSelectedIndex(1)
            self.fields.filterChooser.setSelectedIndex(4)
            
    def checkAbsorptionSinogram(self):
    
        print("Check abs")
        os.chdir(self.logfileParameters.datasetOut)
        self.absSinogramLocation=self.logfileParameters.datasetOut
        if os.path.isdir("sin")==True and "DMP" in str(os.listdir("sin")):
            os.chdir("sin")
            self.absSinogramFound=1
        else:
            self.absSinogramFound=0

        if self.absSinogramFound==0:
            os.chdir(self.logfileParameters.dataset)
            self.absSinogramLocation=self.logfileParameters.dataset
            if os.path.isdir("sin")==True and "DMP" in str(os.listdir("sin")):
                os.chdir("sin")
                self.absSinogramFound=1
            else:
                self.absSinogramFound=0
        print("abs " + str(self.absSinogramFound))

    def checkPhaseSinogram(self):

        #print("Check phase")
        os.chdir(self.logfileParameters.datasetOut)
        self.phaseSinogramLocation=self.logfileParameters.datasetOut
        if os.path.isdir("sin_phase")==True and "DMP" in str(os.listdir("sin_phase")):
            os.chdir("sin_phase")
            self.phaseSinogramFound=1
        else:
            self.phaseSinogramFound=0

        if self.phaseSinogramFound==0:
            os.chdir(self.logfileParameters.dataset)
            self.phaseSinogramLocation=self.logfileParameters.dataset
            if os.path.isdir("sin_phase")==True and "DMP" in str(os.listdir("sin_phase")):
                os.chdir("sin_phase")
                self.phaseSinogramFound=1
            else:
                self.phaseSinogramFound=0
        
        #print("phase " + str(self.phaseSinogramFound))
