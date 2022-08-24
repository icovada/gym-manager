from __future__ import annotations
from tabulate import tabulate
import itertools
from typing import List, Type, Dict


class NumberedObject():
    id = itertools.count()
    prompt_attrs: Dict[str, str] = {}

    def get_prompt_attrs_dict(self) -> dict:
        outd = {}
        for attr in self.prompt_attrs:
            outd[attr] = getattr(self, attr)

        return outd
    
    def cleanup(self) -> None:
        raise NotImplementedError


class ObjectTable():
    _dict = Dict[int, NumberedObject]
    object_class: Type[NumberedObject] = NumberedObject

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

    def filter(self, attr, value) -> NumberedObject:
        out_list = []
        for x in self._dict.values():
            if getattr(x, attr) == value:
                out_list.append(x)

        assert len(out_list) < 2, "Search returned more than one result"
        assert len(out_list) > 0, "Search returned zero results"

        return out_list[0]

    def format_list(self) -> str:
        table = [x.get_prompt_attrs_dict() for x in self._dict.values()]
        return tabulate(table, self.object_class.prompt_attrs, tablefmt="simple")

    def interactive_get(self) -> Type[object_class]:
        print(self.format_list())
        print("")
        id = input("Select a row by its ID: ")
        return self.get(id)


class TrainingClass(NumberedObject):
    id=itertools.count()
    name: str
    trainer_list: List[Trainer]
    price: str
    max_members: int
    member_list: List[Member]
    prompt_attrs={"id": "ID", "name": "Name",
        "price": "Price", "max_members": "Max Members", "empty_seats": "Empty Seats"}

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

    def add_member(self, member_obj: Member) -> None:
        if len(self.member_list) == self.max_members:
            raise ValueError("Class is full")
        self.member_list.append(member_obj)
        member_obj.class_list.append(self)

    def add_trainer(self, trainer_obj: Trainer) -> None:
        self.trainer_list.append(trainer_obj)
        trainer_obj.class_list.append(self)

    def remove_member(self, member_obj: Member) -> None:
        self.member_list.remove(member_obj)
        member_obj.class_list.remove(self)

    def remove_trainer(self, trainer_obj: Trainer) -> None:
        self.trainer_list.remove(trainer_obj)
        trainer_obj.class_list.remove(self)

    def cleanup(self) -> None:
        for i in list(self.member_list):
            self.remove_member(i)
        
        for i in list(self.trainer_list):
            self.remove_trainer(i)

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
    prompt_attrs={"id": "ID", "name": "Name",
        "surname": "Surname", "phone": "Phone", "age": "Age"}


    def __init__(self, name: str, surname: str, phone: str, age: int):
        super().__init__()
        self.id = next(self.id)
        self.name = name
        self.surname = surname
        self.phone = phone
        self.age = age
        self.class_list = []

    def add_training_class(self, class_obj: TrainingClass):
        class_obj.add_member(self)

    def remove_training_class(self, trainingclass_obj: TrainingClass):
        trainingclass_obj.remove_member(self)

    def cleanup(self) -> None:
        for i in list(self.class_list):
            self.remove_training_class(i)
        
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
    prompt_attrs={"id": "ID", "name": "Name",
        "surname": "Surname", "phone": "Phone"}

    def __init__(self, name: str, surname: str, phone: str):
        super().__init__()
        self.id = next(self.id)
        self.name = name
        self.surname = surname
        self.phone = phone
        self.class_list = []

    def add_training_class(self, training_class_obj: TrainingClass):
        training_class_obj.add_trainer(self)

    def remove_training_class(self, training_class_obj: TrainingClass):
        training_class_obj.remove_trainer(self)
        
    def cleanup(self) -> None:
        for i in list(self.class_list):
            self.remove_training_class(i)

    def __repr__(self) -> str:
        return f"Trainer({self.id})"

    def __str__(self) -> str:
        return f"Trainer({self.name}, {self.surname})"
