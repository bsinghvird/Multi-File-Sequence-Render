
import sys 
sys.path.insert(0, "E:\code\mayaTools\Multi-File-Batch-Render\python")

from importlib import reload

import maya_ui_template
import multi_file_batch_render
import render_file as render_file

reload(maya_ui_template)
reload(multi_file_batch_render)
reload(render_file)


a = multi_file_batch_render.InitialWindow()

a.run()

