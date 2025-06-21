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
├── docs/                   # Documentation
│   └── API_PUBLIC.md      # Public API documentation
└── requirements.txt        # Python dependencies
```

## Documentation

- **[Public API Documentation](docs/API_PUBLIC.md)** - Complete API reference with examples
- **[README.md](README.md)** - Project overview and setup guide

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

The application will be available at `http://localhost:80`

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
docker run -p 80:80 gen-ai-poc
```

The application will be available at `http://localhost:80`

**Alternative: Build and run in one command:**
```bash
docker build -f infra/Dockerfile -t gen-ai-poc . && docker run -p 80:80 gen-ai-poc
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

The CLI tool provides three commands for working with Amazon Q agent and GitHub.

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
  --pr-title "Feature: OAuth2 Authentication"
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

#### Mulesoft Migration Command

Downloads Mulesoft project, parses RAML endpoints, and migrates selected endpoint to Python.

**Basic Usage:**
```bash
python scripts/cli_tool.py mulesoft-migr "Convert to AWS Lambda with DynamoDB"
```

**Advanced Usage:**
```bash
python scripts/cli_tool.py mulesoft-migr "Migrate to AWS Lambda with authentication" \
  --branch-name "migrate-auth-api" \
  --pr-title "Migrate Authentication API"
```

#### Command Options

**Create Command Options:**
- `prompt`: The prompt to send to Amazon Q agent (required)
- `--branch-name`: Custom branch name (auto-generated if not provided)
- `--pr-title`: Custom PR title and commit message (auto-generated if not provided)

**Update Command Options:**
- `prompt`: The prompt to send to Amazon Q agent (required)
- `--commit-message`: Custom commit message (auto-generated if not provided)

**Mulesoft Migration Command Options:**
- `prompt`: Additional requirements for the Amazon Q agent (required)
- `--branch-name`: Custom branch name (auto-generated if not provided)
- `--pr-title`: Custom PR title and commit message (auto-generated if not provided)

## API Endpoints

- `GET /hello` - Simple greeting endpoint
- `GET /stations` - Retrieve all train stations

### Hello Endpoint

**GET /hello**

Returns a simple greeting message.

**Example:**
```bash
curl http://localhost:80/hello
```

**Response Format:**
```json
{
  "message": "Hello, world!"
}
```

### Stations Endpoint

**GET /stations**

Returns a list of all available train stations with their details. This endpoint was migrated from a Mulesoft RAML specification to Python Flask.

**Example:**
```bash
curl http://localhost:80/stations
```

**Response Format:**
```json
[
  {
    "id": "st001",
    "name": "Union Station",
    "city": "New York",
    "code": "NYS"
  },
  {
    "id": "st002",
    "name": "Central Station",
    "city": "Chicago",
    "code": "CHI"
  }
]
```

**Station Object Fields:**
- `id` (string): Unique identifier for the station
- `name` (string): Full name of the station
- `city` (string): City where the station is located
- `code` (string): Short code identifier for the station

**Testing the Migration:**
```bash
# Run the comprehensive migration test
python scripts/test_stations_endpoint.py
```

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