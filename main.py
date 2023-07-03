from collections import UserDict
from datetime import date
import pickle


class Field:
    def __init__(self, value=None):
        self._value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def __str__(self):
        return str(self._value)


class Name(Field):
    pass


class Phone(Field):
    @Field.value.setter
    def value(self, new_value):
        # Add any additional validation or formatting for the phone number
        self._value = new_value


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)
        self._value = None
        if value:
            self.value = value

    @Field.value.setter
    def value(self, new_value):
        try:
            parts = new_value.split('-')
            day = int(parts[0])
            month = int(parts[1])
            self._value = date.today().replace(day=day, month=month)
        except (ValueError, IndexError):
            raise ValueError("Invalid birthday format. Please use 'dd-mm' format.")

    def __str__(self):
        return str(self._value)


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if str(p) == old_phone:
                p.value = new_phone
                break

    def days_to_birthday(self):
        if self.birthday.value:
            today = date.today()
            next_birthday = date(today.year, self.birthday.value.month, self.birthday.value.day)
            if next_birthday < today:
                next_birthday = date(today.year + 1, self.birthday.value.month, self.birthday.value.day)
            days_left = (next_birthday - today).days
            return days_left
        return None

    def __str__(self):
        return f"Name: {self.name}, Phones: {', '.join(map(str, self.phones))}, Birthday: {self.birthday}"


class AddressBook(UserDict):
    def __iter__(self):
        return AddressBookIterator(self.data.values())

    def save_to_file(self, filename):
        with open(filename, "wb") as file:
            pickle.dump(self.data, file)

    @classmethod
    def load_from_file(cls, filename):
        with open(filename, "rb") as file:
            data = pickle.load(file)
        address_book = cls()
        address_book.data = data
        return address_book

    def search(self, query):
        results = []
        for record in self.data.values():
            if query.lower() in record.name.value.lower() or any(query in phone.value for phone in record.phones):
                results.append(record)
        return results


class AddressBookIterator:
    def __init__(self, data):
        self.data = data
        self.index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < len(self.data):
            record = list(self.data)[self.index]
            self.index += 1
            return record
        raise StopIteration


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found"
        except ValueError:
            return "Invalid input"
        except IndexError:
            return "Invalid command"
    return inner


@input_error
def add_contact(command):
    # Розділимо рядок команди на ім'я та номер телефону
    name, phone = command.split(' ', 1)
    # Збережемо контакт у словник
    contacts[name] = phone
    return "Contact added successfully"


@input_error
def change_contact(command):
    # Розділимо рядок команди на ім'я та номер телефону
    name, phone = command.split(' ', 1)
    # Змінимо номер телефону для заданого контакту
    contacts[name] = phone
    return "Contact updated successfully"


@input_error
def show_phone(command):
    # Виділимо ім'я контакту з команди
    name = command.strip()
    # Отримаємо номер телефону для заданого контакту
    phone = contacts[name]
    return f"The phone number for {name} is {phone}"


def show_all_contacts():
    # Виведемо всі контакти
    if not contacts:
        return "No contacts found"
    else:
        output = ""
        for name, phone in contacts.items():
            output += f"{name}: {phone}\n"
        return output.strip()


def main():
    print("How can I help you?")
    while True:
        command = input("> ").lower()
        if command == "hello":
            print("How can I help you?")
        elif command.startswith("add"):
            result = add_contact(command[4:].strip())
            print(result)
        elif command.startswith("change"):
            result = change_contact(command[7:].strip())
            print(result)
        elif command.startswith("phone"):
            result = show_phone(command[6:].strip())
            print(result)
        elif command == "show all":
            result = show_all_contacts()
            print(result)
        elif command in ["good bye", "close", "exit"]:
            print("Good bye!")
            break
        else:
            print("Invalid command. Please try again.")


# Словник для зберігання контактів
contacts = {}


# Запуск основної функції
if __name__ == '__main__':
    main()
