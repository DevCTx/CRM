import re
import string
from tinydb import TinyDB, where, table
from pathlib import Path

class User:
    """User Class to create user instances with personal data
    """
    DB = TinyDB(Path(__file__).resolve().parent / "tinydb.json", indent=4)

    def __init__(self, first_name : str, last_name : str, phone_number : str = "", address : str = ""):
        self.first_name = User._check_name(first_name)
        self.last_name = User._check_name(last_name)
        self.phone_number = User._check_phone_number(phone_number)
        self.address = address
    
    @property
    def full_name(self):
        """Property generating a dyanmic full name in case of first or last name changes

        Returns:
            str: full name with first and last names
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        """Return Full User Data (Full Name, Address, Phone Number)

        Returns:
            str: full user data
        """
        return f"{self.full_name}\n{self.address}\n{self.phone_number}"

    def __repr__(self):
        """Represent the object as a string, as when it was created.

        Returns:
            str: User object representation
        """
        return f"User({self.first_name!r}, {self.last_name!r}, {self.phone_number!r}, {self.address!r})"

    @staticmethod
    def _check_name(name:str):
        """Checks if name is valid        
        
        Valid = Names with no digit and no punctuation except "-" , "'" or " "

        Args:
            name (str): name to check

        Raises:
            ValueError: if name is not valid

        Returns:
            str: name if valid
        """
        if not name or any( c.isdigit() or (c in string.punctuation and c not in "'-") for c in name ) :
            raise ValueError(f"Name : {name} is not valid")
        return name
        
    @staticmethod
    def _check_phone_number(phone_number:str):
        """Checks if phone number is valid
        
        Valid = only French phone numbers

        Exemples :  +33 (0)1 23 45 67 89 
                    +33 1 23 45 67 89 
                    +33123456789 
                    01 23 45 67 89
                    +33-1-23-45-67-89
                    01.23.45.67.89
        
        [international phone numbers would require to use phonenumbers library with an additional phone region parameter]

        Args:
            phone_number (str): the phone number to check

        Raises:
            ValueError: if the phone number is not a valid French phone number

        Returns:
            str: phone_number if valid
        """

        french_phone_regex = re.compile(r"""
            ^                                       # start of string
            (?:                                     # non-capturing group (not stored in memory): +33 or 0
                \+33                                # +33 international FR code
                (?:[ .-]?\(0\))?                    # optional (0), may be preceded by space/dot/hyphen
                [ .-]?                              # optional separator after
                |0                                  # OR national number starting with 0
            )
            (?:                                     # possible formats of the rest of the number
                \d{9}                               # 9 digits in a row (classic 0XXXXXXXXX)
                |(?:[ .-]?\d{1})(?:[ .-]?\d{2}){4}  # OR 1-2-2-2-2 format: 4 groups of 2 digits preceded by only 1
                |(?:[ .-]?\d{3}){3}                 # 3-3-3 format
            )
            $                                       # end of string
        """, re.VERBOSE)                            # allows to write more readable regexes.

        if phone_number and not french_phone_regex.match(phone_number):
           raise ValueError(f"Phone Number : {phone_number} is not valid")
        return phone_number

    #-----------------------
    # TinyDB Management
    #-----------------------

    def save(self) -> int :
        """Insert or Update the new User into the database

        Returns:
            int: the index of the record into the database
        """
        if self.exists():
            return User.DB.update(self.__dict__, doc_ids=[self.db_instance.doc_id])[0]
        else:
            return User.DB.insert(self.__dict__)

    @property 
    def db_instance(self) -> table.Document :
        """Get the User instance from the database
        If several instances exist, returns only the first one.

        Returns:
            tinydb.table.Document : the User instance find in DB or None if does not exist
        """
        doc = User.DB.get((where('first_name') == self.first_name) & (where('last_name') == self.last_name))
        if type(doc) is list:
            return doc[0]
        return doc

    def exists(self) -> bool :
        """Check if the user exists in database

        Returns:
            bool: True if the user exists in database else False
        """
        return self.db_instance is not None
    
    def delete(self) -> int:
        if self.exists():
            return User.DB.remove(doc_ids=[self.db_instance.doc_id])[0]
        return None


def get_all_users():
    return [User(**user) for user in User.DB.all()]


if __name__ == "__main__" :
    from faker import Faker
    
    # for _ in range(10):
    #     fake = Faker("fr_FR")
    #     user = User(
    #         first_name=fake.first_name(),
    #         last_name=fake.last_name(),
    #         phone_number=fake.phone_number(),
    #         address=fake.address()
    #     )
    #     user.save()
    #     print("-"*20)

    martin = User("Martin", "Voisin")
    print(martin.delete())
    print(martin.save())
    martin.phone_number = "0123456789"
    print(martin.phone_number)
    print(martin.save())
    print(type(martin.db_instance))
