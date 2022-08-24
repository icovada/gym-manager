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
        class_list = ObjectTable(TrainingClass)
        class_list.add(training_class)

        self.assertIn(training_class.id, class_list._dict)
        self.assertEqual(training_class, class_list.get(training_class.id))

    def test_find_object_by_attr(self):
        training_class = TrainingClass("zumba", "350", 3)
        class_list = ObjectTable(TrainingClass)
        class_list.add(training_class)

        self.assertIn(training_class, class_list.filter("name", "zumba"))
        self.assertIn(training_class, class_list.filter("price", "350"))

    def test_find_object_by_attr_too_many(self):
        training_class = TrainingClass("zumba", "350", 3)
        training_class2 = TrainingClass("zumba", "350", 3)
        class_list = ObjectTable(TrainingClass)
        class_list.add(training_class)
        class_list.add(training_class2)

        self.assertEqual(len(class_list.filter(attr="name", value="zumba")), 2)

    def test_find_object_by_attr_too_few(self):
        class_list = ObjectTable(TrainingClass)

        self.assertEqual(len(class_list.filter(attr="name", value="zumba")), 0)


    def test_fail_add_other_object_type(self):
        class_list = ObjectTable(Member)
        training_class = TrainingClass("zumba", "350", 3)

        self.assertRaises(ValueError, class_list.add, obj=training_class)


class TestCleanup(unittest.TestCase):
    def test_clean_training_class(self):
        class_list = ObjectTable(TrainingClass)
        trc1 = TrainingClass("zumba", "350", 3)
        trc2 = TrainingClass("zumba2", "350", 3)
        
        class_list.add(trc1)
        class_list.add(trc2)
        
        trainer_list = ObjectTable(Trainer)
        tr1 = Trainer("paola", "tizia", "44343423")
        tr2 = Trainer("paolo", "tizio", "44343423")
        trainer_list.add(tr1)
        trainer_list.add(tr2)

        member_list = ObjectTable(Member)
        mem1 = Member("paolo", "tizio", "44343423", 34)
        mem2 = Member("paola", "tizia", "44343423", 45)
        member_list.add(mem1)
        member_list.add(mem2)
        
        trc1.add_member(mem1)
        trc1.add_member(mem2)
        trc1.add_trainer(tr1)

        trc2.add_member(mem1)
        trc2.add_member(mem2)
        trc2.add_trainer(tr2)

        class_list.remove(trc1)
        class_list.remove(trc2)
        
        self.assertNotIn(trc1, class_list.all())
        self.assertNotIn(trc1, tr1.class_list)
        self.assertNotIn(trc1, tr2.class_list)
        self.assertNotIn(trc1, mem1.class_list)
        self.assertNotIn(trc1, mem2.class_list)
        
        self.assertNotIn(trc2, class_list.all())
        self.assertNotIn(trc2, tr1.class_list)
        self.assertNotIn(trc2, tr2.class_list)
        self.assertNotIn(trc2, mem1.class_list)
        self.assertNotIn(trc2, mem2.class_list)

if __name__ == '__main__':
    unittest.main()
