import requests
from datetime import datetime, timedelta
import time

# GitHub repository details
repo_owner = "your_username"
repo_name = "your_repository"
branch_name = "main"

# GitHub personal access token
token = "your_personal_access_token"

# Global headers
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github.v3+json",
}


# Function to create a new commit
def create_commit():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Automated commit on {current_time}"

    # API endpoint for creating a new commit
    commit_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/commits"
    ref_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/heads/{branch_name}"

    # Sample commit data
    commit_data = {
        "message": commit_message,
        "tree": "master",
        "parents": [],
    }

    # Make the API request to create a new commit
    response = requests.post(commit_url, json=commit_data, headers=headers)

    if response.status_code == 201:
        print(f"Commit created successfully: {commit_message}")
        commit_sha = response.json()["sha"]

        # Update the branch reference
        ref_data = {
            "sha": commit_sha,
            "force": False,
        }
        requests.patch(ref_url, json=ref_data, headers=headers)

        return commit_sha
    else:
        print(f"Error creating commit: {response.status_code}")
        return None


# Main functionss
def main():
    # Create a new commit
    commit_sha = create_commit()

    if commit_sha:
        print("Pushing changes to GitHub...")

        # API endpoint for pushing changes
        push_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/git/refs/heads/{branch_name}/"

        # Sample data for pushing changes
        push_data = {
            "force": False,
            "sha": commit_sha,
        }

        # Make the API request to push changes
        response = requests.patch(push_url, json=push_data, headers=headers)

        if response.status_code == 200:
            print("Changes pushed successfully.")
        else:
            print(f"Error pushing changes: {response.status_code}")


if __name__ == "__main__":
    # Run the script at a specific time every day
    scheduled_time = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)

    while True:
        current_time = datetime.now()

        if current_time >= scheduled_time:
            main()
            # Update scheduled time for the next day
            scheduled_time += timedelta(days=1)

        # Sleep for a short interval (e.g., 1 minute)
        time.sleep(60)
