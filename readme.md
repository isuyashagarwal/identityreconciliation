# Identity Reconciliation

Bitespeed Backed Task for SDE 1 Position.

Backend Framework: Python with Flask

Database: Sqlite

## Installation

- Create a virtual environment and clone the repository
- Install the dependencies mentioned in the requirements.txt list

```
pip3 install -r requirements.txt
```

## Usage

/identity endpoint allows POST requests.

Open testcases.json and try hitting the endpoint with the sample test cases or create your own.

## Problem Understanding

- A user is only created when we have both email and phone number.

- A new user is created for every new email.

- The first user with a unique email/phone number combination is the primary user.

- All other users with same phone numbers are secondary user.

- A primary user can turn into a secondary user if a pre-existing primary user (say 'adam') is queried with a different phone number then all other users with this phone number, including the primary user(say 'james') become secondary users and point to **adam**.
