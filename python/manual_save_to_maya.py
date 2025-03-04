import sys 
sys.path.insert(0, r"YOUR PATH HERE")

from importlib import reload

import maya_ui_template
import multi_file_sequence_render
import render_file

reload(maya_ui_template)
reload(multi_file_sequence_render)
reload(render_file)

tool = multi_file_sequence_render.MultiFileSequenceRender()

tool.run()

