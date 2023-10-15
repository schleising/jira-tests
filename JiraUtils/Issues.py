from pydantic import ValidationError
from rich import print
import aiohttp

from JiraUtils import base_url, requests_session, headers
from JiraUtils.models import Issue, Fields, NameField, IdField, CreateIssueResponse, CreateIssueErrorResponse

def get_issue(issue_key: str) -> Issue | None:
    '''Get an issue synchronously
    
    Parameters:
    - `issue_key`: The issue key to get
    
    Returns:
    - `Issue | None`: The issue if the request was successful, otherwise None
    
    Raises:
    - `ValidationError`: If the issue is invalid
    
    Example:
    ```python
    from JiraUtils import get_issue
    
    issue = get_issue('MT-1')
    print(issue)
    ```
    
    Output:
    ```console
    MT-1: Test Issue
    ```
    '''

    # Request an issue
    response = requests_session.get(
        f'{base_url}/rest/api/2/issue/{issue_key}',
    )

    if response.status_code == 200:
        # Return the issue if the request was successful
        try:
            issue = Issue(**response.json())
            return issue
        except ValidationError as e:
            print(f'[red]Issue Validation Error: {e}[/red]')
            print(f'{response.json()}')
            return None
    else:
        # Return None if the request was unsuccessful
        print(f'[red]Get Issue Error: {response.status_code}, Reason: {response.reason}[/red]')
        return None

async def get_issue_async(issue_key: str) -> Issue | None:
    '''Get an issue asynchronously

    Parameters:
    - `issue_key`: The issue key to get

    Returns:
    - `Issue | None`: The issue if the request was successful, otherwise None

    Raises:
    - `ValidationError`: If the issue is invalid

    Example:
    ```python
    import asyncio

    from JiraUtils import get_issue_async

    async def get_issues():
    
        # Create a task group
        async with asyncio.TaskGroup() as task_group:
            # Create a task for each issue
            tasks = [task_group.create_task(get_issue_async('MT-1')) for _ in range(10)]

            # Add a callback to each task to print the result
            for task in tasks:
                task.add_done_callback(lambda t: print(t.result()))
    ```
    '''

    # Create an aiohttp session
    async with aiohttp.ClientSession(headers=headers) as aiohttp_session:
        # Request an issue
        async with aiohttp_session.get(
            f'{base_url}/rest/api/2/issue/{issue_key}',
        ) as response:
            if response.status == 200:
                # Return the issue if the request was successful
                try:
                    issue = Issue(**await response.json())
                    return issue
                except ValidationError as e:
                    print(f'[red]Issue Validation Error for {issue_key}: {e}[/red]')
                    print(f'{await response.json()}')
                    return None
            else:
                # Return None if the request was unsuccessful
                print(f'[red]Get Issue Error: {response.status}, Reason: {response.reason}[/red]')
                return None

def create_issue(issue_type: str, summary: str, description: str) -> str | None:
    '''Create an issue in Jira

    Parameters:
    - `issue_type`: The issue type to create
    - `summary`: The summary of the issue
    - `description`: The description of the issue

    Returns:
    - `str | None`: The issue key if the request was successful, otherwise None

    Raises:
    - `ValidationError`: If the issue is invalid

    Example:
    ```python
    from JiraUtils import create_issue

    issue_key = create_issue(
        issue_type='Bug',
        summary='Test Issue',
        description='This is a test issue 😍🐶',
    )
    ```
    '''
    # Create the pydantic fields
    fields = Fields(
        project=IdField(id = '10000'),
        issuetype=NameField(name = issue_type),
        summary=summary,
        description=description,
    )

    # Create the pydantic issue
    issue = Issue(fields=fields)

    # Create the issue in Jira
    response = requests_session.post(
        f'{base_url}/rest/api/2/issue/',
        json=issue.model_dump(by_alias=True),
    )

    # Check if the request was successful
    if response.status_code == 201:
        # Create a response model
        response_model = CreateIssueResponse(**response.json())

        # Return the issue key
        return response_model.key
    else:
        # Print an error message and return None
        print(f'[red]Create Issue Error: {response.status_code}, Reason: {response.reason}[/red]')

        # Create an error response model
        response_model = CreateIssueErrorResponse(**response.json())

        # Print the error messages
        for error_message in response_model.errorMessages:
            print(f'[red]{error_message}[/red]')

        # Print the errors
        for key, value in response_model.errors.items():
            print(f'[red]{key}: {value}[/red]')

        return None
