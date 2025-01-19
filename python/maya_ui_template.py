"""
Maya/QT UI template
Maya 2023
"""

import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore, QtGui, QtWidgets
from functools import partial # optional, for passing args during signal function calls
import sys
import pathlib
import os

def getMayaWindow():
    """Get the Maya main window as a QMainWindow instance."""
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    mayaWindow = next(w for w in app.topLevelWidgets() if w.objectName() == "MayaWindow")
    return mayaWindow
        
class Window:
    """A window that can be loaded from a Qt .ui file."""
    
    def __init__(self, filePath):
        """Initialize the window."""
        self.filePath = filePath
        self.MainWindow = None
        # self.ui = self.loadUIFile()

    def loadUIFile(self, parent=None):
        """Load the UI file and return the widget."""
        if parent is None:
            parent = getMayaWindow()
        loader = QtUiTools.QUiLoader()
        uiFile = QtCore.QFile(self.filePath)
        uiFile.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(uiFile, parent)
        
        uiFile.close()    
        return self.ui 

    def show(self):
        """Show the window."""
        self.close()
        app = QtWidgets.QApplication.instance()
        self.MainWindow = self.loadUIFile()
        self.MainWindow.setWindowTitle('Mutli File Batch Render')
        self.MainWindow.show()
        app.exec_()
        return app

    def close(self):
        """Close the window."""
        if self.MainWindow is not None:
            self.MainWindow.close()
            self.MainWindow = None
   

# if __name__ == "__main__":
#     """This is the entry point of the script. Create an instance of the Window class and show it."""
#     win = Window('E:\\code\\mayaTools\\testTool\\ui\\sampleUi.ui')
#     win.show()
