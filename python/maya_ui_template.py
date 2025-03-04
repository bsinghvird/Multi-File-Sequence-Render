"""
Maya/QT UI template
Maya 2023
"""
# code for loading a ui file in maya taken from here:
# https://gist.github.com/gabrieljreed/b116cf246152a0da424fde3b9afcd633
from PySide2 import QtUiTools, QtCore, QtGui, QtWidgets
import sys

def get_maya_window():
    """Get the Maya main window as a QMainWindow instance."""
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(sys.argv)

    mayaWindow = next(w for w in app.topLevelWidgets() if w.objectName() == "MayaWindow")
    return mayaWindow
        
class Window:
    """A window that can be loaded from a Qt .ui file."""
    
    def __init__(self, file_path):
        """Initialize the window."""
        self.file_path = file_path
        self.main_window = None

    def load_ui_file(self, parent=None):
        """Load the UI file and return the widget."""
        if parent is None:
            parent = get_maya_window()
        loader = QtUiTools.QUiLoader()
        uiFile = QtCore.QFile(self.file_path)
        uiFile.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(uiFile, parent)
        
        uiFile.close()    
        return self.ui 

    def show(self, window_title):
        """Show the window."""
        self.close()
        
        app = QtWidgets.QApplication.instance()
        self.main_window = self.load_ui_file()
        self.main_window.setWindowTitle(window_title)
        self.main_window.show()
        app.exec_()
        return app

    def close(self):
        """Close the window."""
        if self.main_window is not None:
            self.main_window.close()
            self.main_window = None
   
