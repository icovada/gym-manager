from dataclasses import dataclass
from multiprocessing.sharedctypes import Value
from typing import List, Type, Callable
from tabulate import tabulate
import itertools


@dataclass
class MenuChoice():
    description: str
    callable: Callable


class BaseMenu():
    choices: list

    def __init__(self):
        self.choices = []

    def add_choice(self, choice: MenuChoice):
        self.choices.append(choice)

    def prompt(self):
        counter = itertools.count()
        # start from one
        next(counter)

        numbered_choices = [[str(next(counter)), x] for x in self.choices]
        menu_choices = [[x[0], x[1].description] for x in numbered_choices]
        case_choices = {x[0]: x[1].callable for x in numbered_choices}

        menu_choices.append(["q", "Exit"])

        print(tabulate(menu_choices))
        found = False
        while not found:
            choice = input("Select an option: ")

            if choice in case_choices.keys():
                found = True
                case_choices[choice]()
            elif choice == "q":
                found = True
                continue
            else:
                print("Choice not found")
                continue
