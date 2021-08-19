class Fields():

    def __init__(self, GUI):
        
        # Create a panel for the Reconstruction settings
        self.recoSettingsPanel = GUI.createPanel(5, 175, 790, 540)
    
        # Create Reconstruction settings widgets
        self.recoSettingsLabel = GUI.createLabel("Reconstruction Settings", 10, 5, 300, 30, 2, 14, True)

        # Algorithm selection
        self.algorithmLabel = GUI.createLabel("Algorithm", 10, 35, 200, 30, 2, 12, True)
        # self.algorithmList=["Gridrec","FBP"]
        self.algorithmList=["Gridrec",]
        self.algorithmChooser = GUI.createComboBox(self.algorithmList, 200, 35, 110, 25, 0, 10, True)

        # filter
        self.filterLabel = GUI.createLabel("filter", 10, 65, 200, 30, 2, 12, True)
        self.filterList=["None","Shepp-Logan","Hanning","Hamming","Ramlak","Parzen","cosine","butterworth"]
        self.filterChooser = GUI.createComboBox(self.filterList, 200, 65, 110, 25, 0, 10, True)

        # Rotation center
        self.centerLabel = GUI.createLabel("Rotation center", 10, 95, 200, 30, 2, 12, True)
        self.centerField = GUI.createTextField(10, 200, 95, 110, 25, True,"1")
        
        # Remove Stripe Method
        self.stripe_methodLabel = GUI.createLabel("Remove Stripe Method", 10, 35, 200, 210, 2, 12, True)
        self.stripe_methodList=["none","fw","ti","sf","vo-all"]
        self.stripe_methodChooser = GUI.createComboBox(self.stripe_methodList, 200, 125, 110, 25, 0, 10, True)

        # Paganin
        phase_box_x = 400
        phase_box_y = 17
        self.energyLabel = GUI.createLabel("Energy", phase_box_x+90, phase_box_y-100, 200, 210, 2, 12, False)
        self.energyField = GUI.createTextField(10, phase_box_x+140, phase_box_y-5, 55, 25, False,"0")
        self.energyUnitsLabel = GUI.createLabel("keV", phase_box_x+200, phase_box_y-9, 200, 30, 2, 12, False)

        self.propagation_distanceLabel = GUI.createLabel("Propagation dist.", phase_box_x+15, phase_box_y-75, 200, 210, 2, 12, False)
        self.propagation_distanceField = GUI.createTextField(10, phase_box_x+140, phase_box_y+20, 55, 25, False,"0")
        self.propagation_distanceUnitsLabel = GUI.createLabel("mm", phase_box_x+200, phase_box_y+16, 200, 30, 2, 12, False)

        self.pixel_sizeLabel = GUI.createLabel("Pixel size", phase_box_x+70, phase_box_y-50, 200, 210, 2, 12, False)
        self.pixel_sizeField = GUI.createTextField(10, phase_box_x+140, phase_box_y+45, 55, 25, False,"0")
        self.pixel_sizeUnitsLabel = GUI.createLabel("microns", phase_box_x+200, phase_box_y+42, 200, 30, 2, 12, False)

        self.alphaLabel = GUI.createLabel("alpha", phase_box_x+95, phase_box_y-25, 200, 210, 2, 12, False)
        self.alphaField = GUI.createTextField(10, phase_box_x+140, phase_box_y+70, 55, 25, False,"0")

        # Paganin check box
        self.paganinBox = GUI.createCheckBox("Paganin", 310, 34, 90, 25, 10, True)

        # Slice number
        self.sliceLabel = GUI.createLabel("Slice Number", 250, 160, 200, 265, 2, 12, False)
        self.sliceField = GUI.createTextField(10, 360, 280, 100, 25, False,"0")

        # Center Search Width
        self.centerSearchLabel = GUI.createLabel("Center Search +/-",250, 330, 200, 30, 2, 12, False)
        self.centerSearchField = GUI.createTextField(8, 360, 334, 100, 25, False,"1")
        self.centerSearchUnitsLabel = GUI.createLabel("pixels", 460, 330, 200, 30, 2, 12, False)

        # nsino_x_chunk
        self.nsino_x_chunkLabel = GUI.createLabel("NsinoPerChunk", 250, 380, 200, 30, 2, 12, False)
        self.nsino_x_chunkField = GUI.createTextField(8, 360, 384, 100, 25, False,"1")
        
        # Queue selection
        self.queueLabel = GUI.createLabel("Queue", 30, 423, 48, 30, 2, 10, False)
        self.queueList=["local","LCRC","ALCF"]
        self.localButton = GUI.createRadioButton(self.queueList[0], 10, 445, 130, 20, True, 10, False)
        self.lcrcButton = GUI.createRadioButton(self.queueList[1], 10, 465, 130, 20, False, 10, False)
        self.alcfButton = GUI.createRadioButton(self.queueList[2], 10, 485, 130, 20, False, 10, False)

        # Nodes selection
        self.nnodeLabel = GUI.createLabel("Node #", 150, 465, 150, 30, 2, 10, False)
        # self.nnodeList = ["1","2","3","4","5","6","7","8"]
        self.nnodeList = [1, 2, 3, 4, 5, 6, 7, 8]
        self.nnodeChooser = GUI.createComboBox(self.nnodeList, 195, 468, 60, 25, 3, 10, False)

        # # Create a panel for the choosing a dataset
        self.chooseDatasetPanel = GUI.createPanel(5, 5, 790, 160)

        # Dataset panel
        self.datasetSelectionLabel = GUI.createLabel("Dataset", 10, 5, 200, 30, 2, 14, True)
        self.datasetSelectionButton = GUI.createButton("Select a dataset", 10, 50, 200, 40, 12, True)
        self.selectedDatasetField = GUI.createTextField(20, 210, 57, 350, 25, True,"")

        # Image size
        self.datasetImageSizeLabel = GUI.createLabel("Image size (h, v):", 565, 55, 200, 30, 2, 12, False)
        self.datasetHLabel = GUI.createLabel("", 690, 55, 200, 30, 2, 12, False)
        self.datasetVLabel = GUI.createLabel("", 740, 55, 200, 30, 2, 12, False)
 
        # Theta
        self.datasetThetaLabel = GUI.createLabel("Theta range:", 565, 75, 200, 30, 2, 12, False)
        self.datasetThetaStartLabel = GUI.createLabel("", 660, 75, 200, 30, 2, 12, False)
        self.datasetThetaEndLabel = GUI.createLabel("", 705, 75, 200, 30, 2, 12, False)
               
        # Expert box
        self.expertBox = GUI.createCheckBox("Expert", 725, 5, 60, 15, 8, True)

        # 360 box
        self.flipStichBox = GUI.createCheckBox("360", 625, 5, 60, 15, 8, True)

