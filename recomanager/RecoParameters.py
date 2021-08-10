import os
import sys
from os.path import expanduser

class RecoParameters:

	def __init__(self, world, fields):

		self.world = world
		self.fields = fields
		
		self.setToDefaults()
		

	def setToDefaults(self):	

		self.algorithm = 0
#		self.branch = "master"
#		self.usedBranch = "Beamline"
#		self.queue = "tomcat_NB.q"
#		self.nnodes = 4
		self.FileLocation = ""
		self.nsinoperchunk = "256"
		self.centerSearchWidth= "10"
		self.gridrecPadding = 0
		self.stripeMethod = 0
		self.fwpad = 0


		
		self.sliceNumber = "1"
		self.guiCenter = "0"
		self.rotation = "0"
		self.zeroPadding = "0.5"
		self.geometryIndex = 1
		
		self.filterIndex = 5
		self.filterUsed = "Parzen"
		self.cutOffFrequency = "0.5"
		self.filterOption = "parz"
		
		self.zingerIndex = 0
		self.zinger = "Off"
		self.zingerOption = "False"
		self.threshold = "0"
		self.kernelWidth = "0"
		
		self.ringIndex = 0
		self.ringOption = "0"
		self.windowSize = "31"
		self.windowSizeL = "81"
		self.windowSizeSM = "31"
		self.snr = "3.0"
		self.waveletType = "db15"
		self.waveletTypeIndex = 13
		self.waveletMinComponent = "0"
		self.waveletMaxComponent = "4"
		self.waveletFilterWidth = "1.0"
		self.waveletPadding = "Standard"
		self.waveletPaddingIndex = 0
		
		self.outputFormatIndex = 1
		self.outputFormat = "8"
		self.minimum = "0"
		self.maximum = "0"
		
		self.roiX1 = "0"
		self.roiY1 = "0"
		self.roiX2 = "0"
		self.roiY2 = "0"
		
		self.postfix = ""
		
		self.shiftingIndex = 0
		self.shifting = ""
		
		self.delta = ""
		self.beta = ""
		self.distance = ""
		
		self.paganinPaddingIndex = 0
		self.paganinPadding = ""
		self.stabilizer = ""
		self.width = ""
		
		self.threeSixtyVariable = 0
		self.axisBoxIndex = 0
		self.realOverlap = "0"
		self.overlapCenter = "0"
		self.guiGuessCenter = ""
		self.approachBoxIndex = self.fields.approachBox.getSelectedIndex()
			

	def readParametersFromFile(self,whichfile,dataset="",datasetOut=""):
	
		# if whichfile == "scratch":
		# 	# Read parameters from scratch file
		# 	print "Read from scratch file"
		# 	if self.world=="offline":
		# 		userId=os.getlogin()
		# 		localFile = "/tmp/GUIParameters"+str(userId)+".txt"
		# 	elif self.world=="online":
		# 		userId=os.getlogin()
		# 		localFile = "/scratch/GUIParameters"+str(userId)+".txt"
		# 	else:
		# 		print "Unknown environment!" 
		# else:
			# Read parameters from local file
		print "Read from local file"
		home = expanduser("~")

		localFile = os.path.join(home, "GUIParameters.txt")
			# if self.world=="offline":
			# 	if os.path.isfile(localFile):
			# 		pass
			# 	else:
			# 		localFile = dataset + "/GUIParameters.txt"	
		print localFile
		
		self.guiCenter = self.fields.centerField.getText()
		
		FILE = open(localFile,"r")
		for line in FILE:
			linelist=line.split()
			if len(linelist)>0:
	   			if linelist[0]=="Algorithm":
	   				self.algorithm=linelist[1]
	   			elif linelist[0]=="Gridrec":
	   				self.gridrecPadding=linelist[1]
	   			elif linelist[0]=="RemoveStripeMethod":
	   				self.stripeMethod=linelist[1]
	   			elif linelist[0]=="fw-pad-setting":
	   				self.fwpad=linelist[1]
