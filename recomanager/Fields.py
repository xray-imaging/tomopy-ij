class Fields():

	def __init__(self,GUI):
		
		# Create a panel for the Reconstruction settings
		self.recoSettingsPanel = GUI.createPanel(5,175,790,540)
	
		# Create Reconstruction settings widgets
		self.recoSettingsLabel = GUI.createLabel("Reconstruction Settings",10,5,300,30,2,14,True)

		# Filter
		self.cutOffLabel = GUI.createLabel("Cut-off frequency",310,155,130,30,2,10,True)
		self.cutOffField = GUI.createTextField(8,440,155,35,25,True,"0.5")
		self.filterLabel = GUI.createLabel("Filter",10,155,200,30,2,12,True)
		self.filterList=["None","Shepp-Logan","Hanning","Hamming","Ramp","Parzen","Lanczos","Dpc"]
		self.filterChooser = GUI.createComboBox(self.filterList,200,155,100,25,5,9,True)

		# Algorithm selection
		self.algoLabel = GUI.createLabel("Algorithm",10,35,200,30,2,12,True)
		self.algoList=["Gridrec","Paganin"]
		self.algoChooser = GUI.createComboBox(self.algoList,200,35,100,25,0,10,True)

		# Gridrec Padding
		self.gridrecLabel = GUI.createLabel("Gridrec Padding",10,35,200,210,2,12,True)
		self.gridrecList=["True","False"]
		self.gridrecChooser = GUI.createComboBox(self.gridrecList,200,125,100,25,0,10,True)

		# Remove Stripe Method
		self.stripeMethodLabel = GUI.createLabel("Remove Stripe Method",10,35,200,265,2,12,True)
		self.stripeMethodList=["none","fw","ti","sf","vo-all"]
		self.stripeMethodChooser = GUI.createComboBox(self.stripeMethodList,200,155,100,25,0,10,True)
		
		# fw-pad
		self.fwpadLabel = GUI.createLabel("fw-pad",10,35,200,320,2,12,True)
		self.fwpadList=["True","False"]
		self.fwpadChooser = GUI.createComboBox(self.fwpadList,200,185,100,25,0,10,True)
		
		self.getLastParametersButton = GUI.createButton("Get last parameters",250,10,150,20,8,True)
		
		# Branch selection
		self.branchLabel = GUI.createLabel("Branch",310,35,50,30,2,10,False)
		self.branchList=["master","devel"]
		self.masterButton = GUI.createRadioButton(self.branchList[0],365,40,70,20,True,10,False)
		self.develButton = GUI.createRadioButton(self.branchList[1],435,40,65,20,False,10,False)

		# Queue selection
		self.queueLabel = GUI.createLabel("QUEUE",690,400,50,30,2,10,False)
		self.queueList=["tomcat_NB.q","tomcat_old","tomcat_whole"]
		self.NBButton = GUI.createRadioButton(self.queueList[0],650,425,130,20,True,10,False)
		self.oldButton = GUI.createRadioButton(self.queueList[1],650,445,130,20,False,10,False)
		self.wholeButton = GUI.createRadioButton(self.queueList[2],650,465,130,20,False,10,False)

		# Nodes selection
		self.nnodeLabel = GUI.createLabel("NUMBER OF NODES",665,350,150,30,2,10,False)
