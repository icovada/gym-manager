from dataclasses import dataclass
from typing import Callable
from tabulate import tabulate
import itertools
from objects import ObjectTable


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
        while True:
            choice = input("Select an option: ")

            if choice in case_choices.keys():
                case_choices[choice]()
                print(tabulate(menu_choices))
            elif choice == "q":
                break
            else:
                print("Choice not found")
                continue

class RelationshipMenu(BaseMenu):
    def __init__(self, table: ObjectTable):
        super().__init__()
        self.table = table
        for i in self.table.relationships:
            self.add_choice(MenuChoice(f"Add {i.side_a.object_class.__name__} to {i.side_b.object_class.__name__}", i.interactive_add))
            self.add_choice(MenuChoice(f"Remove {i.side_a.object_class.__name__} to {i.side_b.object_class.__name__}", i.interactive_add))

class CRUDMenu(BaseMenu):
    def __init__(self, table: ObjectTable):
        super().__init__()
        self.table = table
        self.add_choice(MenuChoice("List", self.list))
        self.add_choice(MenuChoice("Create", self.create))
        self.add_choice(MenuChoice("Update", self.update))
        self.add_choice(MenuChoice("Delete", self.delete))
        self.add_choice(MenuChoice("Manage Relationships", self.relationships))

    def list(self) -> None:
        print(self.table.format_list())

    def prompt(self):
        print("######### Manage " + self.table.object_class.__name__ + "s ###########")
        return super().prompt()

    def create(self):
        newdata = {}
        for attr, attrname in self.table.object_class.prompt_attrs.items():
            newdata[attr] = input(f"Insert {attrname}: ")

        new_obj = self.table.object_class(**newdata)
        self.table.add(new_obj)

    def update(self):
        obj = self.table.interactive_get()

        for attr, attrname in self.table.object_class.prompt_attrs.items():
            newval = input(f"Insert {attrname} [{getattr(obj, attr)}]: ")
            if newval != "":
                setattr(obj, attr, newval)

    def delete(self):
        obj = self.table.interactive_get()
        self.table.remove(obj)

    def relationships(self):
        relationship_menu = RelationshipMenu(self.table)
        relationship_menu.prompt()