import maya.cmds as cmds
import maya.mel as mel
from maya import OpenMayaUI as omui
from shiboken2 import wrapInstance
from PySide2 import QtUiTools, QtCore, QtGui, QtWidgets
from functools import partial # optional, for passing args during signal function calls
import sys
import pathlib
import os
from python import maya_ui_template
from python import render_file
import maya.app.renderSetup.views.renderSetupPreferences as prefs 

class MultiFileSequenceRender:
    
    table_file_selection = ""
    text_render_settings_file = ""
    render_setttings_file_path = None
    text_save_location = None
    text_info_messages = None
    default_render_settings_message = "None (Use render settings saved in each file)"
    checkbox_force_smooth = None
       
    def get_first_and_last_frame_from_ma_file(self, file_path):
        
        first_frame = None
        last_frame = None
        
        filename, file_extension = os.path.splitext(file_path)
        
        if (file_extension != '.ma'):
            return first_frame, last_frame      
        
        
        with open(file_path) as file:
            render_settings_found = False
                
            for line in file:
                    
                if ("select -ne :defaultRenderGlobals;" in line):
                    render_settings_found = True
                    continue
                
                if(render_settings_found):
                    if 'setAttr \".fs\"' in line:           
                        first_frame = line.split(" ")[-1].replace(";", "")
                        
                    elif 'setAttr \".ef\"' in line:            
                        last_frame = line.split(" ")[-1].replace(";", "") 
                                
                    elif 'setAttr' in line or 'addAttr' in line:
                        continue
                    else:
                        break 
                        
        return first_frame, last_frame
    
    def file_select(self):
        file_type_filter = "Maya Files (*.ma *.mb);;Maya ASCII (*.ma);;Maya Binary (*.mb);;"
        file_paths = cmds.fileDialog2(fileFilter=file_type_filter, dialogStyle=2,fm = 4, caption = "Select File(s)",okc = "Select File(s)")
        
        if file_paths is None:
            return
        
        for file_path in file_paths:
                        
            first_frame, last_frame = self.get_first_and_last_frame_from_ma_file(file_path)
                        
            file = render_file.RenderFile(file_path)
            self.table_file_selection.insertRow(0)
            new_file_name = QtWidgets.QTableWidgetItem(file.file_name)
            new_file_path = QtWidgets.QTableWidgetItem(file.file_path)
            new_first_frame = QtWidgets.QTableWidgetItem(first_frame)
            new_last_frame = QtWidgets.QTableWidgetItem(last_frame)
            self.table_file_selection.setItem(0, 0, new_file_name)
            self.table_file_selection.setItem(0, 1, new_first_frame)
            self.table_file_selection.setItem(0, 2, new_last_frame)
            self.table_file_selection.setItem(0, 3, new_file_path)
    
    def smooth_all_geometry(self):
        cmds.select(allDagObjects = True)
        all_objects = cmds.ls(selection = True)

        for object in all_objects:
            cmds.displaySmoothness(object, divisionsU=3, divisionsV=3, pointsWire=16, pointsShaded=4, polygonObject=3)
    
    def sequence_render_file(self, file_path, first_frame, last_frame, use_custom_frame_range):
        
        self.text_info_messages.append("----------------------------------------------------\n")
        
        try:
            
            self.text_info_messages.append(f"Opening \"{file_path}\"\n")
        
            cmds.file(file_path, open = True, force = True)
            
            if (self.render_setttings_file_path is not None):

                self.text_info_messages.append(f"Applying render settings from \"{self.render_setttings_file_path}\"\n")
                prefs.loadUserPreset(self.render_setttings_file_path.replace(".json", ""))
            
            cmds.workspace(fileRule=['images',self.text_save_location.toPlainText()])

            mel.eval('setMayaSoftwareFrameExt("3", 0)')
            
            if (use_custom_frame_range):
            
                cmds.setAttr("defaultRenderGlobals.startFrame", first_frame)
                cmds.setAttr("defaultRenderGlobals.endFrame", last_frame)
                
            if(self.checkbox_force_smooth.isChecked()):
                self.smooth_all_geometry()
                
            self.text_info_messages.append(f"Starting \"{file_path}\" render\n")
                
            mel.eval('renderSequence')
            
            self.text_info_messages.append(f"Finished \"{file_path}\" render\n")
        
        except Exception as e:
            
            self.text_info_messages.append(f"!!!!!!!ERROR!!!!!!! RENDER OF \"{file_path}\" DID NOT COMPLETE !!!!!!!ERROR!!!!!!!\n")
            self.text_info_messages.append(f"Error: {e}\n")
        
        self.text_info_messages.append("----------------------------------------------------\n")
        
    def input_is_valid(self):
              
        input_is_valid = True
        error_message = "Error:\n"

        self.text_info_messages.clear()
              
        if (self.text_save_location.toPlainText() == ""):
            error_message += "Save Location Not Selected\n"
            # self.text_save_location.setTextBackgroundColor(QtGui.QColor(150,100,100))
            input_is_valid = False
              
        num_rows = self.table_file_selection.rowCount()
        
        for index in range(num_rows):
            display_row_number = index+1
            first_frame = self.table_file_selection.item(index, 1).text().replace(" ", "")
            last_frame = self.table_file_selection.item(index, 2).text().replace(" ", "")
            
            self.table_file_selection.item(index, 1).setBackground(QtCore.Qt.BrushStyle.NoBrush)
            self.table_file_selection.item(index, 2).setBackground(QtCore.Qt.BrushStyle.NoBrush)

            if (((first_frame == "")) ^ ((last_frame == ""))):
                error_message += f"Invalid frame range in row {display_row_number}: both must be filled or empty\n"
                self.table_file_selection.item(index, 1).setBackground(QtGui.QColor(150,100,100))
                self.table_file_selection.item(index, 2).setBackground(QtGui.QColor(150,100,100))
                input_is_valid = False
            
            if (((first_frame == "")) and ((last_frame == ""))):
                continue
                        
            if( int(first_frame) > int(last_frame)):
                error_message += f"Invalid frame range in row {display_row_number}: last frame must be after first frame\n"
                self.table_file_selection.item(index, 2).setBackground(QtGui.QColor(150,100,100))
                input_is_valid = False
                      
        
        if(input_is_valid):
            return True
        else:
            self.text_info_messages.setText(error_message)
            return False   
                
    def sequence_render_all_files(self):
       
        if (not self.input_is_valid()):
            return
       
        num_rows = self.table_file_selection.rowCount()
        
        for index in range(num_rows):
          
            self.text_info_messages.append(f"File {index+1}/{num_rows}\n")
            
            file_path = self.table_file_selection.item(index, 3).text()
            first_frame = self.table_file_selection.item(index, 1).text().replace(" ", "")
            last_frame = self.table_file_selection.item(index, 2).text().replace(" ", "")
            use_custom_frame_range = False
            if((first_frame != "") and (last_frame != "")):
                first_frame = int(first_frame)
                last_frame = int(last_frame)
                
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
    
    
    def render_settings_button(self):
        
        if (self.render_setttings_file_path is None):
            self.import_render_settings_file()
        else:
            self.remove_render_settings_file()
                
    def remove_render_settings_file(self):
        self.text_render_settings_file.setText(self.default_render_settings_message)
        self.render_setttings_file_path = None
        self.btn_render_settings.setText("Import Render Settings File")
        
    
    def import_render_settings_file(self):
        
        file_type_filter = "JSON (*.json);;"
        file_paths = cmds.fileDialog2(fileFilter=file_type_filter, dialogStyle=2,fm = 1, caption = "Select Render Settings File",okc = "Select Render Settings File")
        
        if file_paths is None:
            return
         
        self.render_setttings_file_path = file_paths[0]
        filename = os.path.basename(self.render_setttings_file_path)
        self.text_render_settings_file.setText(filename)
        self.btn_render_settings.setText("Use Render Settings Saved in Each File")
        
    
    def select_save_location(self):
        folder_path = cmds.fileDialog2(dialogStyle=2,fm = 2, caption = "Select Folder",okc = "Select Folder")
        
        if folder_path is None:
            return
        
        self.text_save_location.setText(folder_path[0])
        
    def set_up_widgets(self):
        
        btn_select_files = self.tool.ui.findChild(QtWidgets.QPushButton, 'btn_select_files')
        btn_remove_selected_files = self.tool.ui.findChild(QtWidgets.QPushButton, 'btn_remove_selected_files')
        btn_cancel =  self.tool.ui.findChild(QtWidgets.QPushButton, 'btn_cancel')
        btn_render = self.tool.ui.findChild(QtWidgets.QPushButton, 'btn_render')
        btn_select_save_location = self.tool.ui.findChild(QtWidgets.QPushButton, 'btn_select_save_location')
        self.btn_render_settings = self.tool.ui.findChild(QtWidgets.QPushButton, 'btn_render_settings')
        
        btn_select_files.clicked.connect(self.file_select)
        btn_remove_selected_files.clicked.connect(self.remove_selected_files)
        btn_cancel.clicked.connect(self.tool.close)
        btn_render.clicked.connect(self.sequence_render_all_files)
        btn_select_save_location.clicked.connect(self.select_save_location)
        self.btn_render_settings.clicked.connect(self.render_settings_button)
        
        self.table_file_selection = self.tool.ui.findChild(QtWidgets.QTableWidget, 'table_file_selection')
        
        self.text_render_settings_file = self.tool.ui.findChild(QtWidgets.QTextEdit, 'text_render_settings_file')
        self.text_save_location = self.tool.ui.findChild(QtWidgets.QTextEdit, 'text_save_location')
        self.text_info_messages = self.tool.ui.findChild(QtWidgets.QTextBrowser, 'text_info_messages')
        
        self.checkbox_force_smooth = self.tool.ui.findChild(QtWidgets.QCheckBox, 'checkbox_force_smooth')

    def run(self):
           
        path = pathlib.Path(__file__).parent.resolve()
        uiFilesPath = os.path.join(path, "..\\ui")
        self.tool = maya_ui_template.Window(uiFilesPath + '\\MultiFileSequenceRenderUi.ui')
        self.tool.show("Multi File Sequence Render")
        self.set_up_widgets()
        