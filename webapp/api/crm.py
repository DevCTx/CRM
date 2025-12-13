import re
import string
from tinydb import TinyDB, where, table
from pathlib import Path

class User:
    """User Class to create user instances with personal data
    """
    DB = TinyDB(Path(__file__).resolve().parent / "tinydb.json", indent=4)

    def __init__(self, first_name : str, last_name : str, phone_number : str = "", address : str = "", doc_id=None):
        """Initialize a new User instance
        
        Args:
            first_name (str): User's first name (no digits or special punctuation)
            last_name (str): User's last name (no digits or special punctuation)
            phone_number (str, optional): French phone number only
            address (str, optional): User's address
            doc_id (int, optional): user id from DB if exists
        
        Raises:
            ValueError: If first_name, last_name, or phone_number are invalid
        """
        self.first_name = User._check_name(first_name)
        self.last_name = User._check_name(last_name)
        self.phone_number = User._check_phone_number(phone_number)
        self.address = address
        self._doc_id = doc_id   # tinyDB
    
    @property
    def full_name(self) -> str:
        """Property generating a dyanmic full name in case of first or last name changes

        Returns:
            str: full name with first and last names
        """
        return f"{self.first_name} {self.last_name}"

    def __str__(self) -> str:
        """Return Full User Data (Full Name, Address, Phone Number)

        Returns:
            str: full user data
        """
        return f"{self.full_name}\n{self.address}\n{self.phone_number}"

    def __repr__(self) -> str:
        """Represent the object as a string, as when it was created.

        Returns:
            str: User object representation
        """
        return f"User({self.first_name!r}, {self.last_name!r}, {self.phone_number!r}, {self.address!r}, {self._doc_id})"

    @staticmethod
    def _check_name(name:str) -> str:
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
    def _check_phone_number(phone_number:str) -> str:
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

    @property
    def doc_id(self) -> int:
        """Public accessor for Document ID for index.html (private not accessible)
        
        Returns:
            int : The Document ID if saved in database or None
        """
        return self._doc_id

    def db_instance(self) -> table.Document:
        """Get the user data from the database by first and last name

        Returns:
            table.Document: The user data if exists or None
        """
        return User.DB.get((where('first_name') == self.first_name) & 
                          (where('last_name') == self.last_name))
    
    def save(self) -> int :
        """Insert or Update the new User into the database

        Ensures no duplicates in the database, based on first and last name.

        Returns:
            int: The document ID of the saved record
        """
        data = {    ## All data except doc_id !!!
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone_number": self.phone_number,
            "address": self.address,
        }
        
        # Check if user already exists in DB by name
        existing = self.db_instance()        
        if existing :
            self._doc_id = User.DB.update(data, doc_ids=[existing.doc_id])[0]
        else:
            self._doc_id = User.DB.insert(data)
        return self._doc_id
    
    def delete(self) -> int:
        """Delete the user from the database
    
        Deletes the user data if exists in DB and resets the instance's doc_id.
        
        Returns:
            int : The deleted document IDs if existed or None
        """
        # Check if user already exists in DB by name
        existing = self.db_instance() 
        self._doc_id = None        
        if existing :            
            return User.DB.remove(doc_ids=[existing.doc_id])[0]            
        return None


def get_all_users() -> list[User]:
    """Retrieve all users from the database
    
    Returns:
        list[User]: List of all User instances stored in the database with their doc_id
    """
    return [User(**user, doc_id=user.doc_id) for user in User.DB.all()]


if __name__ == "__main__" :
    from faker import Faker
    
    for _ in range(100):
        fake = Faker("fr_FR")
        user = User(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            phone_number=fake.phone_number(),
            address=fake.address()
        )
        user.save()
        print("-"*20)

    # martin = User("Martin", "Voisin")
    # print(martin.save())
    # martin.phone_number = "0123456789"
    # print(martin.phone_number)
    # print(martin.save())
    print(get_all_users())
