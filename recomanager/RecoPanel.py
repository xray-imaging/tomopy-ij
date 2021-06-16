from javax.swing import JLabel, JPanel, JTextField, JComboBox, JButton, JRadioButton, JCheckBox
from java.awt.event import ActionListener
from java.awt import Font, Color

class RecoPanel:

    def __init__(self):
        pass

    def createPanel(self,xlocation,ylocation,xsize,ysize):
        self = JPanel()
        self.setLayout(None)
        self.setBackground(Color.lightGray)
        self.setLocation(xlocation,ylocation)
        self.setSize(xsize,ysize)
        return self

    def createLabel(self,name,xlocation,ylocation,xsize,ysize,halignment,fontSize,visibility):
        self = JLabel(name)
        self.setLocation(xlocation,ylocation)
        self.setSize(xsize,ysize)
        self.setHorizontalAlignment(halignment)
        self.setFont(Font("Dialog",Font.BOLD,fontSize))
        self.setVisible(visibility)
        return self

    def createTextField(self,fontSize,xlocation,ylocation,xsize,ysize,visibility,text):
        self = JTextField(fontSize)
        self.setLocation(xlocation,ylocation)
        self.setSize(xsize,ysize)
        self.setVisible(visibility)
        self.setText(text)
        return self

    def createComboBox(self,itemList,xlocation,ylocation,xsize,ysize,index,fontSize,visibility):
        self = JComboBox(itemList)
        self.setSelectedIndex(index)
        self.setFont(Font("Dialog",Font.BOLD,fontSize))
        self.setLocation(xlocation,ylocation)
        self.setSize(xsize,ysize)
        self.setVisible(visibility)
        return self

    def createButton(self,name,xlocation,ylocation,xsize,ysize,fontSize,visibility):
        self = JButton(name)
        self.setLocation(xlocation,ylocation)
        self.setSize(xsize,ysize)
        self.setFont(Font("Dialog",Font.BOLD,fontSize))
        self.setVisible(visibility)
        return self

    def createRadioButton(self,itemList,xlocation,ylocation,xsize,ysize,selection,fontSize,visibility):
        self = JRadioButton(itemList)
        self.setFont(Font("Dialog",Font.BOLD,fontSize))
        self.setLocation(xlocation,ylocation)
        self.setSize(xsize,ysize)
        self.setSelected(selection)
        self.setVisible(visibility)
        return self

    def createCheckBox(self,boxName,xlocation,ylocation,xsize,ysize,fontSize,visibility):
        self = JCheckBox(boxName)
        self.setFont(Font("Dialog",Font.BOLD,fontSize))
        self.setLocation(xlocation,ylocation)
        self.setSize(xsize,ysize)
        self.setVisible(visibility)
        return self
