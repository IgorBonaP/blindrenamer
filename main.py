import configparser
import argparse

from ui import UI
from renamingmethods import blindrename, undolastrename
from configs import __email__

def main(*args,**kwargs)->None:
    configfile = kwargs.get("configfile")
    if configfile:
        return useconfig(configfile)

    ui = UI()
    operation = None
    dirset = False
    paramset = False
    parameters = {
        1:ui.inputext,
        2:ui.namestableoption,
        3:ui.paramsummary
    }
    i = 1
    while not operation:
        operation = ui.operationselector()
    
    while not dirset:
        if ui.inputdir():
            dirset = True

    if operation == "undolastrename":
        try:
            undolastrename(ui.directory)
        except (FileNotFoundError, PermissionError):
            print("## Could not access names table, either non existent or protected.\n\n")
        else:
            print("## Original names were restored.\n")
        finally:
            input("Press ENTER to finish.")
            return

    while not paramset:
        if parameters[i]():
            i += 1
        
        if i == 3:
            parameters[i]()
            try:
                if blindrename(ui.directory, ui.ext, ui.save):
                    print("## Files renamed successfully.")
                else:
                    print("## No files were renamed. Check directory and extension and rerun the program.")
            except:
                print("An unespected error has occurred. Please contact:{email}".format(email=__email__))
            finally:
                input("Press ENTER to finish.")
                return

def useconfig(inifilepath: str)->None:
    cfg = configparser.ConfigParser()
    try:
        cfg.read(inifilepath)
        directory = cfg.get("ALL", "directory")
        ext = cfg.get("ALL", "ext")
        save = cfg.getboolean("ALL", "save", fallback=True)

        if blindrename(directory, ext, save):
            input("Files renamed. Press Enter to finish.")
    except Exception as e:
        print(e.args[1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ini", help="This is the path to the .ini file with blindrenamer configs.", type=str)
    args = parser.parse_args()
    
    if args.ini:
        main(configfile=args.ini)
    else:
        main()