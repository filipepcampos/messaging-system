from enum import Enum
from typing import Optional

from validators import PasswordValidator

from prompt_toolkit import prompt
from prompt_toolkit.formatted_text import HTML
from prompt_toolkit.shortcuts import button_dialog
import requests


class StateVal(Enum):
    START = (0,)
    LOGIN = (1,)
    REGISTER = (2,)
    AUTHED = (3,)
    QUIT = (4,)


URL = "http://127.0.0.1:8000/"  # TODO: Move this


class ClientInterface:
    _username: Optional[str] = None
    _state: StateVal = StateVal.START

    def __init__(self):
        self._state_map: dict[StateVal] = {
            StateVal.START: self.start,
            StateVal.LOGIN: self.login,
            StateVal.REGISTER: self.register,
            StateVal.AUTHED: self.menu,
        }

    def run(self) -> bool:
        if self._state in self._state_map:
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

    def auth(self):
        username = prompt("Username: ")
        password = prompt("Password: ", is_password=True, validator=PasswordValidator())
        return username, password

    def login(self) -> StateVal:
        username, password = self.auth()

        data = {
            "username": username,
            "password": password,
        }

        result = requests.post(f"{URL}/message/login", json=data)
        print("Debug, ", result)

        if False:  # TODO: Send to server
            return StateVal.LOGIN

        self._username = username
        return StateVal.AUTHED

    def register(self):
        username, password = self.auth()

        data = {
            "username": username,
            "password": password,
        }

        result = requests.post(f"{URL}/message/register", json=data)

        print("Debug, ", result)

        return StateVal.START
        # TODO

    def menu(self):
        def bottom_toolbar():
            return HTML(
                f'Logged in as <b><style bg="ansired">{self._username}</style></b>',
            )

        _ = prompt("> ", bottom_toolbar=bottom_toolbar)


def main():
    interface = ClientInterface()

    while interface.run():
        pass


if __name__ == "__main__":
    main()