#	   			elif linelist[0]=="Branch":
#					self.branch=linelist[1]
#	   			elif linelist[0]=="Queue":
#					self.queue=linelist[1]
#	   			elif linelist[0]=="Nnodes":
#					self.nnodes=int(linelist[1])
				elif linelist[0]=="FileName":
					self.FileLocation=linelist[1]
				elif linelist[0]=="SearchWidth":
					self.centerSearchWidth=linelist[1]
				elif linelist[0]=="nsinoperchunk":
					self.nsinoperchunk=linelist[1]
	   			elif linelist[0]=="Center":
					self.centerNumber=linelist[1]
				elif linelist[0]=="Slice":
					self.sliceNumber=linelist[1]
	   			elif linelist[0]=="Postfix":
	   				if linelist[1]=="0":
	   					self.postfix=""
	   				else:
	   					self.postfix=linelist[1]
	   			elif linelist[0]=="Rotation":
					self.rotation=linelist[1]
				elif linelist[0]=="RotationCenter":
					self.centerNumber==linelist[1]
	   			elif linelist[0]=="Filter":
	   				self.filterIndex=int(linelist[1])
	   			elif linelist[0]=="Cutoff":
					self.cutOffFrequency=linelist[2]
	   			elif linelist[0]=="Padding":
					self.zeroPadding=linelist[1]
	   			elif linelist[0]=="Geometry":
	   				if linelist[1]=="6":
	   					linelist[1]="3"
					self.geometryIndex=int(linelist[1])
	   			elif linelist[0]=="Ring":
					self.ringIndex=int(linelist[2])
	   			elif linelist[0]=="windowSize":
					self.windowSize=linelist[1]
	   			elif linelist[0]=="windowSizeL":
					self.windowSizeL=linelist[1]
	   			elif linelist[0]=="windowSizeSM":
					self.windowSizeSM=linelist[1]
	   			elif linelist[0]=="SNR":
					self.snr=linelist[1]
	   			elif linelist[1]=="type":
					self.waveletTypeIndex=int(linelist[2])
	   			elif linelist[1]=="min":
					self.waveletMinComponent=linelist[3]
	   			elif linelist[1]=="max":
					self.waveletMaxComponent=linelist[3]
	   			elif linelist[1]=="filter":
					self.waveletFilterWidth=linelist[3]
	   			elif linelist[1]=="padding":
					self.waveletPaddingIndex=int(linelist[2])
	   			elif linelist[0]=="Zinger":
	   				if linelist[2]=="True":
						self.zingerIndex="1"            
					else:                   
						self.zingerIndex="0"            
	   			elif linelist[0]=="Threshold":
					self.threshold=linelist[1]				
	   			elif linelist[0]=="Kernel":
					self.kernelWidth=linelist[2]				                                
	   			elif linelist[0]=="Output":
					self.outputFormat=linelist[2]
	   				if linelist[2]=="0":
	   					self.outputFormatIndex=0
	   				elif linelist[2]=="8":
	   					self.outputFormatIndex=1
	   				elif linelist[2]=="16":
	   					self.outputFormatIndex=2
	   			elif linelist[0]=="Minimum":
					self.minimum=linelist[1]				
	   			elif linelist[0]=="Maximum":
					self.maximum=linelist[1]				
	   			elif linelist[0]=="X1":
					self.roiX1=linelist[1]				
	   			elif linelist[0]=="X2":
					self.roiX2=linelist[1]				
	   			elif linelist[0]=="Y1":
					self.roiY1=linelist[1]				
	   			elif linelist[0]=="Y2":
					self.roiY2=linelist[1]				
	   			elif linelist[0]=="Shifting":
					self.shiftingIndex=int(linelist[1])
	   			elif linelist[0]=="Axis":
	   				self.axisBoxIndex=int(linelist[2])
	   				self.threeSixtyVariable=1
				elif linelist[0]=="Approach":
					self.approachBoxIndex=int(linelist[1])
	   			elif linelist[0]=="Real":
	   				self.realOverlap=linelist[2]
	   			elif linelist[0]=="Delta":
					self.delta=linelist[1]			
	   			elif linelist[0]=="Beta":
					self.beta=linelist[1]				
	   			elif linelist[0]=="Distance":
					self.distance=linelist[1]				
	   			elif linelist[1]=="Paganin":
					self.paganinPaddingIndex=int(linelist[3])			
	   			elif linelist[0]=="Stabilizer":
					self.stabilizer=linelist[1]			
	   			elif linelist[0]=="Gaussian":
					self.width=linelist[3]			
			
		FILE.close()		
		

	def readParametersFromGUI(self,originalRoiX):
	
		self.sliceNumber = self.fields.sliceField.getText()
		self.algorithm = self.fields.algoChooser.getSelectedIndex()
		self.nsinoperchunk = self.fields.nsinochunkField.getText()
		self.FileLocation = self.fields.selectedDatasetField.getText()
		self.centerSearchWidth = self.fields.searchWidthField.getText()
		self.gridrecPadding = self.fields.gridrecChooser.getSelectedIndex()
		self.stripeMethod = self.fields.stripeMethodChooser.getSelectedIndex()
		self.fwpad = self.fields.fwpadChooser.getSelectedIndex()
		if self.fields.masterButton.isSelected():
			self.branch="master"
			self.usedBranch="Apy3_m"
			print "Master Button is selected"
		elif self.fields.develButton.isSelected():
			self.branch="devel"
			#self.usedBranch="Anaconda_d"
			self.usedBranch="Apy3_d"
			print "Devel Button is selected"
		else:
			print "This branch option is not implemented yet"
			sys.exit()
	
		if self.fields.NBButton.isSelected():
			self.queue="tomcat_NB.q"
			print "NBButton is selected"
		elif self.fields.oldButton.isSelected():
			self.queue="tomcat_old"
			print "oldButton is selected"
		elif self.fields.wholeButton.isSelected():
			self.queue="tomcat_whole"
			print "wholeButton is selected"
		else:
			print "This queue option is not implemented yet"
			sys.exit()
    
		self.nnodes=self.fields.nnodeChooser.getSelectedIndex()+1
		if self.queue=="tomcat_whole":
			if self.nnodes>8:
				self.nnodes=8
				self.fields.nnodeChooser.setSelectedIndex(7)
		else:
			if self.nnodes>4:
				self.nnodes=4
				self.fields.nnodeChooser.setSelectedIndex(3)            

		self.guiCenter = self.fields.centerField.getText()
		self.rotation = self.fields.rotField.getText()
		while float(self.rotation)>180.0:
			self.rotation=str(float(self.rotation)-360.0)
		while float(self.rotation)<-180.0:
			self.rotation=str(float(self.rotation)+360.0)
		self.zeroPadding = self.fields.zeroPaddingField.getText()
		self.geometryIndex = self.fields.geometryBox.getSelectedIndex()
		if self.geometryIndex==3:
			self.geometryIndex=6
	
		self.filterIndex = self.fields.filterChooser.getSelectedIndex()
		self.filterUsed = self.fields.filterList[self.filterIndex]
		if self.filterIndex!=0:
			self.cutOffFrequency = self.fields.cutOffField.getText()
		if self.filterIndex==0:
			self.filterOption = "none"
		elif self.filterIndex==1:
			self.filterOption = "shlo"
		elif self.filterIndex==2:
			self.filterOption = "hann"
		elif self.filterIndex==3:
			self.filterOption = "hamm"
		elif self.filterIndex==4:
			self.filterOption = "ramp"
		elif self.filterIndex==5:
			self.filterOption = "parz"
		elif self.filterIndex==6:
			self.filterOption = "lanc"
		elif self.filterIndex==7:
			self.filterOption = "dpc"
		
		self.zingerIndex = self.fields.zingerBox.getSelectedIndex()
		self.zinger = self.fields.zingerList[self.zingerIndex]
		if self.zingerIndex!=0:
			self.zingerOption = "True"
			self.threshold = self.fields.zingerThresholdField.getText()
			self.kernelWidth = self.fields.zingerKernelWidthField.getText()
		else:
			self.zingerOption = "False"
			self.threshold = "0"
			self.kernelWidth = "0"
	
		self.ringIndex = self.fields.ringChooser.getSelectedIndex()
		if self.ringIndex==0:
			self.ringOption = "0"  
			self.windowSize = "0"
			self.windowSizeL = "0"
			self.windowSizeSM = "0"
			self.snr = "0"
			self.waveletType = "0"
			self.waveletMinComponent = "0"
			self.waveletMaxComponent = "0"
			self.waveletFilterWidth = "0"
			self.waveletPadding = "0"
		elif self.ringIndex==1:
			self.ringOption = "1"  # new option
			self.windowSize = "0"
			self.windowSizeL = "0"
			self.windowSizeSM = "0"
			self.snr = "0"
			self.waveletType = "0"
			self.waveletMinComponent = "0"
			self.waveletMaxComponent = "0"
			self.waveletFilterWidth = "0"
			self.waveletPadding = "0"
		elif self.ringIndex==2:
			self.ringOption = "2"  # original option 1 (used)
			self.windowSize = self.fields.wsField.getText()
			self.windowSizeL = "0"
			self.windowSizeSM = "0"
			self.snr = "0"
			self.waveletType = "0"
			self.waveletMinComponent = "0"
			self.waveletMaxComponent = "0"
			self.waveletFilterWidth = "0"
			self.waveletPadding = "0"
		elif self.ringIndex==3:
			self.ringOption = "3"  # wavelet
			self.windowSize = "0"
			self.windowSizeL = "0"
			self.windowSizeSM = "0"
			self.snr = "0"
			self.waveletTypeIndex = self.fields.waveletTypeChooser.getSelectedIndex()
			self.waveletType = self.fields.waveletTypeList[self.waveletTypeIndex]
			self.waveletMinComponent = self.fields.waveletComponentMinField.getText()
			self.waveletMaxComponent = self.fields.waveletComponentMaxField.getText()
			self.waveletFilterWidth = self.fields.waveletFilterWidthField.getText()
			self.waveletPaddingIndex = self.fields.waveletPaddingBox.getSelectedIndex()
			self.waveletPadding = self.fields.paddingList[self.waveletPaddingIndex]
		elif self.ringIndex==4:
			self.ringOption = "4"  # new option
			self.windowSize = "0"
			self.windowSizeL = self.fields.wslField.getText()
			self.windowSizeSM = self.fields.wssmField.getText()
			self.snr = self.fields.snrField.getText()
			self.waveletType = "0"
			self.waveletMinComponent = "0"
			self.waveletMaxComponent = "0"
			self.waveletFilterWidth = "0"
			self.waveletPadding = "0"
	
		self.outputFormatIndex = self.fields.outputChooser.getSelectedIndex()
		if self.outputFormatIndex == 0:
			self.outputFormat="0"
			self.minimum="0"
			self.maximum="0"
		elif self.outputFormatIndex==1:
			self.outputFormat="8" 
			self.minimum = self.fields.minField.getText()
			self.maximum = self.fields.maxField.getText()
		elif self.outputFormatIndex==2:
			self.outputFormat="16" 
			self.minimum = self.fields.minField.getText()
			self.maximum = self.fields.maxField.getText()

		self.roiX1=self.fields.x1Field.getText()
		self.roiY1=self.fields.y1Field.getText()
		self.roiX2=self.fields.x2Field.getText()
		self.roiY2=self.fields.y2Field.getText()

		self.postfix=self.fields.postfixField.getText()
		if self.postfix=="":
			self.postfix="0"

		self.shiftingIndex=self.fields.shiftingBox.getSelectedIndex()
		if self.shiftingIndex==0:
			self.shifting="False"
		else:
			self.shifting="True"

		if self.threeSixtyVariable==1:
			self.approachBoxIndex=self.fields.approachBox.getSelectedIndex()
			self.axisBoxIndex=self.fields.axisBox.getSelectedIndex()
			if self.approachBoxIndex==1:
				self.realOverlap=self.fields.overlapField.getText()
				if self.realOverlap!="0":
					if self.axisBoxIndex==0:
						self.overlapCenter=str(float(originalRoiX)-0.5*float(self.realOverlap))
						self.guiGuessCenter=self.overlapCenter
					else:
						self.overlapCenter=str(0.5*float(self.realOverlap))
						self.guiGuessCenter=str(float(originalRoiX)+0.5*float(self.realOverlap))
				else:
					self.guiGuessCenter="0"
					self.overlapCenter="0"	

		self.delta=self.fields.deltaField.getText()
		self.beta=self.fields.betaField.getText()
		self.distance=self.fields.distanceField.getText()

		self.paganinPaddingIndex = self.fields.paganinPaddingBox.getSelectedIndex()
		self.paganinPadding = self.fields.paganinPaddingList[self.paganinPaddingIndex]
		self.stabilizer = self.fields.paganinStabilizerField.getText()
		self.width = self.fields.paganinWidthField.getText()
	

	def writeParametersToFile(self, whichfile,dataset="", datasetOut=""):

		# if whichfile == "scratch":
		# 	if self.world=="offline":
		# 		userId=os.getlogin()
		# 		localFile = "/tmp/GUIParameters"+str(userId)+".txt"
		# 	elif self.world=="online":
		# 		userId=os.getlogin()
		# 		localFile = "/scratch/GUIParameters"+str(userId)+".txt"
		# 	else:
		# 		print "Unknown environment!"    				
		# else:
		# 	localFile = datasetOut + "/GUIParameters.txt"
		# 	if self.world=="offline":
		# 		if os.path.isfile(localFile):
		# 			pass
		# 		else:
		# 			localFile = dataset + "/GUIParameters.txt"	
		home = expanduser("~")

		localFile = os.path.join(home, "GUIParameters.txt")

		print localFile
		print "Write to local file"
		
		try:
			FILE = open(localFile,"w+")
			FILE.write("Algorithm                  " + str(self.algorithm) +"\n")
			# FILE.write("Branch                     " + str(self.branch) +"\n")
			# FILE.write("Queue                      " + str(self.queue) +"\n")
			# FILE.write("Nnodes                     " + str(self.nnodes) +"\n")
			# FILE.write("Postfix                    " + self.postfix + "\n")
			# if whichfile != "scratch":
			# 	FILE.write("Center                     " + self.guiCenter + "\n")
			# FILE.write("Filter                     " + str(self.filterIndex) + "\n")
			# FILE.write("Cutoff frequency           " + self.cutOffFrequency + "\n")
			FILE.write("Rotation                   " + self.rotation + "\n")
			FILE.write("Center                     " + self.centerNumber + "\n")
			FILE.write("Slice                      " + self.sliceNumber + "\n")
			FILE.write("FileName                   " + self.FileLocation + '\n')
			FILE.write("nsino-per-chunk            " + self.nsinoperchunk + "\n")
			FILE.write("SearchWidth                " + self.centerSearchWidth + "\n")
			FILE.write("Gridrec                    " + str(self.gridrecPadding) + "\n")
			FILE.write("RemoveStripeMethod         " + str(self.stripeMethod) + "\n")
			FILE.write("fw-pad-setting             " + str(self.fwpad) + "\n")
			# FILE.write("Padding                    " + self.zeroPadding + "\n")
			# FILE.write("Geometry                   " + str(self.geometryIndex) + "\n")
			# FILE.write("Ring option                " + self.ringOption + "\n")	
			# if self.ringOption=="2":
			# 	FILE.write("windowSize                 " + self.windowSize + "\n")
			# elif self.ringOption=="3":
			# 	FILE.write("Wavelet type               " + str(self.waveletTypeIndex) + "\n")
			# 	FILE.write("Wavelet min comp           " + self.waveletMinComponent + "\n")
			# 	FILE.write("Wavelet max comp           " + self.waveletMaxComponent + "\n")
			# 	FILE.write("Wavelet filter width       " + self.waveletFilterWidth + "\n")
			# 	FILE.write("Wavelet padding            " + str(self.waveletPaddingIndex) + "\n")
			# elif self.ringOption=="4":
			# 	FILE.write("windowSizeL                " + self.windowSizeL + "\n")
			# 	FILE.write("windowSizeSM               " + self.windowSizeSM + "\n")
			# 	FILE.write("SNR                        " + self.snr + "\n")
			# FILE.write("Zinger option              " + self.zingerOption + "\n")
			# if self.zingerOption!="False":
			# 	FILE.write("Threshold                  " + self.threshold + "\n")
			# 	FILE.write("Kernel Width               " + self.kernelWidth + "\n")
			# FILE.write("Output format              " + self.outputFormat + "\n")
			# if self.outputFormat!="0":
			# 	FILE.write("Minimum                    " + self.minimum + "\n")
			# 	FILE.write("Maximum                    " + self.maximum + "\n")
			# FILE.write("X1                         " + self.roiX1 + "\n")
			# FILE.write("X2                         " + self.roiX2 + "\n")
			# FILE.write("Y1                         " + self.roiY1 + "\n")
			# FILE.write("Y2                         " + self.roiY2 + "\n")
			# FILE.write("Shifting                   " + str(self.shiftingIndex) + "\n")
			# if self.threeSixtyVariable==1:
			# 	FILE.write("Axis position              " + str(self.axisBoxIndex) + "\n")		
			# 	FILE.write("Real overlap               " + str(self.realOverlap) + "\n")
			# 	FILE.write("Approach                   " + str(self.approachBoxIndex) + "\n")		
			# if self.delta != "":
			# 	FILE.write("Delta                      " + self.delta + "\n")
			# if self.beta != "":
			# 	FILE.write("Beta                       " + self.beta + "\n")
			# if self.distance != "":
			# 	FILE.write("Distance                   " + self.distance + "\n")
			# 	FILE.write("FFT Paganin padding        " + str(self.paganinPaddingIndex) + "\n")
			# if self.stabilizer != "":
			# 	FILE.write("Stabilizer                 " + self.stabilizer + "\n")
			# if self.width != "":
			# 	FILE.write("Gaussian kernel width      " + self.width + "\n")
			FILE.write("\n")
 			FILE.close()
		except IOError:
			pass
	
		
	def writeParametersToGUI(self):

   		self.fields.algoChooser.setSelectedIndex(int(self.algorithm))
		self.fields.sliceField.setText(str(self.sliceNumber))
		self.fields.selectedDatasetField.setText(str(self.FileLocation))
		self.fields.gridrecChooser.setSelectedIndex(int(self.gridrecPadding))
		self.fields.stripeMethodChooser.setSelectedIndex(int(self.stripeMethod))
		self.fields.fwpadChooser.setSelectedIndex(int(self.fwpad))

		
