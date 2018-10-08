# BLINDRENAMER
Python version: 3.7.0

This is both a CLI application and a python module for blindly renaming files of a given extension in a directory retaining the ability to revert the renaming operation.
Currently, it can only rename files of one given extension at a time retaining the names relation of the last renaming operation run on the directory.

### Usage
#### As a python module
Simply import the renaming methods from the blindrenamer package
```python
from blindrenamer import renamingmethods

pathtofiles = "some/path/to/files"
ext = ".someextension"
result = renamingmethods.blindrename(pathtofiles, ext)

for oldname, newname in result.items():
    print("{oldname} was renamed to {newname}".format(oldname=oldname, newname=newname))

revertresult = renamingmethods.undolastrename(pathtofiles)

for names in revertresult["success"]:
    print("{name} was sucessfully reverted to its original name.")
```
#### As a CLI application
Run **main.py** in python interpreter and follow the instructions in the prompt.