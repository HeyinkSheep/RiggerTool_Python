import importlib
import MayaUtils
from MayaUtils import MayaWindow


from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout
from PySide2.QtGui import QDoubleValidator
import maya.cmds as mc

class SpineRigger:
    def__init__(self):
        self.root = ""
        self.mid = ""
        self.end = ""
