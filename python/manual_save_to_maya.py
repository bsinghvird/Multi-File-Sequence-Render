import sys 
sys.path.insert(0, r"YOUR PATH HERE TO MULTI-FILE-SEQUENCE-RENDER FOLDER HERE")

from importlib import reload

from python import maya_ui_template
from python import multi_file_sequence_render
from python import render_file

reload(maya_ui_template)
reload(multi_file_sequence_render)
reload(render_file)

tool = multi_file_sequence_render.MultiFileSequenceRender()

tool.run()

