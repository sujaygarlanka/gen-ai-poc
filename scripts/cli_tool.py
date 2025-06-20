#!/usr/bin/env python3

import argparse
import subprocess
import requests
import json
import os
import sys
import shutil
import re
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
    """Create a new branch from main."""
    print(f"Creating branch: {branch_name}")
    
    # Ensure we're on main and up to date
    run_command("git checkout main")
    run_command("git pull origin main")
    
    # Create and checkout new branch
    run_command(f"git checkout -b {branch_name}")
    return True

def call_amazon_q_agent(prompt):
    """Call Amazon Q CLI agent with the given prompt."""
    print(f"Calling Amazon Q agent with prompt")
    
    try:
        # Use subprocess to pipe the prompt to q chat and show output in real-time
        process = subprocess.Popen(
            ['q', 'chat', '--no-interactive', '--trust-all-tools'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Send the prompt
        process.stdin.write(prompt)
        process.stdin.close()
        
        # Read and display output in real-time
        print("\n" + "="*50)
        print("Amazon Q Agent Output:")
        print("="*50)
        
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                print(output.rstrip())
        
        # Wait for process to complete
        return_code = process.wait()
        
        print("="*50)
        print("Amazon Q Agent completed")
        print("="*50 + "\n")
        
        if return_code == 0:
            print("Amazon Q agent response received")
            return True
        else:
            stderr_output = process.stderr.read()
            if stderr_output:
                print(f"Error from Amazon Q agent: {stderr_output}")
            return None
            
    except Exception as e:
        print(f"Error calling Amazon Q agent: {e}")
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

def get_diff_from_main():
    """Get the git diff from main branch to current branch."""
    try:
        # Get diff from main to current branch
        diff_output = run_command("git diff main...HEAD")
        return diff_output
    except Exception as e:
        print(f"Error getting git diff from main: {e}")
        return None

def clean_ansi_codes(text):
    """Remove ANSI escape codes and color sequences from text."""
    if not text:
        return text
    
    # Remove ANSI color codes (e.g., [38;5;13m, [1m, [0m)
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    cleaned = ansi_escape.sub('', text)
    
    # Remove any remaining escape sequences
    cleaned = re.sub(r'\[[0-9;]*[a-zA-Z]', '', cleaned)
    
    # Clean up extra whitespace and newlines
    cleaned = re.sub(r'\n\s*\n\s*\n', '\n\n', cleaned)
    cleaned = cleaned.strip()
    
    return cleaned

def generate_pr_summary(diff_content):
    """Use Amazon Q agent to generate a markdown summary of the changes."""
    if not diff_content:
        return "Changes generated by Amazon Q agent"
    
    try:
        # Create the prompt
        prompt = """Generate a concise markdown summary of the following code changes for a pull request description. 
Focus on what was changed, why it was changed, and any important implementation details.

Please provide a well-formatted markdown summary suitable for a PR description."""
        
        print("Generating PR summary with Amazon Q agent...")
        
        # Use subprocess to pipe the diff content to q chat
        process = subprocess.Popen(
            ['q', 'chat', '--no-interactive', '--trust-all-tools'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Send the prompt and diff content
        input_data = f"{prompt}\n\nCode Changes:\n{diff_content}"
        stdout, stderr = process.communicate(input=input_data)
        
        if process.returncode == 0 and stdout:
            # Clean ANSI codes and ensure it's markdown
            summary = clean_ansi_codes(stdout.strip())
            if not summary.startswith('#'):
                summary = f"## Summary\n\n{summary}"
            return summary
        else:
            print(f"Error from q chat: {stderr}")
            return "Changes generated by Amazon Q agent"
            
    except Exception as e:
        print(f"Error generating PR summary: {e}")
        return "Changes generated by Amazon Q agent"

def create_pull_request(branch_name, title, repo_owner, repo_name):
    """Create a pull request using GitHub CLI."""
    print(f"Creating pull request for branch: {branch_name}")
    
    try:
        # Get diff from main to current branch
        diff_content = get_diff_from_main()
        
        # Generate PR summary using Amazon Q agent
        pr_summary = generate_pr_summary(diff_content)
        
        # Create PR body
        pr_body = f"{pr_summary}\n\n---\n*This PR was generated by Amazon Q agent*"
        
        # Use GitHub CLI to create pull request
        command = f'gh pr create --title "{title}" --body "{pr_body}" --base main --head {branch_name}'
        result = run_command(command)
        
        if result:
            print(f"Pull request created successfully!")
            # Extract PR URL from gh output
            if "https://github.com" in result:
                pr_url = result.strip()
                print(f"PR URL: {pr_url}")
                return pr_url
            else:
                print("Pull request created but couldn't extract URL")
                return True
        else:
            print("Failed to create pull request")
            return None
        
    except Exception as e:
        print(f"Error creating pull request: {e}")
        print("Note: Make sure GitHub CLI (gh) is installed and authenticated.")
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

def update_pr_body_with_diff(branch_name):
    """Update the PR body with the latest diff using Amazon Q agent."""
    try:
        # Get diff from main to current branch
        diff_content = get_diff_from_main()
        
        if not diff_content:
            print("No changes detected to update PR body")
            return False
        
        # Generate new PR summary using Amazon Q agent
        pr_summary = generate_pr_summary(diff_content)
        
        # Update the PR body using GitHub CLI
        print("Updating PR body with latest changes...")
        
        # Create temporary file with new body content
        import tempfile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as temp_file:
            temp_file.write(pr_summary)
            temp_file_path = temp_file.name
        
        # Update PR body using GitHub CLI
        command = f'gh pr edit {branch_name} --body-file {temp_file_path}'
        result = run_command(command)
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        if result:
            print("✅ PR body updated successfully!")
            return True
        else:
            print("Failed to update PR body")
            return False
            
    except Exception as e:
        print(f"Error updating PR body: {e}")
        return False

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
        
        # Step 5: Update PR body if branch has an open PR
        current_branch = run_command("git branch --show-current")
        if current_branch:
            print("Checking for open PR to update...")
            update_pr_body_with_diff(current_branch)
        
        print("✅ Update completed successfully!")
        return True
        
    except KeyboardInterrupt:
        print("\nUpdate cancelled by user")
        return False
    except Exception as e:
        print(f"Unexpected error during update: {e}")
        return False

def create_command(prompt, branch_name, commit_message):
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
        
        # Step 5: Create pull request using commit message as title
        pr_url = create_pull_request(branch_name, commit_message, repo_owner, repo_name)
        
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

def read_raml_file():
    """Read the API.raml file and return its contents."""
    try:
        with open('./temp/api.raml', 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print("Warning: api.raml file not found")
        return None
    except Exception as e:
        print(f"Error reading api.raml file: {e}")
        return None

def sanitize_raml_content(raml_content):
    """Sanitize RAML content to avoid shell command issues."""
    if not raml_content:
        return ""
    
    # Replace problematic characters
    sanitized = raml_content.replace('"', '\\"')  # Escape double quotes
    sanitized = sanitized.replace("'", "\\'")     # Escape single quotes
    sanitized = sanitized.replace('\n', '\\n')    # Escape newlines
    sanitized = sanitized.replace('\r', '\\r')    # Escape carriage returns
    
    # Truncate if too long to avoid command line length issues
    # if len(sanitized) > 8000:
    #     sanitized = sanitized[:8000] + "... [RAML content truncated]"
    
    return sanitized

def parse_raml_endpoints(raml_content):
    """Parse RAML content and extract all endpoints using YAML parsing."""
    endpoints = []
    
    if not raml_content:
        return endpoints
    
    try:
        import yaml
        
        # Parse RAML as YAML
        raml_dict = yaml.safe_load(raml_content)
        
        # Extract endpoints from parsed RAML
        if raml_dict and isinstance(raml_dict, dict):
            # Look for resources/endpoints in the RAML structure
            for key, value in raml_dict.items():
                if key.startswith('/') and isinstance(value, dict):
                    # This is an endpoint
                    path = key
                    
                    # Extract methods from the endpoint
                    for method_key, method_value in value.items():
                        if method_key.lower() in ['get', 'post', 'put', 'delete', 'patch']:
                            method_name = method_key.upper()
                            description = ""
                            
                            # Extract description if available
                            if isinstance(method_value, dict) and 'description' in method_value:
                                description = method_value['description']
                            
                            endpoints.append({
                                'path': path,
                                'method': method_name,
                                'description': description,
                                'full_endpoint': f"{method_name} {path}"
                            })
        
        return endpoints
        
    except Exception as e:
        print(f"Error parsing RAML: {e}")
        return []

def show_endpoint_selector(endpoints):
    """Show a CLI selector for endpoints."""
    if not endpoints:
        print("No endpoints found in RAML file")
        return None
    
    print("\n📋 Available endpoints from RAML:")
    print("=" * 50)
    
    for i, endpoint in enumerate(endpoints, 1):
        print(f"{i:2d}. {endpoint['full_endpoint']}")
        if endpoint['description']:
            print(f"    Description: {endpoint['description']}")
        print()
    
    while True:
        try:
            choice = input(f"Select endpoint to migrate (1-{len(endpoints)}): ").strip()
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(endpoints):
                selected_endpoint = endpoints[choice_num - 1]
                print(f"\n✅ Selected: {selected_endpoint['full_endpoint']}")
                return selected_endpoint
            else:
                print(f"Please enter a number between 1 and {len(endpoints)}")
        except ValueError:
            print("Please enter a valid number")
        except KeyboardInterrupt:
            print("\nSelection cancelled")
            return None

def mulesoft_migr_command(branch_name, commit_message):
    """Mulesoft migration command: full workflow with new branch and PR."""
    print("🔄 Mulesoft Migration mode: Creating new branch and pull request")
    
    # Get GitHub repository info
    repo_owner, repo_name = get_github_info()
    if not repo_owner or not repo_name:
        return False
    
    try:
        # Step 1: Create new branch
        if not create_branch(branch_name):
            print("Failed to create branch")
            return False
        
        # Step 2: Download project from Anypoint Design Center
        print("Downloading project from Anypoint Design Center...")
        download_result = run_command("anypoint-cli designcenter project download gen-ai-poc ./temp")
        if not download_result:
            print("Warning: Failed to download project from Anypoint Design Center")
        
        # Step 3: Read API.raml file
        print("Reading API.raml file...")
        raml_content = read_raml_file()
        
        # Step 4: Parse endpoints and show selector
        if raml_content:
            print("Parsing RAML endpoints...")
            endpoints = parse_raml_endpoints(raml_content)
            
            if endpoints:
                selected_endpoint = show_endpoint_selector(endpoints)
                if not selected_endpoint:
                    print("No endpoint selected. Exiting...")
                    return False
                
                # Use selected endpoint
                endpoint = selected_endpoint['full_endpoint']
                print(f"Using endpoint: {endpoint}")
            else:
                print("No endpoints found in RAML. Exiting...")
                return False
        else:
            print("No RAML file found. Exiting...")
            return False
        
        # Step 5: Call Amazon Q agent with endpoint and RAML context
        # Sanitize RAML content
        sanitized_raml = raml_content
        enhanced_prompt = f"""Migrate the following Mulesoft endpoint to python: {endpoint}

API Specification (RAML):
{sanitized_raml}

Please migrate this endpoint to a Python Flask application with proper error handling, documentation, and tests."""
        
        print("Calling Amazon Q agent with RAML specification...")
        agent_response = call_amazon_q_agent(enhanced_prompt)
        if not agent_response:
            print("Failed to get response from Amazon Q agent")
            return False
        
        # Step 6: Clean up temp folder
        print("Cleaning up temporary files...")
        try:
            if os.path.exists('./temp'):
                shutil.rmtree('./temp')
                print("Temp folder deleted successfully")
        except Exception as e:
            print(f"Warning: Failed to delete temp folder: {e}")
        
        # Step 7: Commit changes
        if not commit_changes(commit_message):
            print("Failed to commit changes")
            return False
        
        # Step 8: Push branch
        if not push_branch(branch_name):
            print("Failed to push branch")
            return False
        
        # Step 9: Create pull request
        pr_url = create_pull_request(branch_name, commit_message, repo_owner, repo_name)
        
        if pr_url:
            print(f"\n✅ Success! Mulesoft migration pull request created: {pr_url}")
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
    create_parser.add_argument("--pr-title", help="PR title and commit message (default: auto-generated)")
    
    # Update command (new functionality)
    update_parser = subparsers.add_parser('update', help='Call Amazon Q agent and push changes to current branch')
    update_parser.add_argument("prompt", help="The prompt to send to Amazon Q agent")
    update_parser.add_argument("--commit-message", help="Commit message (default: auto-generated)")
    
    # Mulesoft migration command
    mulesoft_parser = subparsers.add_parser('mulesoft-migr', help='Migrate Mulesoft endpoint to AWS with Amazon Q agent')
    mulesoft_parser.add_argument("--branch-name", help="Name for the new branch (default: auto-generated)")
    mulesoft_parser.add_argument("--pr-title", help="PR title and commit message (default: auto-generated)")
    
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
        # Generate values if not provided
        branch_name = args.branch_name or f"feature/amazon-q-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        commit_message = args.pr_title or f"Feature: {args.prompt[:50]}..."
        
        success = create_command(args.prompt, branch_name, commit_message)
        sys.exit(0 if success else 1)
    
    elif args.command == 'mulesoft-migr':
        # Generate values if not provided
        branch_name = args.branch_name or f"mulesoft-migration-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        commit_message = args.pr_title or f"Mulesoft Migration: {datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
        success = mulesoft_migr_command(branch_name, commit_message)
        sys.exit(0 if success else 1)

if __name__ == "__main__":
    main() 