#		self.nnodeList = ["1","2","3","4","5","6","7","8"]
		self.nnodeList = [1,2,3,4,5,6,7,8]
		self.nnodeChooser = GUI.createComboBox(self.nnodeList,685,375,45,25,3,10,False)

		# Rotation center
		self.centerLabel = GUI.createLabel("Rotation center",10,65,200,30,2,12,True)
		self.centerField = GUI.createTextField(8,200,65,100,25,True,"0")
		self.getRotationCenterButton = GUI.createButton("Get center",310,68,90,20,8,True)
		
		# Slice number
		self.sliceLabel = GUI.createLabel("Slice Number",10,95,200,30,2,12,True)
		self.sliceField = GUI.createTextField(8,200,95,100,25,True,"1")

		# Center Search Width
		self.searchWidthLabel = GUI.createLabel("Center Search Width",10,290,200,30,2,12,True)
		self.searchWidthField = GUI.createTextField(8,200,290,100,25,True,"1")

		# nsinoPerChunk
		self.nsinochunkLabel = GUI.createLabel("nsino-per-chunk",10,390,200,30,2,12,True)
		self.nsinochunkField = GUI.createTextField(8,200,390,100,25,True,"1")
		
		# Rotation
		self.rotLabel = GUI.createLabel("Rotation",10,125,200,30,2,12,True)
		self.rotField = GUI.createTextField(8,200,125,100,25,True,"0")
		
		# Zero padding
		self.zeroPaddingLabel = GUI.createLabel("Zero padding",10,185,200,30,2,12,True)
		self.zeroPaddingField = GUI.createTextField(8,200,185,100,25,True,"0.5")
		
		# Geometry
		self.geometryLabel = GUI.createLabel("Geometry",10,215,200,30,2,12,True)
		self.geometryList = ["Txt file provided","0-PI","0-2PI", "HDF5 file provided"]
		self.geometryBox = GUI.createComboBox(self.geometryList,200,215,100,25,1,8,True)
		
		# Zingers
		self.zingerThresholdLabel = GUI.createLabel("Threshold",310,245,70,30,2,10,False)
		self.zingerThresholdField = GUI.createTextField(8,380,245,50,25,False,"0.95")
		self.zingerKernelWidthLabel = GUI.createLabel("Kernel width",440,245,90,30,2,10,False)
		self.zingerKernelWidthField = GUI.createTextField(8,530,245,30,25,False,"5")
		self.zingerLabel = GUI.createLabel("Zinger removal",10,245,200,30,2,12,True)
		self.zingerList = ["Off","On"]
		self.zingerBox = GUI.createComboBox(self.zingerList,200,245,100,25,0,10,True)
		
		# Ring removal
		self.wslLabel = GUI.createLabel("Window size large",310,275,100,30,2,10,False)
		self.wslField = GUI.createTextField(8,420,275,30,25,False,"81")
		self.wssmLabel = GUI.createLabel("Wsindow size small/medium",460,275,180,30,2,10,False)
		self.wssmField = GUI.createTextField(8,630,275,30,25,False,"3.0")
		self.snrLabel = GUI.createLabel("SNR",680,275,50,30,2,10,False)
		self.snrField = GUI.createTextField(8,710,275,40,25,False,"0.3")
		self.wsLabel = GUI.createLabel("Window size",310,275,70,30,2,10,False)
		self.wsField = GUI.createTextField(8,400,275,30,25,False,"31")
		self.sarepyRef = GUI.createLabel("Vo et al. (2018)",10,290,100,30,2,9,False)
		self.muenchRef = GUI.createLabel("Muench et al. (2009)",10,290,100,30,2,9,False)
		self.waveletTypeLabel = GUI.createLabel("Wav. type",310,275,70,30,2,10,False)
		self.waveletTypeList=["db2","db3","db4","db5","db6","db7","db8","db9","db10","db11","db12","db13","db14","db15","db16","db17","db18","db19","db20"]
		self.waveletTypeChooser = GUI.createComboBox(self.waveletTypeList,380,275,60,25,13,10,False)
		self.waveletComponentMinLabel = GUI.createLabel("Min. comp.",450,275,70,30,2,10,False)
		self.waveletComponentMinField = GUI.createTextField(2,525,275,25,25,False,"0")
		self.waveletComponentMaxLabel = GUI.createLabel("Max. comp.",560,275,70,30,2,10,False)
		self.waveletComponentMaxField = GUI.createTextField(2,635,275,25,25,False,"4")
		self.waveletFilterWidthLabel = GUI.createLabel("Filter width",670,275,75,30,2,10,False)
		self.waveletFilterWidthField = GUI.createTextField(2,750,275,30,25,False,"1.0")
		self.waveletPaddingLabel = GUI.createLabel("Padding",670,245,75,30,2,10,False)
		self.paddingList = ["zpd","cpd","sym", "ppd","sp1"]
		self.waveletPaddingBox = GUI.createComboBox(self.paddingList,730,245,50,25,0,10,False)
		self.ringLabel = GUI.createLabel("Ring removal",10,275,200,30,2,12,True)
		self.ringList=["Off","Standard","Sarepy sorting","FFT/Wavelet","Sarepy all"]
		self.ringChooser = GUI.createComboBox(self.ringList,200,275,100,25,0,9,True)
		
		# Output
		self.minLabel = GUI.createLabel("Min.",310,305,30,30,2,10,False)
		self.minField = GUI.createTextField(8,345,305,85,25,False,"0")
		self.maxLabel = GUI.createLabel("Max.",440,305,30,30,2,10,False)
		self.maxField = GUI.createTextField(8,475,305,85,25,False,"0")
		self.getBothButton = GUI.createButton("Use both",580,305,95,26,9,False)
		self.applyBothButton = GUI.createButton("Apply both",685,305,97,26,9,False)
		self.outputLabel = GUI.createLabel("Output format",10,305,200,30,2,12,True)		
		self.outputList=["DMP","TIFF8","TIFF16"]
		self.outputChooser = GUI.createComboBox(self.outputList,200,305,100,25,1,10,True)

		# ROI
		self.roiLabel = GUI.createLabel("ROI",10,335,30,30,2,12,True)
		self.setRoiButton = GUI.createButton("Set",50,340,60,20,10,True)
		self.doneRoiButton = GUI.createButton("Update",115,340,80,20,10,True)
		self.x1Label = GUI.createLabel ("X1",205,335,30,30,2,12,True)
		self.x1Field = GUI.createTextField(4,235,335,45,25,True,"0")
		self.y1Label = GUI.createLabel ("Y1",295,335,30,30,2,12,True)
		self.y1Field = GUI.createTextField(4,325,335,45,25,True,"0")
		self.x2Label = GUI.createLabel ("X2",385,335,30,30,2,12,True)
		self.x2Field = GUI.createTextField(4,415,335,45,25,True,"0")
		self.y2Label = GUI.createLabel ("Y2",475,335,30,30,2,12,True)
		self.y2Field = GUI.createTextField(4,505,335,45,25,True,"0")
		self.resetRoiButton = GUI.createButton("Reset",570,340,75,20,10,True)
	
		# Block
		self.blockLabel = GUI.createLabel("Block",10,365,50,30,2,12,True)
		
		# Shifting
		self.shiftingLabel = GUI.createLabel("Projection rotation",10,395,200,30,2,12,True)
		self.shiftingList = ["Off","On"]
		self.shiftingBox = GUI.createComboBox(self.shiftingList,200,395,100,25,0,10,True)
	
		# Postfix
		self.postfixLabel = GUI.createLabel("Postfix",10,425,200,30,2,12,True)
		self.postfixField = GUI.createTextField(8,200,425,300,25,True,"")

		# Create a panel for the choosing a dataset
		self.chooseDatasetPanel = GUI.createPanel(5,5,790,160)

		# Dataset panel
		self.datasetSelectionLabel = GUI.createLabel("Dataset",10,5,200,30,2,14,True)
		self.datasetSelectionButton = GUI.createButton("Select a dataset",10,50,200,40,12,True)
		self.selectedDatasetField = GUI.createTextField(20,250,57,200,25,True,"")
		
		# 360
		self.threeSixtyLabel = GUI.createLabel("360 degree scan",570,30,200,25,2,12,False)
		self.approachLabel = GUI.createLabel("Approach",460,45,200,30,2,12,False)
		self.approachList = ["New","Old"]
		self.approachBox = GUI.createComboBox(self.approachList,535,55,70,30,0,12,False)
		self.axisLabel = GUI.createLabel("Axis location",620,55,200,30,2,12,False)
		self.axisList = ["Right","Left"]
		self.axisBox = GUI.createComboBox(self.axisList,715,55,70,30,0,12,False)
		self.overlapLabel = GUI.createLabel("Projection overlap",665,95,200,25,2,10,False)
		self.overlapField = GUI.createTextField(8,681,120,60,20,False,"")
		self.cleanButton = GUI.createButton("Clean",462,73,60,15,8,False)
		
		# Absorption sinograms
		self.sinogramCalculationLabel = GUI.createLabel("Sinograms",10,152,100,30,2,12,False)
		self.sinogramCalculationButton = GUI.createButton("Compute",120,155,100,25,12,False)
		
		# Paganin
		self.paganinCalculationLabel = GUI.createLabel("Paganin",10,192,100,30,2,12,False)
		self.deltaLabel = GUI.createLabel("Delta",120,193,50,30,2,10,False)
		self.deltaField = GUI.createTextField(8,170,195,55,25,False,"")
		self.betaLabel = GUI.createLabel("Beta",240,193,50,30,2,10,False)
		self.betaField = GUI.createTextField(8,290,195,55,25,False,"")
		self.distanceLabel = GUI.createLabel("Distance (mm)",360,193,90,30,2,10,False)
		self.distanceField = GUI.createTextField(8,460,195,55,25,False,"")
		self.paganinCalculationButton = GUI.createButton("Compute",540,195,100,25,12,False)
		self.paganinPaddingLabel = GUI.createLabel("Padding",652,175,90,30,2,10,False)
		self.paganinPaddingList = ["Standard","Extended"]
		self.paganinPaddingBox = GUI.createComboBox(self.paganinPaddingList,707,180,80,18,0,9,False)
		self.paganinDeconvolutionLabel = GUI.createLabel("Deconvol.",652,205,90,30,2,10,False)
		self.paganinStabilizerLabel = GUI.createLabel("Stabilizer",707,197,90,30,2,9,False)
		self.paganinStabilizerField = GUI.createTextField(5,752,200,35,18,False,"")
		self.paganinWidthLabel = GUI.createLabel("Width",707,212,90,30,2,9,False)
		self.paganinWidthField = GUI.createTextField(5,752,219,35,18,False,"")
		
		# Expert box
		self.expertBox = GUI.createCheckBox("Expert",725,5,60,15,8,True)


