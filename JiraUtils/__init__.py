from pathlib import Path
import atexit

import requests

from rich import print
from rich.prompt import Prompt

from JiraUtils.models import SessionResponse

def _initialise_sessions() -> tuple[requests.Session, dict[str, str]]:
    # Set the initial headers
    HEADERS={
        'content-type': 'application/json; charset=utf-8',
        'Accept': 'application/json; charset=utf-8',
    }

    # Get the username
    username = 'steve'

    # Get the password
    secrets_file = Path('secrets.txt')

    if secrets_file.exists():
        # Read the password from the secrets file
        with secrets_file.open() as f:
            password = f.read().strip()
    else:
        # Prompt for the password
        password = Prompt.ask('Enter password', password=True)

        # Write the password to the secrets file
        with secrets_file.open('w') as f:
            f.write(password)

    # Login to Jira
    response = requests.post(
        'http://macmini2:8100/rest/auth/1/session/',
        headers=HEADERS,
        json={
            'username': username,
            'password': password,
        },
    )

    # Delete the password
    del password

    if response.status_code == 200:
        # Update the headers with the session cookie
        session = SessionResponse(**response.json()).session
        HEADERS['cookie'] = f'{session.name}={session.value}'

        # Get the user details
        response = requests.get(f'{base_url}/rest/api/2/myself', headers=HEADERS)

        # Check the response
        if response.status_code == 200:
            # Get the user details
            userdetails = response.json()
        else:
            # Print an error message and exit
            print(f'[red]User Details Error {response.status_code}, Reason: {response.reason}[/red]')
            exit()

        # Print a success message
        print(f'[green]Logged in as {userdetails["name"]}[/green]')
    else:
        # Print an error message and exit
        print(f'[red]Login Error {response.status_code}, Reason: {response.reason}[/red]')
        exit()

    # Create a requests session with the updated headers
    requests_session = requests.Session()
    requests_session.headers.update(HEADERS)

    def logout() -> None:
        # Log out
        response = requests_session.delete(
            'http://macmini2:8100/rest/auth/1/session/',
        )

        if response.status_code == 204:
            # Print a success message
            print('[green]Logged out[/green]')
        else:
            # Print an error message
            print(f'[red]Logout Error {response.status_code}, Reason: {response.reason}[/red]')

        # Close the requests session
        requests_session.close()
        print('[green]Closed requests session[/green]')

    # Register the logout function to run at exit
    atexit.register(logout)

    # Return the requests session and headers
    return requests_session, HEADERS

# Set the base url
base_url = 'http://macmini2:8100'

# Initialise the requests session and headers
requests_session, headers = _initialise_sessions()

from JiraUtils.Issues import get_issue, get_issue_async, create_issue, create_issue_link

# Export the public functions and variables
__all__ = [
    'requests_session',
    'headers',
    'base_url',
    'get_issue',
    'get_issue_async',
    'create_issue',
    'create_issue_link',
]
