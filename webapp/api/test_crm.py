import unittest
from crm import User, get_all_users  
from tinydb import TinyDB
from tinydb.storages import MemoryStorage
from pathlib import Path

class TestUser(unittest.TestCase):
    """Tests for the user data"""

    def test_valid_user_creation(self):
        """Tests that a valid user is created correctly"""
        user = User("Jean", "Dupont", "+33 6 12 34 56 78", "Paris, France")
        self.assertEqual(user.first_name, "Jean")
        self.assertEqual(user.last_name, "Dupont")
        self.assertEqual(user.phone_number, "+33 6 12 34 56 78")
        self.assertEqual(user.address, "Paris, France")
        self.assertEqual(user.full_name, "Jean Dupont")

    def test_valid__str__(self):
        """Tests that a valid user return valid information as str with __str__"""
        user = User("Jean", "Dupont", "+33 6 12 34 56 78", "Paris, France")
        self.assertIn("Jean Dupont", str(user))
        self.assertIn("Paris, France", str(user))
        self.assertIn("+33 6 12 34 56 78", str(user))

    def test_valid__repr__(self):
        """Tests that valid user return the str image of the same object with __repr__"""
        user = User("Jean", "Dupont", "+33 6 12 34 56 78", "Paris, France")
        expected = "User('Jean', 'Dupont', '+33 6 12 34 56 78', 'Paris, France', None)"
        self.assertTrue(repr(user) == expected)


    valid_names = [
        "Pierre", 
        "Jean-Pierre", 
        "Anne Marie", 
        "Dach'wen",
        "Garnier-Dupont", 
        "Mac Leod", 
        "O'Connor"
    ]

    def test_valid_static_check_name(self):
        """Tests the valid names on the static _check_name method"""
        for name in self.valid_names:
            self.assertEqual(User._check_name(name), name)
    
    def test_valid_first_name(self):
        """Tests that valid first names do not raise ValueError"""
        for name in self.valid_names:
            with self.subTest(name=name):   # Allows you to see which one failed, if applicable.
                user = User(name, "Name")
                self.assertEqual(user.first_name, name)

    def test_valid_last_name(self):
        """Test that valid last names do not raise ValueError"""
        for name in self.valid_names:
            with self.subTest(name=name):   # Allows you to see which one failed, if applicable.
                user = User("Name", name)
                self.assertEqual(user.last_name, name)

    invalid_names = [
        "", 
        "Jean~Pierre", 
        "$ophie", 
        "Gh!slain", 
        "Dup0nt", 
        "Dupon#"
    ]

    def test_invalid_static_check_name(self):
        """Tests the invalid names on the static _check_name method"""
        for name in self.invalid_names:
            with self.assertRaises(ValueError):
                User._check_name(name)

    def test_invalid_first_name(self):
        """Tests that invalid first names raise ValueError"""
        for name in self.invalid_names:
            with self.assertRaises(ValueError):
                User(name, "Name")

    def test_invalid_last_name(self):
        """Tests that invalid last names raise ValueError"""
        for name in self.invalid_names:
            with self.assertRaises(ValueError):
                User("Name", name)

    def test_full_name_property(self):
        """Tests that changing first or last name updates full_name"""
        user = User("Jean", "Dupont")
        self.assertEqual(user.full_name, "Jean Dupont")
        user.first_name = "Pierre"
        self.assertEqual(user.full_name, "Pierre Dupont")
        user.last_name = "Dupontel"
        self.assertEqual(user.full_name, "Pierre Dupontel")

    valid_FR_numbers = [
        "01 23 45 67 89",
        "01.23.45.67.89",
        "01-23-45-67-89",
        "0123456789",
        "+33123456789",
        "+33 1 23 45 67 89",
        "+33 (0)1 23 45 67 89",
        "+33-1-23-45-67-89",
        "+33 123 456 789",
        "+33-123-456-789",
        "+33.123.456.789",
    ]

    def test_valid_static_check_phone_number(self):
        """Tests the valid phone number formats into _check_phone_number static method"""
        for number in self.valid_FR_numbers:
            self.assertEqual(User._check_phone_number(number), number)

    def test_valid_phone_numbers(self):
        """Tests valid French phone numbers"""
        for number in self.valid_FR_numbers:
            user = User("NotRelevant", "NotRelevant", number)
            self.assertEqual(user.phone_number, number)

    invalid_numbers = [
        "+44 20 7946 0958",  # UK number
        "+1 520 794 0958",   # US number
        "+1 (520) 794-0958", # US number
        "+86 138 00138000",  # CN number
        "+5511912345678",    # Brazil E.164
        "12345",             # Too short
        "01 23 45 67",       # Too short FR number
        "+33 123 456 7890"   # Too long FR number
    ]

    def test_invalid_static_check_phone_number(self):
        """Tests the invalid phone number formats into _check_phone_number static method"""
        for number in self.invalid_numbers:
            with self.assertRaises(ValueError):
                User._check_phone_number(number)

    def test_invalid_phone_numbers(self):
        """Tests invalid phone numbers raise ValueError"""
        for number in self.invalid_numbers:
            with self.assertRaises(ValueError):
                User("NotRelevant", "NotRelevant", number)


