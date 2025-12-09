import unittest
from crm import User  


class TestUser(unittest.TestCase):

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
        expected = "User('Jean', 'Dupont', '+33 6 12 34 56 78', 'Paris, France')"
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


if __name__ == "__main__":
    unittest.main()
