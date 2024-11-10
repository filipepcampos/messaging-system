# Mini Messaging System

This project is divided into two main compontents, `django-backend` and
`user-cli`.

To run the backend simply run the following commands from their respective subdirectories:

```
python3 -m venv .venv
source venv .venv
pip install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

To run the CLI:

```
python3 -m venv .venv
source venv .venv
pip install -r requirements.txt
python3 main.py
```

## Quick overview

The backend is based on Django with a simple authentication system.
Since the backend on a real use scenario would most likely be used through a web interface
the authentication is kept simple, by providing username & password on every request. This avoids implementing a token system for the CLI to the session state.
On a real use-case django automatically stores session tokens on the browser.

The db is kept simple and includes: User, Message, Channel and Contact.

Features:

- Authentication
- Adding Contacts so the user doesn't have to remember usernames
- Seen / Not seen receipts for messages

The main feature that remained implemented was a Group Chat functionality. But the schema was designed for this in mind and should be easily extendable for that use case. A direct message is a specific case of a Channel with only two users.

Other features:

- Automatically showing new messages on the CLI. Currently to refresh the message list the user has to click Enter.
- Containarization, due to time constraints this wasn't done but should be easily done.
- Adding Tests, due to the time constraints they were not added since the bare minimum functionality for the prototype had to be implemented first.
