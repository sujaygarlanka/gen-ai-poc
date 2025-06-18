#!/usr/bin/env python3

import argparse
import subprocess
import requests
import json
import os
import sys
from datetime import datetime

def run_command(command, check=True):
    """Run a shell command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {command}")
        print(f"Error: {e.stderr}")
        return None

def create_branch(branch_name):
    """Create a new branch from master."""
    print(f"Creating branch: {branch_name}")
    
    # Ensure we're on master and up to date
    run_command("git checkout master")
    run_command("git pull origin master")
    
    # Create and checkout new branch
    run_command(f"git checkout -b {branch_name}")
    return True

def call_amazon_q_agent(prompt):
    """Call Amazon Q CLI agent with the given prompt."""
    print(f"Calling Amazon Q agent with prompt: {prompt}")
    
    # This is a placeholder - replace with actual Amazon Q CLI command
    # Example: aws q generate-code --prompt "your prompt here"
    command = f'aws q generate-code --prompt "{prompt}"'
    
    result = run_command(command)
    if result:
        print("Amazon Q agent response received")
        return result
    else:
        print("Failed to get response from Amazon Q agent")
        return None

def commit_changes(commit_message):
    """Commit any changes made by the agent."""
    print("Committing changes...")
    
    # Add all changes
    run_command("git add .")
    
    # Commit with the provided message
    run_command(f'git commit -m "{commit_message}"')
    return True

def push_branch(branch_name):
    """Push the branch to GitHub."""
    print(f"Pushing branch {branch_name} to GitHub...")
    
    result = run_command(f"git push origin {branch_name}")
    return result is not None

def push_current_branch():
    """Push the current branch to GitHub."""
    current_branch = run_command("git branch --show-current")
    if not current_branch:
        print("Error: Could not determine current branch")
        return False
    
    print(f"Pushing current branch {current_branch} to GitHub...")
    result = run_command(f"git push origin {current_branch}")
    return result is not None

def create_pull_request(branch_name, title, description, github_token, repo_owner, repo_name):
    """Create a pull request using GitHub API."""
    print(f"Creating pull request for branch: {branch_name}")
    
    url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/pulls"
    
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    
    data = {
        "title": title,
        "body": description,
        "head": branch_name,
        "base": "master"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        
        pr_data = response.json()
        print(f"Pull request created successfully!")
        print(f"PR URL: {pr_data['html_url']}")
        return pr_data['html_url']
        
    except requests.exceptions.RequestException as e:
        print(f"Error creating pull request: {e}")
        return None

def get_github_info():
    """Extract GitHub repository info from git remote."""
    remote_url = run_command("git remote get-url origin")
    if not remote_url:
        print("Error: Could not get git remote URL")
        return None, None
    
    # Handle both HTTPS and SSH URLs
    if remote_url.startswith("https://"):
        # https://github.com/owner/repo.git
        parts = remote_url.replace("https://github.com/", "").replace(".git", "").split("/")
    else:
        # git@github.com:owner/repo.git
        parts = remote_url.replace("git@github.com:", "").replace(".git", "").split("/")
    
    if len(parts) >= 2:
        return parts[0], parts[1]
    else:
        print("Error: Could not parse GitHub repository info")
        return None, None

def update_command(prompt, commit_message):
    """Update command: call Amazon Q agent and push changes to current branch."""
    print("🔄 Update mode: Working on current branch")
    
    # Check if we're in a git repository
    if not run_command("git rev-parse --git-dir"):
        print("Error: Not in a git repository")
        return False
    
    # Check if we have uncommitted changes
    status = run_command("git status --porcelain")
    if status:
        print("Warning: You have uncommitted changes. Consider committing them first.")
        response = input("Continue anyway? (y/N): ")
        if response.lower() != 'y':
            print("Update cancelled")
            return False
    
    try:
        # Step 1: Call Amazon Q agent
        agent_response = call_amazon_q_agent(prompt)
        if not agent_response:
            print("Failed to get response from Amazon Q agent")
            return False
        
        # Step 2: Check if any changes were made
        status_after = run_command("git status --porcelain")
        if not status_after:
            print("No changes detected after Amazon Q agent response")
            return True
        
        # Step 3: Commit changes
        if not commit_changes(commit_message):
            print("Failed to commit changes")
            return False
        
        # Step 4: Push to current branch
        if not push_current_branch():
            print("Failed to push changes")
            return False
        
        print("✅ Update completed successfully!")
        return True
        
    except KeyboardInterrupt:
        print("\nUpdate cancelled by user")
        return False
    except Exception as e:
        print(f"Unexpected error during update: {e}")
        return False

def create_command(prompt, branch_name, commit_message, pr_title, pr_description, github_token):
    """Create command: full workflow with new branch and PR."""
    print("🆕 Create mode: Creating new branch and pull request")
    
    # Get GitHub repository info
    repo_owner, repo_name = get_github_info()
    if not repo_owner or not repo_name:
        return False
    
    try:
        # Step 1: Create new branch
        if not create_branch(branch_name):
            print("Failed to create branch")
            return False
        
        # Step 2: Call Amazon Q agent
        agent_response = call_amazon_q_agent(prompt)
        if not agent_response:
            print("Failed to get response from Amazon Q agent")
            return False
        
        # Step 3: Commit changes
        if not commit_changes(commit_message):
            print("Failed to commit changes")
            return False
        
        # Step 4: Push branch
        if not push_branch(branch_name):
            print("Failed to push branch")
            return False
        
        # Step 5: Create pull request
        pr_url = create_pull_request(branch_name, pr_title, pr_description, github_token, repo_owner, repo_name)
        
        if pr_url:
            print(f"\n✅ Success! Pull request created: {pr_url}")
            return True
        else:
            print("Failed to create pull request")
            return False
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="CLI tool to work with Amazon Q agent and GitHub")
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create command (original functionality)
    create_parser = subparsers.add_parser('create', help='Create new branch, call Amazon Q agent, and create PR')
    create_parser.add_argument("prompt", help="The prompt to send to Amazon Q agent")
    create_parser.add_argument("--branch-name", help="Name for the new branch (default: auto-generated)")
    create_parser.add_argument("--commit-message", help="Commit message (default: auto-generated)")
    create_parser.add_argument("--pr-title", help="Pull request title (default: auto-generated)")
    create_parser.add_argument("--pr-description", help="Pull request description")
    create_parser.add_argument("--github-token", help="GitHub personal access token (or set GITHUB_TOKEN env var)")
    
    # Update command (new functionality)
    update_parser = subparsers.add_parser('update', help='Call Amazon Q agent and push changes to current branch')
    update_parser.add_argument("prompt", help="The prompt to send to Amazon Q agent")
    update_parser.add_argument("--commit-message", help="Commit message (default: auto-generated)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    if args.command == 'update':
        # Generate commit message if not provided
        commit_message = args.commit_message or f"Update from Amazon Q agent: {args.prompt[:50]}..."
        
        success = update_command(args.prompt, commit_message)
        sys.exit(0 if success else 1)
    
    elif args.command == 'create':
        # Get GitHub token from args or environment
        github_token = args.github_token or os.getenv("GITHUB_TOKEN")
        if not github_token:
            print("Error: GitHub token required. Set GITHUB_TOKEN environment variable or use --github-token")
            sys.exit(1)
        
        # Generate values if not provided
        branch_name = args.branch_name or f"feature/amazon-q-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        commit_message = args.commit_message or f"Apply changes from Amazon Q agent: {args.prompt[:50]}..."
        pr_title = args.pr_title or f"Feature: {args.prompt[:50]}..."
        pr_description = args.pr_description or f"Changes generated by Amazon Q agent based on prompt: {args.prompt}"
        
        success = create_command(args.prompt, branch_name, commit_message, pr_title, pr_description, github_token)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 