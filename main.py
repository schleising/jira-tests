import asyncio

from JiraUtils import get_issue, get_issue_async

async def get_issues():
    # Create a task group
    async with asyncio.TaskGroup() as task_group:
        # Create a task for each issue
        tasks = [task_group.create_task(get_issue_async('MT-1')) for _ in range(10)]

        # Add a callback to each task to print the result
        for task in tasks:
            task.add_done_callback(lambda t: print(t.result()))

def main():
    # Get an issue synchronously
    issue = get_issue('MT-1')

    if issue is not None:
        print(f'Key: {issue.key}')
        print(f'Project: {issue.project.name}')
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
