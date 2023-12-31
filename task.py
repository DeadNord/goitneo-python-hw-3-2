from collections import UserDict
from datetime import datetime
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

    def __eq__(self, other):
        return self.value == other


class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    def __hash__(self):
        return hash(self.value)


class Phone(Field):
    def __init__(self, value):
        if value.isdigit() and len(value) == 10:
            super().__init__(value)
        else:
            raise ValueError("Invalid phone number")


class Birthday(Field):
    DATE_FORMAT = "%d.%m.%Y"

    def __init__(self, value):
        date_obj = datetime.strptime(value, self.DATE_FORMAT)
        super().__init__(date_obj.date())

    def __lt__(self, other):
        if isinstance(other, Birthday):
            return self.value < other.value

    def __gt__(self, other):
        if isinstance(other, Birthday):
            return self.value > other.value


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phone = ""
        self.birthday = "None"

    def add_phone(self, value):
        self.phone = Phone(value)

    def edit_phone(self, new_phone):
        self.phone = new_phone
        return f"Phone number updated to {new_phone}"

    def __str__(self):
        return (
            f"Contact name: {self.name}, phone: {self.phone}, birthday: {self.birthday}"
        )


class AddressBook(UserDict):
    def __init__(self):
        self.data = {}

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    def read_from_file(self, filename):
        try:
            with open(filename, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            self.data = {}

    def add_record(self, record):
        self.data[record.name] = record

    def find(self, name):
        res = self.data.get(name)
        if res:
            return res
        else:
            raise ValueError("Contact not found")

    def add_birthday(self, name, birthday):
        try:
            contact = self.find(name)
        except ValueError:
            print("Contact not found")
        else:
            contact.birthday = Birthday(birthday)
            print("Birthday added.")

    def show_birthday(self, name):
        for i in self.data:
            if i == name:
                return self.data[i].birthday
            else:
                raise ValueError("Contact not found")

    def birthdays(self):
        birthday_dict = {}
        for user in sorted(self.data.values(), key=lambda x: x.birthday):
            current_date = datetime.now().date()
            next_year = current_date.year + 1
            birthday = user.birthday
            if birthday == "None":
                continue
            birthday = birthday.value
            birthday_this_year = birthday.replace(year=current_date.year)
            if birthday_this_year < current_date:
                birthday_this_year = birthday.replace(year=next_year)

            delta_days = (birthday_this_year - current_date).days

            if delta_days <= 5:
                weekday = birthday_this_year.strftime("%A")
                if weekday in ("Saturday", "Sunday"):
                    weekday = "Monday"
                if weekday in birthday_dict:
                    birthday_dict[weekday] += [user.name]
                else:
                    birthday_dict[weekday] = [user.name]

        res = "\nAll Birthdays:\n"
        for day, names in birthday_dict.items():
            res += f"{day}: {', '.join(map(str, names))}\n"
        return res
