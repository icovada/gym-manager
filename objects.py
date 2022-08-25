from __future__ import annotations
from tabulate import tabulate
import itertools
from typing import List, Type, Dict


class NumberedObject():
    id = itertools.count()
    prompt_attrs: Dict[str, str]
    menu_attrs: Dict[str, str]

    def get_menu_dict(self) -> dict:
        outd = {}
        for attr in self.menu_attrs:
            outd[attr] = getattr(self, attr)

        return outd

    def cleanup(self) -> None:
        raise NotImplementedError


class ObjectTable():
    _dict = Dict[int, NumberedObject]
    object_class: Type[NumberedObject] = NumberedObject
    relationships: set = set()

    def __init__(self, object_class: Type[NumberedObject]) -> None:
        self._dict = {}
        self.object_class = object_class

    def all(self) -> list:
        return self._dict.values()

    def add(self, obj: NumberedObject) -> None:
        if not isinstance(obj, self.object_class):
            raise ValueError

        self._dict.update({obj.id: obj})

    def remove(self, obj: NumberedObject) -> None:
        obj.cleanup()
        self._dict.pop(obj.id)

    def get(self, obj_id: int) -> NumberedObject:
        obj_id = int(obj_id)
        return self._dict[obj_id]

    def filter(self, attr, value) -> list[NumberedObject]:
        out_list = []
        for x in self._dict.values():
            if getattr(x, attr) == value:
                out_list.append(x)

        return out_list

    def format_list(self) -> str:
        table = [x.get_menu_dict() for x in self._dict.values()]
        return tabulate(table, self.object_class.menu_attrs, tablefmt="simple")

    def interactive_get(self) -> Type[object_class]:
        print(self.format_list())
        print("")
        id = input(f"Select a {self.object_class.__name__} by its ID: ")
        return self.get(id)


class TrainingClass(NumberedObject):
    id = itertools.count()
    name: str
    trainer_list: List[Trainer]
    price: str
    max_members: int
    member_list: List[Member]
    prompt_attrs = {"name": "Name",
                    "price": "Price", "max_members": "Max Members"}
    menu_attrs = {"id": "ID", "name": "Name",
                  "price": "Price", "max_members": "Max Members",  "empty_seats": "Empty Seats", "member_list": "Members"}

    def __init__(self, name: str, price: str, max_members: int) -> None:
        super().__init__()
        self.id = next(self.id)
        self.name = name
        self.trainer_list = []
        self.price = price
        self.max_members = max_members
        self.member_list = []

    @property
    def empty_seats(self) -> int:
        return self.max_members - len(self.member_list)

    def add_Member(self, member_obj: Member) -> None:
        if len(self.member_list) == self.max_members:
            raise ValueError("Class is full")
        self.member_list.append(member_obj)
        member_obj.class_list.append(self)

    def add_Trainer(self, trainer_obj: Trainer) -> None:
        self.trainer_list.append(trainer_obj)
        trainer_obj.class_list.append(self)

    def remove_Member(self, member_obj: Member) -> None:
        self.member_list.remove(member_obj)
        member_obj.class_list.remove(self)

    def remove_Trainer(self, trainer_obj: Trainer) -> None:
        self.trainer_list.remove(trainer_obj)
        trainer_obj.class_list.remove(self)

    def cleanup(self) -> None:
        for i in list(self.member_list):
            self.remove_Member(i)

        for i in list(self.trainer_list):
            self.remove_Trainer(i)

    def __setattr__(self, __name: str, __value) -> None:
        if __name == "max_members":
            __value = int(__value)
        return super().__setattr__(__name, __value)

    def __repr__(self) -> str:
        return f"TrainingClass({self.id})"

    def __str__(self) -> str:
        return f"TrainingClass({self.name})"


class Member(NumberedObject):
    id = itertools.count()
    name: str
    surname: str
    phone: str
    age: int
    class_list: List[TrainingClass]
    prompt_attrs = {"name": "Name",
                    "surname": "Surname", "phone": "Phone", "age": "Age"}
    menu_attrs = {"id": "ID", "name": "Name",
                  "surname": "Surname"}

    def __init__(self, name: str, surname: str, phone: str, age: int):
        super().__init__()
        self.id = next(self.id)
        self.name = name
        self.surname = surname
        self.phone = phone
        self.age = age
        self.class_list = []

    def add_TrainingClass(self, class_obj: TrainingClass):
        class_obj.add_Member(self)

    def remove_TrainingClass(self, trainingclass_obj: TrainingClass):
        trainingclass_obj.remove_Member(self)

    def cleanup(self) -> None:
        for i in list(self.class_list):
            self.remove_TrainingClass(i)

    def __repr__(self) -> str:
        return f"Member({self.id})"

    def __str__(self) -> str:
        return f"Member({self.name}, {self.surname})"


class Trainer(NumberedObject):
    id = itertools.count()
    name: str
    surname: str
    phone: str
    class_list: List[TrainingClass]
    prompt_attrs = {"name": "Name",
                    "surname": "Surname", "phone": "Phone"}
    menu_attrs = {"id": "ID", "name": "Name",
                  "surname": "Surname", "phone": "Phone"}

    def __init__(self, name: str, surname: str, phone: str):
        super().__init__()
        self.id = next(self.id)
        self.name = name
        self.surname = surname
        self.phone = phone
        self.class_list = []

    def add_TrainingClass(self, training_class_obj: TrainingClass):
        training_class_obj.add_Trainer(self)

    def remove_TrainingClass(self, training_class_obj: TrainingClass):
        training_class_obj.remove_Trainer(self)

    def cleanup(self) -> None:
        for i in list(self.class_list):
            self.remove_TrainingClass(i)

    def __repr__(self) -> str:
        return f"Trainer({self.id})"

    def __str__(self) -> str:
        return f"Trainer({self.name}, {self.surname})"


class NumberedObjectRelationship():
    def __init__(self, side_a: ObjectTable, side_b: ObjectTable) -> None:
        self.side_a = side_a
        self.side_b = side_b
        self.side_a.relationships.add(self)
        self.side_b.relationships.add(self)

    def interactive_add(self):
        a_obj = self.side_a.interactive_get()
        b_obj = self.side_b.interactive_get()

        self.add(a_obj, b_obj)

    def interactive_remove(self):
        a_obj = self.side_a.interactive_get()
        b_obj = self.side_b.interactive_get()

        self.remove(a_obj, b_obj)

    def add(self, a_obj, b_obj):
        f = getattr(a_obj, "add_"+b_obj.__class__.__name__)
        f(b_obj)

    def remove(self, a_obj, b_obj):

        f = getattr(a_obj, "renmove_"+b_obj.__class__.__name__)
        f(b_obj)
