import unittest
from objects import Member, ObjectTable, Trainer, TrainingClass


class TestBaseObjects(unittest.TestCase):
    def test_member_to_training_class_add_remove(self):
        training_class = TrainingClass("yoga", "300", 3)
        member = Member("federico", "tabbo", "3601074728", 31)

        training_class.add_member(member)
        self.assertIn(member, training_class.member_list)
        self.assertIn(training_class, member.class_list)

        training_class.remove_member(member)
        self.assertNotIn(member, training_class.member_list)
        self.assertNotIn(training_class, member.class_list)

    def test_training_class_to_member_add_remove(self):
        training_class = TrainingClass("yoga", "300", 3)
        member = Member("federico", "tabbo", "3601074728", 31)

        member.add_training_class(training_class)
        self.assertIn(member, training_class.member_list)
        self.assertIn(training_class, member.class_list)

        member.remove_training_class(training_class)
        self.assertNotIn(member, training_class.member_list)
        self.assertNotIn(training_class, member.class_list)

    def test_trainer_to_training_class_add_remove(self):
        training_class = TrainingClass("yoga", "300", 3)
        trainer = Trainer("tizio", "muscoloso", "432443")

        training_class.add_trainer(trainer)
        self.assertIn(trainer, training_class.trainer_list)
        self.assertIn(training_class, trainer.class_list)

        training_class.remove_trainer(trainer)
        self.assertNotIn(trainer, training_class.trainer_list)
        self.assertNotIn(training_class, trainer.class_list)

    def test_training_class_to_trainer_add_remove(self):
        training_class = TrainingClass("yoga", "300", 3)
        trainer = Trainer("tizio", "muscoloso", "432443")

        trainer.add_training_class(training_class)
        self.assertIn(trainer, training_class.trainer_list)
        self.assertIn(training_class, trainer.class_list)

        trainer.remove_training_class(training_class)
        self.assertNotIn(trainer, training_class.trainer_list)
        self.assertNotIn(training_class, trainer.class_list)

    def test_training_class_add_too_many_members(self):
        training_class = TrainingClass("yoga", "300", 0)
        member = Member("federico", "tabbo", "3601074728", 31)

        self.assertRaises(
            ValueError, training_class.add_member, member_obj=member)


class TestObjectTable(unittest.TestCase):
    def test_find_object_by_id(self):
        training_class = TrainingClass("zumba", "350", 3)
        class_list = ObjectTable()
        class_list.add(training_class)

        self.assertIn(training_class.id, class_list._dict)
        self.assertEqual(training_class, class_list.get(training_class.id))

    def test_find_object_by_attr(self):
        training_class = TrainingClass("zumba", "350", 3)
        class_list = ObjectTable()
        class_list.add(training_class)

        self.assertEqual(training_class, class_list.filter("name", "zumba"))
        self.assertEqual(training_class, class_list.filter("price", "350"))

    def test_find_object_by_attr_too_many(self):
        training_class = TrainingClass("zumba", "350", 3)
        training_class2 = TrainingClass("zumba", "350", 3)
        class_list = ObjectTable()
        class_list.add(training_class)
        class_list.add(training_class2)

        self.assertRaises(AssertionError, class_list.filter,
                          attr="name", value="zumba")

    def test_find_object_by_attr_too_few(self):
        class_list = ObjectTable()

        self.assertRaises(AssertionError, class_list.filter,
                          attr="name", value="zumba")


if __name__ == '__main__':
    unittest.main()
