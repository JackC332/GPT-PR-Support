import os
import openai
import urllib.request
from github import Github

# This is the main entrypoint to the action

def main():
    # Get input parameters from the workflow
    github_token = os.getenv("GITHUB_TOKEN")
    openai_api_key = os.getenv("OPEN_API_KEY")

    # Initialize GitHub API client
    gh_client = Github(github_token)

    # Initialize OpenAI API client
    openai.api_key = openai_api_key

    # Get PR information and extract relevant lines of code
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number = int(os.getenv("GITHUB_PULL_NUMBER"))
    repo = gh_client.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    # Extract only the relevant lines of code from the diff
    file_name = pr.get_files()[0].filename
    file_url = pr.get_files()[0].raw_url
    raw_file_url = file_url.replace('/raw/', '/').replace(f'/{file_name}', '')

    with urllib.request.urlopen(file_url) as f:
        file_content = f.read().decode('utf-8')

    lines = file_content.split("\n")
    code_lines = [line for line in lines if line.startswith("+")]

    # Send relevant lines of code to the OpenAI API
    prompt = "Review the following lines of code for improvements and security vulnerabilities:\n\n" + "\n".join(code_lines)

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7,
    )



    # Post feedback as a comment on the PR
    feedback = response.choices[0].text.strip()

    if feedback:
        repo_name = os.getenv("GITHUB_REPOSITORY")
        pr_number = int(os.getenv("GITHUB_PULL_NUMBER"))
        repo = gh_client.get_repo(repo_name)
        pr = repo.get_pull(pr_number)
        file_name = pr.get_files()[0].filename
        file_sha = pr.get_files()[0].sha
        line_numbers = [index + 1 for index, line in enumerate(lines) if line in code_lines]
        comment_body = "🤖 ChatGPT Code Review:\n\n" + feedback

        for line_number in line_numbers:
            pr.create_review_comment(comment_body, file_name, line_number, commit_id=file_sha)


if __name__ == "__main__":
    main()
