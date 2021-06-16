import os, shutil
from java.awt.event import ActionListener, ItemListener
from java.awt import event
from javax.swing import JOptionPane
from ij import IJ

class CutOffFrequency(event.ActionListener):

	def __init__(self, filterC, cutOffL, cutOffF):
		
		self.filterC=filterC
		self.cutOffL=cutOffL
		self.cutOffF=cutOffF
		
		
	def actionPerformed(self,event):
		
		selFilter = self.filterC.getSelectedIndex()
		if selFilter == 0:
			self.cutOffL.setVisible(False)
			self.cutOffF.setVisible(False)
		else:
			self.cutOffL.setVisible(True)
			self.cutOffF.setVisible(True)

class AlgorithmParameters(event.ActionListener):

	def __init__(self,algoC,filterC):

		self.algoC=algoC
		self.filterC=filterC
		
		
	def actionPerformed(self,event):
	
		algorithmOption = self.algoC.getSelectedIndex()
		if algorithmOption == 0:
			self.filterC.setSelectedIndex(5)
		elif algorithmOption==1:
			self.filterC.setSelectedIndex(4)
		elif algorithmOption==2:
			IJ.showMessage("This option has not been implemented yet!" )			
			self.algoC.setSelectedIndex(0)
			self.filterC.setSelectedIndex(5)

class ZingerParameters(event.ActionListener):

	def __init__(self,zingerB,zingerTL,zingerTF,zingerKL,zingerKF):

		self.zingerB=zingerB
		self.zingerTL=zingerTL
		self.zingerTF=zingerTF
		self.zingerKL=zingerKL
		self.zingerKF=zingerKF
		
	def actionPerformed(self,event):
		
		zingerOption = self.zingerB.getSelectedIndex()
		if zingerOption == 0:
			self.zingerTL.setVisible(False)
			self.zingerTF.setVisible(False)
			self.zingerKL.setVisible(False)
			self.zingerKF.setVisible(False)
		elif zingerOption==1:
			self.zingerTL.setVisible(True)
			self.zingerTF.setVisible(True)
			self.zingerKL.setVisible(True)
			self.zingerKF.setVisible(True)

