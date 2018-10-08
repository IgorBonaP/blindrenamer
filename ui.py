import os
from renamingmethods import blindrename
from sys import stdin
from configs import __version__, __author__, __email__

class UI():

    def __init__(self):
        
        self.directory = None
        self.ext = None
        self.save = False
        self.operations = ("blindrename", "undolastrename")
        greetings = (
            "++++++++++++++++++++++++++++++\n"
            "##### Welcome to the blindrename program"
            "\n#### Dev: {dev}, {email}"
            "\n##### Version: {version}\n++++++++++++++++++++++++++++++\n\n"
            .format(version=__version__, dev=__author__, email=__email__)
        )
        print(greetings)

    def operationselector(self)->str:
        self.listoperations()
        option = stdin.read(1)

        try:
            return self.operations[int(option)]
        except IndexError:
            print("## Invalid operation\n")
            self.listoperations()
        except ValueError:
            print("# Invalid selection, please use only numbers.\n")

    def listoperations(self)->None:
        print("## Type the number of the desired operation\n"
        "## Below are the currently available operations:\n")
        for i in range(len(self.operations)):
            print("\t{number} -> {name}\n".format(number=i, name=self.operations[i]))

    def inputdir(self)-> bool:   
        
        directory = input("\n## Please type in the directory with the files to be renamed:\n")
        if not os.path.isdir(directory):
            print("## {inputdir} is an invalid directory".format(inputdir=directory))
        else:
            self.directory = directory
            return True

    def inputext(self)-> bool:
        
        ext = input("\n## Please type the extension of the files to be renamed (For instance: .txt)\n")
        if not ext.strip() or not ext.startswith("."):
            print("## No extension selected.")
        else:
            self.ext = ext
            return True

    def namestableoption(self)-> bool:
        
        save = input("\n## Do you want to save the original names relation? (Y/N)\n## (If you choose"
                    " not to it won't be possible to rever to the original names.)\n"
        ).capitalize()        
        if save == "Y":
           self. save = True
           return True
        elif save == "N":
            self.save = False
            return True
        else:
            print("\n## Invalid answer, please type Y for yes or N for no.")
            
    def paramsummary(self)-> None:
        
        input( "\n\n### Selected settings:"
            "\n### Directory: {directory}"
            "\n### Extension affected: {ext}"
            "\n### Save names relation? {save}"
            "\n### Press enter to proceed.\n\n".format(directory=self.directory, ext=self.ext,
            save=self.save)
        )
