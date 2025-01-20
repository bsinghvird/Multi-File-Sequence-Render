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

class MultiFileSequenceRender:
    
    table_file_selection = ""
    
    def file_select(self):
        file_paths = cmds.fileDialog2(fm = 4)
        print(file_paths)
        
        if file_paths is None:
            return
        
        for file_path in file_paths:
            file = render_file.RenderFile(file_path)
            self.table_file_selection.insertRow(0)
            new_file_name = QtWidgets.QTableWidgetItem(file.file_name)
            new_file_path = QtWidgets.QTableWidgetItem(file.file_path)
            self.table_file_selection.setItem(0, 0, new_file_name)
            self.table_file_selection.setItem(0, 3, new_file_path)
        
    def remove_selected_files(self):
        selected_rows = self.table_file_selection.selectedItems()
        print(selected_rows)    
    
     
    def set_up_buttons(self):
        
        btn_select_files = self.tool.ui.findChild(QtWidgets.QPushButton, 'btn_select_files')
        btn_remove_selected_files = self.tool.ui.findChild(QtWidgets.QPushButton, 'btn_remove_selected_files')
        
        btn_select_files.clicked.connect(self.file_select)
        btn_remove_selected_files.clicked.connect(self.remove_selected_files)
        
        self.table_file_selection = self.tool.ui.findChild(QtWidgets.QTableWidget, 'table_file_selection')
        self.table_file_selection.setColumnCount(4)
        self.table_file_selection.setHorizontalHeaderLabels(["File Name", "First Frame", "Last Frame", "File Path"])

    def run(self):
           
        path = pathlib.Path(__file__).parent.resolve()
        uiFilesPath = os.path.join(path, "..\\ui")
        self.tool = maya_ui_template.Window(uiFilesPath + '\\MultiFileBatchRenderUi.ui')
        self.tool.show()
        self.set_up_buttons()
        