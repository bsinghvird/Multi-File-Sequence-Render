Welcome to Multi File Sequence Render. A maya tool that lets you select multiple files, set frame ranges, load render settings, and then render out the sequences one after the other.
The tool was developed and tested with Maya 2024 on Windows. It may work on other verions/os, but it has not been tested there. 

There are two ways of running this tool

1. Drag "drag_into_maya.py" into your maya 3D viewport. The tool will then launch
2. If you wish to save this tool to your shelf, first select the shelf you want to save the tool to. Then double click the "generate_save_to_maya_file.bat" file. This will create a file called "save_to_maya.py" Open up the maya script editor, and then select File -> Open Script, and then File -> Save Script To Shelf. A window will open asking you to input a name for the shelf item. Enter whatever name you wish, hit ok and a button will be added to whichever shelf you currently have open.

If for whatever reason you are not able to run .bat files on your computer but still wish to save the tool to your shelf there is another option. In the python folder, there is the "manual_save_to_maya.py" file. On line 4 of this file there is a string that says "YOUR PATH HERE TO MULTI-FILE-SEQUENCE-RENDER FOLDER HERE". You must replace this text with the file path to where you downloaded and extracted the files for this tool. For example if I have it on my desktop it might look something like this:
path =  r"C:\Users\me\OneDrive\Desktop\Multi-File-Sequence-Render"
The lower case "r" before the string is necessary to avoid issues with file paths on windows. 


Other Info:
To export a render settings file, open up your render settings window then select Presets -> Export Render Settings. This will create a .json file which can then be loaded into the tool. The render settings in the file will then be applied to all files in the sequence. It will not override the frame range though.

Features for the future:
Extra error handling. There is some error handling on the input, but not all edge cases are accounted for yet. As long as you're not intentionally trying to break it or putting in invalid input like letters instead of numbers in the frame range you should be fine.
Force smooth mode toggle. An option to force smooth mode on for all meshes in the files 
