from dataclasses import dataclass
from multiprocessing.sharedctypes import Value
from typing import List
from tabulate import tabulate
import itertools


@dataclass
class MenuChoice():
    description: str
    callable: function

class BaseMenu():
    choices: list
    
    def __init__(self, choices: List[MenuChoice]):
        self.choices = choices

    def prompt(self):
        counter = itertools.count()
        # start from one
        next(counter)
        
        numbered_choices = [[next(counter), x] for x in self.choices]
        menu_choices = [[x[0], x[1].description] for x in numbered_choices]
        case_choices = {x[0]: x[1].callable for x in numbered_choices}
        
        print(tabulate(menu_choices))
        found = False
        while not found:
            choice = input("Select an option, or q to exit: ")
            try:
                choice = int(choice)
            except ValueError:
                pass #TODO
            
            match choice:
                case case_choices.keys():
                    found = True
                    case_choices[choice]()
                case "q":
                    found = True
                    continue
                case _:
                    print("Choice not found")
                    continue
            
        
        

class CRUDInteractiveMenu():
    