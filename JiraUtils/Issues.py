from pydantic import ValidationError
from rich import print
import aiohttp

from JiraUtils import base_url, requests_session, headers
from JiraUtils.models import Issue

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

# Get an issue asynchronously
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
                    print(f'[red]Issue Validation Error: {e}[/red]')
                    print(f'{await response.json()}')
                    return None
            else:
                # Return None if the request was unsuccessful
                print(f'[red]Get Issue Error: {response.status}, Reason: {response.reason}[/red]')
                return None
