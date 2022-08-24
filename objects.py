from __future__ import annotations
from dataclasses import dataclass
import itertools
from typing import List


@dataclass
class NumberedObject():
    id = itertools.count()

class ObjectTable():
    def __init__(self) -> None:
        self._dict = {}

    def add(self, obj: NumberedObject) -> None:
        self._dict.update({obj.id: obj})

    def remove(self, obj: NumberedObject) -> None:
        self._dict.pop(obj.id)

    def get(self, obj_id: int) -> NumberedObject:
        return self._dict[obj_id]

    def filter(self, attr, value):
        sorted_dict = {getattr(v, attr): v for k, v in self._dict.items()}
        return sorted_dict[value]


class TrainingClass(NumberedObject):
    id = itertools.count()
    name: str
    trainer_list: List[Trainer]
    price: str
    max_members: int
    member_list: List[Member]

    def __init__(self, name: str, price: str, max_members: int) -> None:
        super().__init__()
        self.id = next(self.id)
        self.name = name
        self.trainer_list = []
        self.price = price
        self.max_members = max_members
        self.member_list = []

    def add_member(self, member_obj: Member) -> None:
        if len(self.member_list) == self.max_members:
            raise ValueError("Class is full")
        self.member_list.append(member_obj)
        member_obj.class_list.append(self)

    def add_trainer(self, trainer_obj: Trainer):
        self.trainer_list.append(trainer_obj)
        trainer_obj.class_list.append(self)

    def remove_member(self, member_obj: Member):
        self.member_list.remove(member_obj)
        member_obj.class_list.remove(self)

    def remove_trainer(self, trainer_obj: Trainer):
        self.trainer_list.remove(trainer_obj)
        trainer_obj.class_list.remove(self)


class Member(NumberedObject):
    id = itertools.count()
    name: str
    surname: str
    phone: str
    age: int
    class_list: List[TrainingClass]

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


class Trainer(NumberedObject):
    id = itertools.count()
    name: str
    surname: str
    phone: str
    class_list: List[TrainingClass]

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