class TestUserDatabase(unittest.TestCase):
    """Tests for database operations"""
    
    @classmethod
    def setUpClass(cls):    # "Executed once before each test"
        """Close the original file-based DB once before all tests"""
        User.DB.close()

    def setUp(self):        # "Executed before each test"
        """Use an in-memory DB instead of the JSON DB before each test"""
        User.DB = TinyDB(storage=MemoryStorage)
    
    def tearDown(self):     # "Executed after each test"
        """Clean up the DB after each test"""
        User.DB.drop_tables()
        User.DB.close()

    @classmethod
    def tearDownClass(cls): # "Executed once after each test"
        """Restore the original file-based DB after all tests"""
        User.DB = TinyDB(Path(__file__).resolve().parent / "tinydb.json", indent=4)


    def test_db_instance(self):
        """Test retrieving the instance from the DB"""
        user1 = User("Jean", "Dupont", "0123456789", "Paris")       # create 3 users
        user2 = User("Marie", "Morrin", "0198765432", "Lyon")
        user3 = User("Pierre", "Dubois", "0122334455", "Rennes")
        user1.save()                                                # Save only 2 users in DB
        user2.save()
        
        db_user2 = user2.db_instance()                              # get existing user from db
        self.assertIsNotNone(db_user2)                              # Verify it returns not None
        self.assertEqual(db_user2['first_name'], "Marie")           # verify db_instance get the right first name
        self.assertEqual(db_user2['last_name'], "Morrin")           # verify db_instance get the right last name
        
        # Test user3 does not exist in DB
        db_user3 = user3.db_instance()                              # try to get inexisting user from db
        self.assertIsNone(db_user3)                                 # verify it returns None

    def test_save_new_user(self):
        """Test inserting a new user"""
        user1 = User("Jean", "Dupont", "0123456789", "Paris")       # create a user instance
        doc_user1 = user1.save()                                    # create a user in db
        self.assertIsInstance(doc_user1, int)                       # verify it returns an id
        self.assertEqual(doc_user1, 1)                              # verify the id is the first one (new db)
        self.assertEqual(user1._doc_id, 1)                          # verify that doc_id is stored correctly
    
    def test_save_update_user(self):
        """Test updating an existing user"""
        user1 = User("Jean", "Dupont", "0123456789", "Paris")       # create a user instance
        doc_user1 = user1.save()                                    # create a user in db
        self.assertEqual(doc_user1, 1)                              # verify the id is the first one (new db)
        user1.phone_number = "0111111111"                           # modify its phone number
        doc_user1 = user1.save()                                    # update the user in db
        self.assertEqual(doc_user1, 1)                              # verify the id is still the first one        
        updated = User.DB.get(doc_id=1)                             # get information of the first document
        self.assertEqual(updated['phone_number'], "0111111111")     # verify the phone number was updated
            
    def test_delete(self):
        """Test deleting a user"""
        user1 = User("Jean", "Dupont", "0123456789", "Paris")       # create a user instance

        result = user1.delete()                                     # try to delete unexisting user
        self.assertIsNone(result)                                   # verify it returns None

        doc_user1 = user1.save()                                    # create a user in db
        self.assertEqual(doc_user1, 1)                              # verify the id is the first one (new db)
        self.assertEqual(len(User.DB.all()), 1)                     # check DB has 1 user
        self.assertEqual(user1._doc_id, 1)                          # verify the db_id of user is the first one

        db_user1 = user1.delete()                                   # delete the existing user
        self.assertEqual(doc_user1, 1)                              # verify the id is the first one 
        self.assertEqual(len(User.DB.all()), 0)                     # check DB is empty
        self.assertIsNone(user1._doc_id)                            # verify the db_id of user is None

    def test_get_all_users(self):
        """Test get_all_users() with DB"""
        users = get_all_users()                                     # Try get users from empty DB
        self.assertEqual(len(users), 0)                             # verify it returns 0
    
        user1 = User("Jean", "Dupont", "0123456789", "Paris")       # create 2 user instances
        user2 = User("Marie", "Morrin", "0198765432", "Lyon")       
        user1.save()                                                # save 2 users in db
        user2.save()                                                
        users = get_all_users()                                     # get users from DB
        self.assertEqual(len(users), 2)                             # verify it returns 3
        self.assertIsInstance(users[0], User)                       # verify user1 is a User instance
        self.assertIsInstance(users[1], User)                       # verify user2 is a User instance
        self.assertEqual(users[0]._doc_id, 1)                       # verify that doc_id is stored correctly
        self.assertEqual(users[1]._doc_id, 2)                       # verify that doc_id is stored correctly
    
    def test_no_duplicate(self):
        """Test multiple saves don't create duplicates"""
        user1 = User("Jean", "Dupont", "0123456789", "Paris")       # create user instance
        user2 = User("Jean", "Dupont", "0123456789", "Paris")       # create identical user instance
        user1.save()
        user2.save()
        self.assertEqual(len(User.DB.all()), 1)                     # verify no duplicate


if __name__ == "__main__":
    unittest.main()
