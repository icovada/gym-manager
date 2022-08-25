from objects import TrainingClass, Member, Trainer, ObjectTable
from menu_manager import BaseMenu, CRUDMenu, MenuChoice


def main(members_list, trainers_list, training_class_list):
    members_menu = CRUDMenu(members_list)
    trainers_menu = CRUDMenu(trainers_list)
    training_class_menu = CRUDMenu(training_class_list)

    base = BaseMenu()
    base.add_choice(MenuChoice("Manage Members", members_menu.prompt))
    base.add_choice(MenuChoice("Manage Trainers", trainers_menu.prompt))
    base.add_choice(MenuChoice("Manage Training Classes",
                    training_class_menu.prompt))

    base.prompt()


if __name__ == "__main__":
    members_list = ObjectTable(Member)
    trainers_list = ObjectTable(Trainer)
    training_class_list = ObjectTable(TrainingClass)
    main(members_list, trainers_list, training_class_list)
