from enum import Enum
from typing import Optional
import os
import json

from validators import PasswordValidator

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import button_dialog
from prompt_toolkit.completion import WordCompleter
import requests


def cls():
    os.system("cls||clear")


class StateVal(Enum):
    START = (0,)
    LOGIN = (1,)
    REGISTER = (2,)
    AUTHED = (3,)
    QUIT = (4,)
    CHAT = (5,)


URL = "http://127.0.0.1:8000/"  # TODO: Move this


class ClientInterface:
    _username: Optional[str] = None
    _password: Optional[str] = None
    _state: StateVal = StateVal.START
    _contacts: list[str] = []
    _current_chat: Optional[str] = None

    def __init__(self):
        self._state_map: dict[StateVal] = {
            StateVal.START: self.start,
            StateVal.LOGIN: self.login,
            StateVal.REGISTER: self.register,
            StateVal.AUTHED: self.menu,
            StateVal.CHAT: self.chat,
        }

    def run(self) -> bool:
        if self._state in self._state_map:
            cls()
            self._state = self._state_map[self._state]()
            return True

        return False

    def start(self) -> StateVal:
        result = button_dialog(
            title="Welcome to Dexter Messaging",
            text="Choose an option",
            buttons=[
                ("Login", StateVal.LOGIN),
                ("Register", StateVal.REGISTER),
                ("Quit", StateVal.QUIT),
            ],
        ).run()

        return result

    def auth(self, validate=False) -> tuple[str, str]:
        username = prompt("Username: ")

        if validate:
            password = prompt(
                "Password: ",
                is_password=True,
                validator=PasswordValidator(),
            )
        else:
            password = prompt("Password: ", is_password=True)

        return username, password

    def login(self) -> StateVal:
        username, password = self.auth()

        data = {
            "username": username,
            "password": password,
        }

        requests.post(f"{URL}/message/login", json=data)

        self._username = username
        self._password = password

        self.get_contacts()

        return StateVal.AUTHED

    def get_contacts(self):
        result = requests.post(
            f"{URL}/message/get_contacts",
            json={
                "username": self._username,
                "password": self._password,
            },
        )

        self._contacts = [
            contact["contact__username"]
            for contact in json.loads(result.json()["data"])
        ]

    def register(self):
        username, password = self.auth(validate=True)

        data = {
            "username": username,
            "password": password,
        }

        requests.post(f"{URL}/message/register", json=data)
        return StateVal.START

    def bottom_toolbar(self):
        return HTML(
            f'Logged in as <b><style bg="ansired">{self._username}</style></b>',
        )

    def menu(self):
        if self._contacts:
            print("Contacts: ")

            for contact in self._contacts:
                print(f"   - {contact}")

        print("Options:")
        print("    To chat with a user, type their username")
        print("    1. Add username to contacts")
        print("    2. Remove username from contacts")
        print("    3. Logout")

        username_completer = WordCompleter(self._contacts)
        res = prompt(
            "> ",
            bottom_toolbar=lambda: self.bottom_toolbar(),
            completer=username_completer,
        )

        if res == "1":
            username = prompt(
                "Enter username: ",
                bottom_toolbar=lambda: self.bottom_toolbar(),
            )

            requests.post(
                f"{URL}/message/add_contact",
                json={
                    "username": self._username,
                    "password": self._password,
                    "target_user": username,
                },
            )
            self.get_contacts()
            return StateVal.AUTHED
        elif res == "2":
            username = prompt(
                "Enter username: ",
                bottom_toolbar=lambda: self.bottom_toolbar(),
                completer=username_completer,
            )

            requests.post(
                f"{URL}/message/remove_contact",
                json={
                    "username": self._username,
                    "password": self._password,
                    "target_user": username,
                },
            )
            self.get_contacts()
            return StateVal.AUTHED
        elif res == "3":
            return StateVal.START
        elif res:
            self._current_chat = res
            return StateVal.CHAT
        return StateVal.AUTHED

    def chat(self):
        if self._current_chat:
            print("Chatting with: ", self._current_chat, "\n\n\n")

            result = requests.post(
                f"{URL}/message/get_direct_messages",
                json={
                    "username": self._username,
                    "password": self._password,
                    "target_user": self._current_chat,
                },
            )

            messages_json = result.json()["data"]
            messages = json.loads(messages_json)

            for message in messages:
                print(
                    message["author_id__username"]
                    + "  "
                    + message["sent_date"]
                    + ": "
                    + message["text"]
                    + f" [{'SEEN' if message['seen'] else 'NOT SEEN'}]",
                )

            message = prompt("> ", bottom_toolbar=lambda: self.bottom_toolbar())

            if message:
                requests.post(
                    f"{URL}/message/send_direct_message",
                    json={
                        "username": self._username,
                        "password": self._password,
                        "target_user": self._current_chat,
                        "message": message,
                    },
                )

            return StateVal.CHAT


def main():
    interface = ClientInterface()

    while interface.run():
        pass


if __name__ == "__main__":
    main()