class RingParameters(event.ActionListener):
	
	def __init__(self,fields):

		self.fields=fields
	
	def actionPerformed(self,event):
	
		ringFilter = self.fields.ringChooser.getSelectedIndex()
		if ringFilter == 0 or ringFilter == 1:
			self.fields.wsLabel.setVisible(False)
			self.fields.wsField.setVisible(False)
			self.fields.waveletTypeLabel.setVisible(False)
			self.fields.waveletTypeChooser.setVisible(False)
			self.fields.waveletComponentMinLabel.setVisible(False)
			self.fields.waveletComponentMinField.setVisible(False)
			self.fields.waveletComponentMaxLabel.setVisible(False)
			self.fields.waveletComponentMaxField.setVisible(False)
			self.fields.waveletFilterWidthLabel.setVisible(False)
			self.fields.waveletFilterWidthField.setVisible(False)
			self.fields.waveletPaddingLabel.setVisible(False)
			self.fields.waveletPaddingBox.setVisible(False)
			self.fields.muenchRef.setVisible(False)
			self.fields.wslLabel.setVisible(False)
			self.fields.wslField.setVisible(False)
			self.fields.wssmLabel.setVisible(False)
			self.fields.wssmField.setVisible(False)
			self.fields.snrLabel.setVisible(False)
			self.fields.snrField.setVisible(False)
			self.fields.sarepyRef.setVisible(False)			
		elif ringFilter == 2:
			self.fields.wsLabel.setVisible(True)
			self.fields.wsField.setVisible(True)
			self.fields.waveletTypeLabel.setVisible(False)
			self.fields.waveletTypeChooser.setVisible(False)
			self.fields.waveletComponentMinLabel.setVisible(False)
			self.fields.waveletComponentMinField.setVisible(False)
			self.fields.waveletComponentMaxLabel.setVisible(False)
			self.fields.waveletComponentMaxField.setVisible(False)
			self.fields.waveletFilterWidthLabel.setVisible(False)
			self.fields.waveletFilterWidthField.setVisible(False)
			self.fields.waveletPaddingLabel.setVisible(False)
			self.fields.waveletPaddingBox.setVisible(False)
			self.fields.muenchRef.setVisible(False)
			self.fields.wslLabel.setVisible(False)
			self.fields.wslField.setVisible(False)
			self.fields.wssmLabel.setVisible(False)
			self.fields.wssmField.setVisible(False)
			self.fields.snrLabel.setVisible(False)
			self.fields.snrField.setVisible(False)			
			self.fields.sarepyRef.setVisible(True)			
		elif ringFilter == 3:
			self.fields.wsLabel.setVisible(False)
			self.fields.wsField.setVisible(False)
			self.fields.waveletTypeLabel.setVisible(True)
			self.fields.waveletTypeChooser.setVisible(True)
			self.fields.waveletComponentMinLabel.setVisible(True)
			self.fields.waveletComponentMinField.setVisible(True)
			self.fields.waveletComponentMaxLabel.setVisible(True)
			self.fields.waveletComponentMaxField.setVisible(True)
			self.fields.waveletFilterWidthLabel.setVisible(True)
			self.fields.waveletFilterWidthField.setVisible(True)
			self.fields.waveletPaddingLabel.setVisible(True)
			self.fields.waveletPaddingBox.setVisible(True)
			self.fields.muenchRef.setVisible(True)
			self.fields.wslLabel.setVisible(False)
			self.fields.wslField.setVisible(False)
			self.fields.wssmLabel.setVisible(False)
			self.fields.wssmField.setVisible(False)
			self.fields.snrLabel.setVisible(False)
			self.fields.snrField.setVisible(False)			
			self.fields.sarepyRef.setVisible(False)			
		elif ringFilter == 4:
			self.fields.wsLabel.setVisible(False)
			self.fields.wsField.setVisible(False)
			self.fields.waveletTypeLabel.setVisible(False)
			self.fields.waveletTypeChooser.setVisible(False)
			self.fields.waveletComponentMinLabel.setVisible(False)
			self.fields.waveletComponentMinField.setVisible(False)
			self.fields.waveletComponentMaxLabel.setVisible(False)
			self.fields.waveletComponentMaxField.setVisible(False)
			self.fields.waveletFilterWidthLabel.setVisible(False)
			self.fields.waveletFilterWidthField.setVisible(False)
			self.fields.waveletPaddingLabel.setVisible(False)
			self.fields.waveletPaddingBox.setVisible(False)
			self.fields.muenchRef.setVisible(False)
			self.fields.wslLabel.setVisible(True)
			self.fields.wslField.setVisible(True)
			self.fields.wssmLabel.setVisible(True)
			self.fields.wssmField.setVisible(True)
			self.fields.snrLabel.setVisible(True)
			self.fields.snrField.setVisible(True)			
			self.fields.sarepyRef.setVisible(True)			
		
class LevelParameters(event.ActionListener):

	def __init__(self,outputC,minL,minF,maxL,maxF,getBB,applyBB):

		self.outputC=outputC
		self.minL=minL
		self.minF=minF
		self.maxL=maxL
		self.maxF=maxF
		self.getBB=getBB
		self.applyBB=applyBB

	def actionPerformed(self,event):
	
		outputFormat = self.outputC.getSelectedIndex()
		if outputFormat == 0:
			self.minL.setVisible(False)
			self.minF.setVisible(False)
			self.maxL.setVisible(False)
			self.maxF.setVisible(False)
			self.getBB.setVisible(False)
			self.applyBB.setVisible(False)		
		elif outputFormat == 1 or outputFormat == 2:
			self.minL.setVisible(True)
			self.minF.setVisible(True)
			self.maxL.setVisible(True)
			self.maxF.setVisible(True)
			self.getBB.setVisible(True)
			self.applyBB.setVisible(True)

