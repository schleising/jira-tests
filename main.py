import asyncio

from JiraUtils import get_issue, get_issue_async, create_issue

async def get_issues():
    # Create a task group
    async with asyncio.TaskGroup() as task_group:
        # Create a task for each issue
        tasks = [task_group.create_task(get_issue_async('MT-1')) for _ in range(10)]

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

def main():
    # Get an issue synchronously
    issue = get_issue('MT-1')

    if issue is not None:
        print(f'Key: {issue.key}')
        print(f'Issue Type: {issue.issue_type.name}')
        print(f'Summary: {issue.summary}')
        print(f'Description: {issue.description}')        

    # Print the issue
    print(issue)

if __name__ == '__main__':
    # Run the main function
    main()

    # Run the async function
    asyncio.run(get_issues())

    # Create some issues
    create_issues()
