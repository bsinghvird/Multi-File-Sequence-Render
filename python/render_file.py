import maya.cmds as cmds


class RenderFile:
    file_path = ""
    file_name = ""
    first_frame = 0
    last_frame = 0
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.file_name = file_path.split('/')[-1]
    