class ApproachSelection(event.ActionListener):

    def __init__(self,fields):

        self.fields = fields
        self.originalGeometry = 4
        
    def actionPerformed(self,event):
    
        chosenApproach = self.fields.approachBox.getSelectedIndex()
        if chosenApproach == 0:
            self.fields.overlapLabel.setVisible(False)
            self.fields.overlapField.setVisible(False)
            if self.originalGeometry != 4:
                 self.fields.geometryBox.setSelectedIndex(self.originalGeometry)
        else:
            self.originalGeometry = self.fields.geometryBox.getSelectedIndex()
            self.fields.overlapLabel.setVisible(True)
            self.fields.overlapField.setVisible(True)
            self.fields.geometryBox.setSelectedIndex(1)
          
class CleanButton(event.ActionListener):

    def __init__(self,logfileParameters):

        self.logfileParameters=logfileParameters
        
    def actionPerformed(self,event):
		
        chosenResponseOptionCleanButton = JOptionPane.showConfirmDialog(None, "If existing, temporary directories (fltp, sin, ...) for this dataset will be removed. Do you want to proceed?", "Temporary directory removal", JOptionPane.YES_NO_CANCEL_OPTION,JOptionPane.QUESTION_MESSAGE);
    
        if chosenResponseOptionCleanButton==JOptionPane.YES_OPTION:
            os.chdir(self.logfileParameters.datasetOut)
            print "Directories will be removed"
            if os.path.isdir(self.logfileParameters.datasetOut + "/sin")==True:
                shutil.rmtree(self.logfileParameters.datasetOut + "/sin", ignore_errors=True)
            if os.path.isdir(self.logfileParameters.datasetOut + "/sin_phase")==True:
                shutil.rmtree(self.logfileParameters.datasetOut + "/sin_phase")
            if os.path.isdir(self.logfileParameters.datasetOut + "/fltp")==True:
                shutil.rmtree(self.logfileParameters.datasetOut + "/fltp")
            if os.path.isdir(self.logfileParameters.datasetOut + "/cpr")==True:
                shutil.rmtree(self.logfileParameters.datasetOut + "/cpr")
            if os.path.isdir(self.logfileParameters.datasetOut + "/sin_tmp")==True:
                shutil.rmtree(self.logfileParameters.datasetOut + "/sin_tmp")                
            
class ExpertSelection(event.ItemListener):

    def __init__(self,world,fields):

        self.world = world
        self.fields = fields

    def itemStateChanged(self,event):

        if self.fields.expertBox.isSelected() == True:
            self.fields.branchLabel.setVisible(True)
            self.fields.masterButton.setVisible(True)
            self.fields.develButton.setVisible(True)
            if self.world=="online":
                self.fields.queueLabel.setVisible(True)
                self.fields.NBButton.setVisible(True)
                self.fields.oldButton.setVisible(True)
                self.fields.wholeButton.setVisible(True)
                self.fields.nnodeLabel.setVisible(True)
                self.fields.nnodeChooser.setVisible(True)
            else:
                self.fields.queueLabel.setVisible(False)
                self.fields.NBButton.setVisible(False)
                self.fields.oldButton.setVisible(False)
                self.fields.wholeButton.setVisible(False)
                self.fields.nnodeLabel.setVisible(False)
                self.fields.nnodeChooser.setVisible(False)
        else:
            self.fields.branchLabel.setVisible(False)
            self.fields.masterButton.setVisible(False)
            self.fields.develButton.setVisible(False)
            self.fields.queueLabel.setVisible(False)
            self.fields.NBButton.setVisible(False)
            self.fields.oldButton.setVisible(False)
            self.fields.wholeButton.setVisible(False)
            self.fields.nnodeLabel.setVisible(False)
            self.fields.nnodeChooser.setVisible(False)

class GetLastParameters(event.ActionListener):

	def __init__(self,recoParameters):
	
	    self.recoParameters = recoParameters
		
	def actionPerformed(self,event):
	
		self.recoParameters.readParametersFromFile("scratch")
		self.recoParameters.writeParametersToGUI()

