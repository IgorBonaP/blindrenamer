import os
from stringutils import randomstring
from configs import SAVEDICTNAME
from exceptions import (TargetExtensionError,
                        ExhaustedNamesError)
from files_iter import get_file_iterator

def serialrename(basename: str, pathstring: str, ext: str, subtree:bool, savedict=False)->dict:
    '''Renames files of a given extension in a directory using title as the base filename followed by a serial number.
    By default it returns a dict with keys being the original names and values being the new
    names if successful.
    ext = file extension to be affected
    If savedict is set to True a names_table tabseparated file is saved with the names relation is saved in
    patstring directory.'''
    renamingdict = {}
    for count, f in enumerate(get_file_iterator(pathstring, subtree, ext=ext)):
        newname = f.parent.joinpath(f"{basename}_{count}{ext}")
        os.rename(str(f), newname)
        renamingdict.update({f.name: newname.name})
    if savedict and renamingdict:
        write_names_relation_table(pathstring, renamingdict)
    return renamingdict


def blindrename(pathstring: str, ext: str, savedict=False)-> dict:
    '''Blindly renames files of a given extension in a directory to a 4 random letters string. By default it
    returns a dict with keys being the original names and values being the new
    names if successful.
    ext = file extension to be affected
    If savedict is set to True a names_table tabseparated file is saved with the names relation is saved in
    patstring directory.'''
    if not isinstance(ext, str) or not ext.strip() or not ext.startswith("."):
        raise TargetExtensionError(
            "Extension should be a non empty string starting with a colon.")
    directory = os.listdir(pathstring)
    possiblenames = 7311616  # Possible 4 letter names taking into account total ascii_letters
    renamingdict = {}
    for f in directory:
        if not f.endswith(ext):
            continue
        srcpath = os.path.join(pathstring, f)
        renameattempts = 0
        while True:
            renameattempts += 1
            if renameattempts > possiblenames:
                raise ExhaustedNamesError(
                    "Exhausted possible random names. Please retry with higher name length")
            randomname = randomstring(4)
            newname = "{name}{ext}".format(name=randomname, ext=ext)
            dst = os.path.join(pathstring, newname)
            nameisok = not os.path.isfile(dst)
            if nameisok:
                os.rename(srcpath, dst)
                renamingdict.update(
                    {f: "{newname}{ext}".format(newname=randomname, ext=ext)})
                break

    if savedict and renamingdict:
        write_names_relation_table(pathstring, renamingdict)

    return renamingdict

def write_names_relation_table(pathstring:str, renamingdict:dict):
    '''
    Writes a txt file with the name relation contained in the renaming dict.
    '''
    dictfile = os.path.join(pathstring, SAVEDICTNAME)
    with open(dictfile, "w") as names_table:
        names_table.write("OLD NAME\tNEW NAME\n")
        for old_name, new_name in renamingdict.items():
            names_table.write("{old}\t{new}\n".format(
                old=old_name, new=new_name))

def undolastrename(pathstring: str)-> dict:
    '''Restore original name of files in pathstring directory according to names table in
    pathtosavedict path.
    Returns a dict with  keys containing lists of file names with the following structure:
        success-> names of renamed files
        notfound-> names of not found files
        conflict-> names of files whose original names were already present in the directory
        or being used by another process
    If savedict isn't a tsv or is missing a value IndexError will be raised.
    It assumes savedict first line is a header.'''

    if not os.path.isdir(pathstring):
        raise FileNotFoundError("{pathstring} is an invalid directory or does not exists".format(pathstring=pathstring))

    pathtosavedict = os.path.join(pathstring, SAVEDICTNAME)

    with open(pathtosavedict, "r") as namesdict:
        next(namesdict)
        result = {
            "success":[],
            "notfound": [],
            "conflict": []
        }
        for l in namesdict:
            names = l[:-1].split("\t")
            try:
                originalname = os.path.join(pathstring, names[0].trim())
                actualname = os.path.join(pathstring, names[1].trim())
                os.rename(actualname, originalname)
            except (FileExistsError, PermissionError):
                result["conflict"].append(originalname)
                continue
            except FileNotFoundError:
                result["notfound"].append(actualname)
                continue
            else:
                result["success"].append(actualname)
    try:
        os.remove(pathtosavedict)
    except PermissionError:
        print(">{scriptname} Notice: Couldn't delete names table, permission denied".format(scriptname=__name__))

        return result

if __name__ == "__main__":
    from stringutils import randomstring
    files = r"test"
    basename = randomstring(4)
    ext = ".txt"
    subtree = False
    result = serialrename(basename, files, ".txt", subtree, savedict=True)
    print(result)
