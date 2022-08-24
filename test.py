import unittest
from objects import Member, Trainer, TrainingClass


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
        
        self.assertRaises(ValueError, training_class.add_member, member_obj=member)
        

if __name__ == '__main__':
    unittest.main()
