import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore, QtGui, QtWidgets
from functools import partial # optional, for passing args during signal function calls
import sys
import pathlib
import os
import maya_ui_template
import render_file

class InitialWindow:
    
    table_file_selection = ""
    
    def file_select(self):
        file_paths = cmds.fileDialog2(fm = 4)
        print(file_paths)
        
        if file_paths is None:
            return
        
        for file_path in file_paths:
            file = render_file.RenderFile(file_path)
            self.table_file_selection.insertRow(0)
            new_file = QtWidgets.QTableWidgetItem(file.file_name)
            self.table_file_selection.setItem(0, 0, new_file)
     
    def set_up_buttons(self):
        
        btn_select_file = self.win.ui.findChild(QtWidgets.QPushButton, 'btn_select_file')
        btn_select_file.clicked.connect(self.file_select)
        self.table_file_selection = self.win.ui.findChild(QtWidgets.QTableWidget, 'table_file_selection')
        self.table_file_selection.setColumnCount(3)
        self.table_file_selection.setHorizontalHeaderLabels(["File", "First Frame", "Last Frame"])

    def run(self):
        
        path = pathlib.Path(__file__).parent.resolve()
        uiFilesPath = os.path.join(path, "..\\ui")
        self.win = maya_ui_template.Window(uiFilesPath + '\\MultiFileBatchRenderUi.ui')
        self.win.show()
        self.set_up_buttons()
        
        # win.setupButtons()
        