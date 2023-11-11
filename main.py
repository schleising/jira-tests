import asyncio

from JiraUtils import get_issue, get_issue_async, create_issue, create_issue_link
from JiraUtils.models import IssueType

async def get_issues():
    # Create a task group
    async with asyncio.TaskGroup() as task_group:
        # Create a task for each issue
        tasks = [task_group.create_task(get_issue_async(f'MT-{i}')) for i in range(4, 8)]

        # Add a callback to each task to print the result
        for task in tasks:
            task.add_done_callback(lambda t: print(t.result()))

def create_issues() -> None:
    # Create an empty list to store the issue keys
    issue_keys: list[str] = []

    # Create 10 issues
    for i in range(10):
        issue_key = create_issue(
            issue_type='Bug',
            summary=f'Test Issue {i}',
            description=f'This is test issue number {i} 😍🐶',
        )

        # Add the issue key to the list
        if issue_key is not None:
            issue_keys.append(issue_key)

            # Print the issue key
            print(f'Created issue {issue_key}')

def create_epic_or_story(type: IssueType, summary: str, desciption: str) -> str | None:
    # Get the epic name if the issue type is an Epic
    if type == IssueType.epic:
        epic_name = summary
    else:
        epic_name = None

    # Create an issue of the specified type
    issue_key = create_issue(
        issue_type=type,
        summary=summary,
        description=desciption,
        epic_name=epic_name,
    )

    # Print the issue key
    print(f'Created issue {issue_key}')

    # Return the issue key
    return issue_key

def main():
    # Get an issue synchronously
    # issue = get_issue('MT-1')

    # if issue is not None:
    #     print(f'Key: {issue.key}')
    #     print(f'Issue Type: {issue.issue_type}')
    #     print(f'Summary: {issue.summary}')
    #     print(f'Description: {issue.description}')     
    #     print(f'Status: {issue.status}')   

    # # Print the issue
    # print(issue)

    # Create an Epic
    epic_key = create_epic_or_story(
        type=IssueType.epic,
        summary='Test Epic',
        desciption='This is a test epic 😍🐶',
    )

    # Check if the Epic was created
    if epic_key is None:
        # Print an error message and exit
        print('[red]Failed to create Epic[/red]')
        exit()

    # Create a Story
    story_key = create_epic_or_story(
        type=IssueType.story,
        summary='Test Story',
        desciption='This is a test story 😍🐶',
    )

    # Check if the Story was created
    if story_key is None:
        # Print an error message and exit
        print('[red]Failed to create Story[/red]')
        exit()

    # Create a link between the Epic and Story
    link_created = create_issue_link(outward_issue_key=epic_key, inward_issue_key=story_key)

    # Check if the link was created
    if not link_created:
        # Print an error message and exit
        print('[red]Failed to create link[/red]')
        exit()
    else:
        # Print a success message
        print('[green]Link created[/green]')

if __name__ == '__main__':
    # Run the main function
    main()

    # Run the async function
    # asyncio.run(get_issues())

    # Create some issues
    # create_issues()
