# Gen AI POC

A Flask application with Data USA API integration and automated deployment to AWS.

## Project Structure

```
gen-ai-poc/
├── src/                    # Application source code
│   └── app.py             # Flask application
├── tests/                  # Test files
│   └── test_app.py        # Application tests
├── infra/                  # Infrastructure files
│   ├── Dockerfile         # Container definition
│   └── ecs-task-def.json  # ECS task definition
├── scripts/                # Utility scripts
│   └── cli_tool.py        # CLI tool for Amazon Q integration
├── .github/workflows/      # GitHub Actions
│   ├── python-app.yml     # Test workflow
│   └── deploy-to-aws.yml  # Deployment workflow
└── requirements.txt        # Python dependencies
```

## Prerequisites

- Python 3.8+
- Git
- AWS CLI with Amazon Q configured
- GitHub CLI (gh) installed and authenticated
- Docker (for containerization)

## Setup

1. **Install GitHub CLI**:
   ```bash
   # macOS
   brew install gh
   
   # Ubuntu/Debian
   sudo apt install gh
   
   # Windows
   winget install GitHub.cli
   ```

2. **Authenticate GitHub CLI**:
   ```bash
   gh auth login
   ```

3. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Flask App

```bash
python src/app.py
```

The application will be available at `http://localhost:8080`

### Running Tests

```bash
pytest
```

### Running with Docker

Build the Docker image:
```bash
docker build -f infra/Dockerfile -t gen-ai-poc .
```

Run the container locally:
```bash
docker run -p 8080:8080 gen-ai-poc
```

The application will be available at `http://localhost:8080`

**Alternative: Build and run in one command:**
```bash
docker build -f infra/Dockerfile -t gen-ai-poc . && docker run -p 8080:8080 gen-ai-poc
```

### Deploying to AWS ECR

Build for x86_64 architecture:
```bash
docker build --platform linux/amd64 -f infra/Dockerfile -t gen-ai-poc .
```

Tag the image for ECR:
```bash
docker tag gen-ai-poc:latest public.ecr.aws/b8p9r6a3/allwyn/gen-ai-poc:latest
```

Authenticate with ECR:
```bash
aws ecr-public get-login-password --region us-east-1 | docker login --username AWS --password-stdin public.ecr.aws
```

Push to ECR:
```bash
docker push public.ecr.aws/b8p9r6a3/allwyn/gen-ai-poc:latest
```

### Using the CLI Tool

The CLI tool provides two commands for working with Amazon Q agent and GitHub.

#### Create Command (Full Workflow)

Creates a new branch, calls Amazon Q agent, and creates a pull request.

**Basic Usage:**
```bash
python scripts/cli_tool.py create "Add a new endpoint for user authentication"
```

**Advanced Usage:**
```bash
python scripts/cli_tool.py create "Implement OAuth2 authentication" \
  --branch-name "feature/oauth2-auth" \
  --commit-message "Add OAuth2 authentication endpoints" \
  --pr-title "Feature: OAuth2 Authentication" \
  --pr-description "Implements OAuth2 authentication flow with Google and GitHub providers"
```

#### Update Command (Quick Updates)

Calls Amazon Q agent and pushes changes to the current branch (no new branch or PR).

**Basic Usage:**
```bash
python scripts/cli_tool.py update "Fix the authentication bug in login endpoint"
```

**With Custom Commit Message:**
```bash
python scripts/cli_tool.py update "Add input validation to user registration" \
  --commit-message "Add comprehensive input validation for user registration form"
```

#### Command Options

**Create Command Options:**
- `prompt`: The prompt to send to Amazon Q agent (required)
- `--branch-name`: Custom branch name (auto-generated if not provided)
- `--commit-message`: Custom commit message (auto-generated if not provided)
- `--pr-title`: Custom pull request title (auto-generated if not provided)
- `--pr-description`: Custom pull request description
- `--github-token`: GitHub personal access token (can also use GITHUB_TOKEN env var)

**Update Command Options:**
- `prompt`: The prompt to send to Amazon Q agent (required)
- `--commit-message`: Custom commit message (auto-generated if not provided)

## API Endpoints

- `GET /hello` - Simple greeting endpoint
- `GET /datausa/top-earning-state` - State with highest median household income
- `GET /datausa/youngest-large-county` - County with lowest median age
- `GET /datausa/largest-counties` - Top 5 counties by population
- `GET /datausa/most-expensive-housing-state` - State with highest median property value

## Deployment

The application is automatically deployed to AWS ECS when code is merged to the main branch.

## Contributing

1. Use the CLI tool to create feature branches with Amazon Q assistance
2. Use the update command for quick fixes and improvements
3. Ensure all tests pass before creating pull requests
4. Follow the established project structure

## Requirements

- Python 3.11+
- AWS CLI with Amazon Q configured
- GitHub personal access token
- Docker (for containerization)

## GitHub Actions Deployment

### Prerequisites

1. **AWS Credentials**: Create an IAM user with the following permissions:
   - `AmazonEC2ContainerRegistryPublicPowerUser`
   - `AmazonECS-FullAccess`

2. **GitHub Secrets**: Add these secrets to your GitHub repository:
   - `AWS_ACCESS_KEY_ID`: Your AWS access key
   - `AWS_SECRET_ACCESS_KEY`: Your AWS secret key

### Setup

1. **Update Environment Variables**: Edit `.github/workflows/deploy.yml` and replace:
   - `your-cluster-name` with your ECS cluster name
   - `your-service-name` with your ECS service name
   - `your-task-definition-family` with your task definition family name

2. **Deploy**: The workflow will automatically run on:
   - Push to `main` branch
   - Manual trigger via GitHub Actions UI

### What the Workflow Does

1. **Build**: Creates Docker image for x86_64 architecture
2. **Push**: Uploads to ECR Public Registry with commit SHA and latest tags
3. **Update Task Definition**: Creates new revision with latest image
4. **Deploy**: Updates ECS service with new task definition
5. **Wait**: Ensures deployment completes successfully

### Manual Deployment

To manually trigger deployment:
1. Go to your GitHub repository
2. Click "Actions" tab
3. Select "Deploy to AWS ECS" workflow
4. Click "Run workflow" 