class OptimizeRecoSlice():

    def __init__(self,reconstructedSlice,fields):

        self.reconstructedSlice = reconstructedSlice
        self.fields = fields

    def GetBoth(self,event):

        tmpLevel=self.reconstructedSlice.getDisplayRangeMin()
        minLevel="%(minlevel).3e" % {'minlevel':tmpLevel}
        tmpLevel=self.reconstructedSlice.getDisplayRangeMax()
        maxLevel="%(maxlevel).3e" % {'maxlevel':tmpLevel}
        self.fields.minField.setText(str(minLevel))
        self.fields.maxField.setText(str(maxLevel))	

    def ApplyBoth(self,event):

        minLevel=self.fields.minField.getText()
        maxLevel=self.fields.maxField.getText()
        self.reconstructedSlice.setDisplayRange(float(minLevel),float(maxLevel))
        self.reconstructedSlice.updateAndDraw()

    def SetRoi(self,event):

        IJ.setTool("rectangle")
        win=self.reconstructedSlice.getWindow()
        win.toFront()
        IJ.showMessage("Select a region of interest")

    def DoneRoi(self,event):

        currentRoi=self.reconstructedSlice.getRoi()
        x=currentRoi.getBounds().getX()
        self.fields.x1Field.setText(str(int(x)))
        y=currentRoi.getBounds().getY()
        self.fields.y1Field.setText(str(int(y)))
        widthLocal=currentRoi.getBounds().getWidth()
        self.fields.x2Field.setText(str(int(x+widthLocal)))
        height=currentRoi.getBounds().getHeight()
        self.fields.y2Field.setText(str(int(y+height))) 

    def ResetRoi(self,event):

        self.fields.x1Field.setText("0")
        self.fields.y1Field.setText("0")
        self.fields.x2Field.setText("0")
        self.fields.y2Field.setText("0")
        self.reconstructedSlice.killRoi()

class OriginalRotationCenter():

    def __init__(self,logfileParameters,recoParameters,fields):

        self.logfileParameters = logfileParameters
        self.recoParameters = recoParameters
        self.fields = fields
 
    def getOriginalRotationCenter(self,event):

        tmpCenter="0"
        tmpOriginalCenter="0"

        FILE = open(self.logfileParameters.logfile,"r")
        self.logfileParameters.foundStitched=0
        self.logfileParameters.foundOriginal=0
        for line in FILE:
            linelist=line.split()
            if len(linelist)>0:
                if self.recoParameters.threeSixtyVariable==0:
                    if linelist[0]=="Original" and linelist[1]=="rotation" and self.logfileParameters.foundOriginal==0:
                        if len(linelist)==5:
                            tmpCenter=linelist[4]
                        else:
                            tmpCenter=linelist[3]
                        self.logfileParameters.foundOriginal=1
                else:
                    if linelist[0]=="Rotation" and linelist[1]=="center" and len(linelist)==7 and self.logfileParameters.foundStitched==0:
                        tmpCenter=linelist[6]
                        self.logfileParameters.foundStitched=1
                    elif linelist[0]=="Rotation" and linelist[1]=="center" and len(linelist)==6 and self.logfileParameters.foundStitched==0:
                        tmpCenter=linelist[5]
                        self.logfileParameters.foundStitched=1
                    elif linelist[0]=="Original" and linelist[1]=="rotation" and len(linelist)==5 and self.logfileParameters. foundOriginal==0:
                        tmpOriginalCenter=linelist[4]
                        self.logfileParameters.foundOriginal=1
                    elif linelist[0]=="Original" and linelist[1]=="rotation" and len(linelist)==4 and self.logfileParameters.foundOriginal==0:
                        tmpOriginalCenter=linelist[3]
                        self.logfileParameters.foundOriginal=1
                    self.recoParameters.axisBoxIndex=self.fields.axisBox.getSelectedIndex()
                    if self.recoParameters.axisBoxIndex==1:
                        if tmpOriginalCenter!="0":
                            tmpRealOverlap=str(2*float(tmpOriginalCenter))
                            self.fields.overlapField.setText(tmpRealOverlap)
                    elif self.recoParameters.axisBoxIndex==0:
                        if tmpOriginalCenter!="0":
                            tmpRealOverlap=str(2*(float(self.logfileParameters.originalRoiX)-float(tmpOriginalCenter)))
                            self.fields.overlapField.setText(tmpRealOverlap)
                    else:
                        IJ.showMessage("The rotation axis has not been positioned at the side of the field of view or this is not recorded in the log file!" )

        FILE.close()
        self.fields.centerField.setText(tmpCenter)			
