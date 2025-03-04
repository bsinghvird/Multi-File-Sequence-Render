
echo import pathlib > save_to_maya.py
echo import sys >> save_to_maya.py
echo import os >> save_to_maya.py

echo path = r"%~dp0\" >> save_to_maya.py
echo sys.path.insert(1, path) >> save_to_maya.py

echo from importlib import reload >> save_to_maya.py
echo from python import maya_ui_template >> save_to_maya.py
echo from python import multi_file_sequence_render >> save_to_maya.py
echo from python import render_file >> save_to_maya.py

echo reload(maya_ui_template) >> save_to_maya.py
echo reload(multi_file_sequence_render) >> save_to_maya.py
echo reload(render_file) >> save_to_maya.py

echo tool = multi_file_sequence_render.MultiFileSequenceRender() >> save_to_maya.py

echo tool.run() >> save_to_maya.py


