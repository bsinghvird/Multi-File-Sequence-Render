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
    
    def sequence_render_file(self, file_path, first_frame, last_frame, use_custom_frame_range):
        
        cmds.file(file_path, open = True, force = True)
        mel.eval('setMayaSoftwareFrameExt("3", 0)')
        cmds.setAttr('defaultArnoldDriver.ai_translator', 'png', type='string')
        cmds.setAttr("defaultResolution.width", 1280)
        cmds.setAttr("defaultResolution.width", 720)

        
        if (use_custom_frame_range):
        
            cmds.setAttr("defaultRenderGlobals.startFrame", first_frame)
            cmds.setAttr("defaultRenderGlobals.endFrame", last_frame)
            
            
        mel.eval('renderSequence')
                
    def sequence_render_all_files(self):
       
        num_rows = self.table_file_selection.rowCount()
        
        for index in range(num_rows):
            file_path = self.table_file_selection.item(index, 3).text()
            first_frame = -1
            last_frame = -1
            use_custom_frame_range = False
            if((self.table_file_selection.item(index, 1) is not None) & (self.table_file_selection.item(index, 2) is not None)):
                first_frame = self.table_file_selection.item(index, 1).text()
                last_frame = self.table_file_selection.item(index, 2).text()
                use_custom_frame_range = True
                        
            self.sequence_render_file(file_path, first_frame, last_frame, use_custom_frame_range)

        for index in range(num_rows):
            self.table_file_selection.removeRow(0)
                
    
    def remove_selected_files(self):     
        selected_rows = self.table_file_selection.selectionModel().selectedRows()
        
        row_indexes = []
        
        for selected_row in selected_rows:
            row_indexes.append(selected_row.row())
        
        row_indexes.sort(reverse=True)

        for row_index in row_indexes:
            self.table_file_selection.removeRow(row_index)        
        

    def set_up_buttons(self):
        
        btn_select_files = self.tool.ui.findChild(QtWidgets.QPushButton, 'btn_select_files')
        btn_remove_selected_files = self.tool.ui.findChild(QtWidgets.QPushButton, 'btn_remove_selected_files')
        btn_cancel =  self.tool.ui.findChild(QtWidgets.QPushButton, 'btn_cancel')
        btn_render = self.tool.ui.findChild(QtWidgets.QPushButton, 'btn_render')
        
        btn_select_files.clicked.connect(self.file_select)
        btn_remove_selected_files.clicked.connect(self.remove_selected_files)
        btn_cancel.clicked.connect(self.tool.close)
        btn_render.clicked.connect(self.sequence_render_all_files)
        
        self.table_file_selection = self.tool.ui.findChild(QtWidgets.QTableWidget, 'table_file_selection')


    def run(self):
           
        path = pathlib.Path(__file__).parent.resolve()
        uiFilesPath = os.path.join(path, "..\\ui")
        self.tool = maya_ui_template.Window(uiFilesPath + '\\MultiFileSequenceRenderUi.ui')
        self.tool.show()
        self.set_up_buttons()
        