#	   	if self.branch=="master":
#	  		self.fields.masterButton.setSelected(True)
#	  	else:
#	   		self.fields.develButton.setSelected(True)

 		self.fields.postfixField.setText(self.postfix)
		self.fields.centerField.setText(self.centerNumber)
		self.fields.rotField.setText(self.rotation)
		self.fields.nsinochunkField.setText(self.nsinoperchunk)
		self.fields.searchWidthField.setText(self.centerSearchWidth)

	   	self.fields.filterChooser.setSelectedIndex(self.filterIndex)
		self.fields.cutOffField.setText(self.cutOffFrequency)
		self.fields.zeroPaddingField.setText(self.zeroPadding)
		self.fields.geometryBox.setSelectedIndex(self.geometryIndex)

		self.fields.ringChooser.setSelectedIndex(self.ringIndex)
		self.fields.snrField.setText(self.snr)
		self.fields.wsField.setText(self.windowSize)
		self.fields.wslField.setText(self.windowSizeL)
		self.fields.wssmField.setText(self.windowSizeSM)
		self.fields.waveletTypeChooser.setSelectedIndex(self.waveletTypeIndex)
		self.fields.waveletComponentMinField.setText(self.waveletMinComponent)
		self.fields.waveletComponentMaxField.setText(self.waveletMaxComponent)
		self.fields.waveletFilterWidthField.setText(self.waveletFilterWidth)
		self.fields.waveletPaddingBox.setSelectedIndex(self.waveletPaddingIndex)

		self.fields.zingerBox.setSelectedIndex(int(self.zingerIndex))            
		self.fields.zingerThresholdField.setText(self.threshold)				
		self.fields.zingerKernelWidthField.setText(self.kernelWidth)				                                

	   	self.fields.outputChooser.setSelectedIndex(self.outputFormatIndex)
		self.fields.minField.setText(self.minimum)				
		self.fields.maxField.setText(self.maximum)				

		self.fields.x1Field.setText(self.roiX1)				
		self.fields.x2Field.setText(self.roiX2)				
		self.fields.y1Field.setText(self.roiY1)				
		self.fields.y2Field.setText(self.roiY2)				

	   	self.fields.shiftingBox.setSelectedIndex(self.shiftingIndex)
	   	
		self.fields.axisBox.setSelectedIndex(self.axisBoxIndex)
	   	self.fields.overlapField.setText(self.realOverlap)
		self.fields.approachBox.setSelectedIndex(self.approachBoxIndex)

		self.fields.deltaField.setText(self.delta)				
		self.fields.betaField.setText(self.beta)				
		self.fields.distanceField.setText(self.distance)				
		self.fields.paganinPaddingBox.setSelectedIndex(self.paganinPaddingIndex)				
		self.fields.paganinStabilizerField.setText(self.stabilizer)				
		self.fields.paganinWidthField.setText(self.width)				
