
from PySide2.QtGui import QColor, QDoubleValidator
from PySide2.QtWidgets import QColorDialog, QHBoxLayout, QLabel, QLineEdit, QMainWindow,  QMessageBox, QPushButton, QSlider, QVBoxLayout, QWidget # This imports all the ui widgets we are using to set up the LimbRigger.
from PySide2.QtCore import Qt, Signal #Importing the QT core from Pyside to our Maya Plug in
from maya.OpenMaya import MVector 
import maya.OpenMayaUI as omui
import maya.cmds as mc
import maya.mel as mel
import shiboken2 



def GetMayaMainWindow() -> QMainWindow:
     mainWindow = omui.MQtUtil.mainWindow()
     return shiboken2.wrapInstance(int(mainWindow), QMainWindow)

def DeleteWidgetWithName(name):
     for widget in GetMayaMainWindow().findChildren(QWidget, name):
          widget.deleteLater()

class MayaWindow(QWidget):
     def __init__(self):
          super().__init__(parent = GetMayaMainWindow())
          DeleteWidgetWithName(self.GetWidgetUniqueName())
          self.setWindowFlags(Qt.WindowType.Window)
          self.setObjectName(self.GetWidgetUniqueName())

     def GetWidgetUniqueName(self):
          return "jklopoutuefadsfdhjkkjhgfdfghjkjhgfd"

class SpineRigger:
    def __init__(self):
        self.root=""
        self.afterRoot =""
        self.jnt = []
        self.SpineParts = 6
        self.controlerSize = 5

    def AutoFindJntBasedonSelection(self):
        self.jnts.clear()
        self.afterRoot = mc.listRelatives(self.root, c=True)[0]
        self.jnts.append(mc.listRelatives(self.afterRoot, c=True,type="joint"))
        spineParts = self.SpineParts - 2
        for x in range(spineParts):
            self.jnts.append(mc.listRelatives(self.jnts[x], c=True,type="joint")[0])
        print(self.root)
        print(self.afterRoot)
        print(self.jnts)

    def AutoRigSpineJntsCtrls(self):
        ctrlGrpName = "Spine_Grp"
        rootName = "ac_" + self.root
        afterRootName = "ac_" + self.afterRoot
        mc.circle(n=rootName, nr= (1,0,0), r = 20)
        mc.group(rootName, n = ctrlGrpName)
        mc.matchTransform(rootName,self.root)
        mc.orientConstraint(rootName,self.root)

        mc.circle(n=afterRootName, nr=(1,0,0), r=20)
        mc.parent(afterRootName,ctrlGrpName)
        mc.matchTransform(afterRootName,self.afterRoot)
        mc.orientConstraint(afterRootName,self.afterRoot)


        spinectrlsname = self.SpineCtrlsName - 1
        for x in range(spinectrlsname):
            ctrlGrpName = "ac_jnt_Spine_" + str(x + 2)
            mc.circle(n=ctrlGrpName, nr=(1,0,0), r=20)
            mc.group(spinectrlsname, n=ctrlGrpName)
            mc.matchTransform(spinectrlsname, self.jntName)
            mc.orientConstraint(spinectrlsname, self.jntName)
            return spinectrlsname, ctrlGrpName
        
class SpineRiggerWidget(QWidget):
     def __init__(self):
          super().__init__()
          self.rigger = SpineRigger()
          self.setWindowTitle("Spine Rigger")

          self.masterLayout = QVBoxLayout()
          self.setLayout(self.masterLayout) 

          toolTipLabel = QLabel('select the root of the spine then press the auto find button to create')
          self.masterLayout.addWidget(toolTipLabel)


          SetRootjntBtn = QPushButton(" Please select Root and Press here")
          self.masterLayout.addWidget(SetRootjntBtn)
          SetRootjntBtn.clicked.connect(self.SetRootJntBtnClicked)
          self.RootSelectionDisplay = QLabel()
          self.masterLayout.addWidget(self.RootSelectionDisplay)

          SpineJntName = QLabel("How may Spine Jnts to create")
          self.masterLayout.addWidget(SpineJntName)
          self.ctrlSize = QLineEdit()
          self.ctrlSize.setValidator(QDoubleValidator())
          self.ctrlSize.textChanged.connect(self.SetNumberOfSpineJntName)
          self.masterLayout.addWidget(self.ctrlSize)

          autoFindJntsBtn = QPushButton("Auto Find spine Jnts")
          self.masterLayout.addWidget(autoFindJntsBtn)
          autoFindJntsBtn.clicked.connect(self. AutoFindJntsBtnClicked)
          self.SpineSelectionDisplay = QLabel()
          self.masterLayout.addWidget(autoFindJntsBtn)

          AutoRigJntBtn = QPushButton("Rig Spine")
          self.masterLayout.addWidget(AutoRigJntBtn)
          AutoRigJntBtn.clicked.connect(self.AutoRigJntBtnClicked)

          self.adjustSize()
          self.SpineRigger = SpineRigger()

     def SetNumberOfSpineJntName(self, valStr:str):
           spinectrlsname = int(valStr)
           self.SpineRigger.spinectrlsname = spinectrlsname
           
     def AutoFindJntsBtnClicked(self):
                print("button")
                self.SpineRigger.AutoFindJntBasedonSelection()
                self.SpineSelectionDisplay.setText(f"{self.SpineRigger.afterRoot}, {self.SpineRigger.jnts}")

     def AutoRigJntBtnClicked(self):
                print("clicker")
                self.SpineRigger.AutoRigSpineJntsCtrls()
            
     def SetRootJntBtnClicked(self):
                self.SpineRigger.root = mc.ls(sl=True,type = "joint")[0]
                self.RootSelectionDisplay.setText(f"{self.SpineRigger.root}")



SpineRiggerWidget = SpineRiggerWidget()

SpineRiggerWidget.show()
