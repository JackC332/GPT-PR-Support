import os
import openai
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

    # Get PR information
    repo_name = os.getenv("GITHUB_REPOSITORY")
    pr_number = int(os.getenv("GITHUB_PULL_NUMBER"))
    repo = gh_client.get_repo(repo_name)
    pr = repo.get_pull(pr_number)

    # Extract PR information and send it to OpenAI API
    prompt = f"Review this code for improvements and security vulnerabilities:\n\n{pr.diff_url}"

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
        pr.create_issue_comment(f"🤖 ChatGPT Code Review:\n\n{feedback}")


if __name__ == "__main__":
    main()
