from ui import UI
from renamingmethods import blindrename, undolastrename
from configs import __email__

def main(*args,**kwargs)->None:
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

if __name__ == "__main__":
    main()