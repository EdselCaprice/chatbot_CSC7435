# Docker Setup for Tax Research Chatbot

This project has been containerized using Docker with separate containers for the frontend and backend, orchestrated via Docker Compose.

## Prerequisites

- Docker Desktop installed on your system
- Docker Compose V2 (included with Docker Desktop)

## Project Structure

```
chatbot_CSC7435/
├── backend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── app.py
│   ├── research.py
│   ├── requirements.txt
│   └── .env (you need to create this)
├── frontend/
│   ├── Dockerfile
│   ├── .dockerignore
│   ├── nginx.conf
│   ├── package.json
│   └── src/
├── docker-compose.yml
├── Jenkinsfile
└── DOCKER.md
```

## Environment Setup

### Backend Environment Variables

Create a `.env` file in the `backend/` directory with the following variables:

```env
SECRET_KEY=your_secret_key_here
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
ss_url=your_smartsheets_base_url
header={"Authorization": "Bearer your_smartsheet_token"}
exclusions_sheet=sheet_id_1
nexus_sheet=sheet_id_2
pre_post_sheet=sheet_id_3
tax_rates_sheet=sheet_id_4
cfp_sheet=sheet_id_5
limitations_sheet=sheet_id_6
methods_sheet=sheet_id_7
```

**Important**: The `.env` file is excluded from the Docker image via `.dockerignore` for security. Environment variables are passed at runtime via `docker-compose.yml`.

## Running with Docker Compose (Recommended)

### Initial Build and Run

Build and start both containers:

```powershell
docker compose up --build
```

Run in detached mode (background):

```powershell
docker compose up -d
```

### After Code Changes

When you update your application code, rebuild and restart:

```powershell
docker compose down; docker compose up -d --build
```

Or separately:

```powershell
docker compose build
docker compose up -d
```

### Stopping the Application

Stop and remove containers:

```powershell
docker compose down
```

Stop containers without removing them:

```powershell
docker compose stop
```

### Application Access

Once running, the application will be available at:
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## Docker Compose Configuration

The `docker-compose.yml` defines two services:

### Backend Service
- **Container Name**: `chatbot-backend`
- **Port**: 5000:5000
- **Base Image**: Python 3.11-slim
- **Server**: Gunicorn (4 workers, 120s timeout)
- **Environment**: Loaded from `backend/.env`
- **Restart Policy**: `unless-stopped`

### Frontend Service
- **Container Name**: `chatbot-frontend`
- **Port**: 3000:80
- **Base Image**: Multi-stage (Node 18-alpine → Nginx Alpine)
- **Build Arg**: `REACT_APP_API_URL=http://localhost:5000`
- **Depends On**: backend
- **Restart Policy**: `unless-stopped`

### Network
- **Name**: `chatbot-network`
- **Driver**: bridge

## Running Containers Individually (Alternative)

### Backend

Build the backend image:
```powershell
cd backend
docker build -t chatbot-backend .
```

Run the backend container:
```powershell
docker run -p 5000:5000 --env-file .env chatbot-backend
```

### Frontend

Build the frontend image:
```powershell
cd frontend
docker build -t chatbot-frontend --build-arg REACT_APP_API_URL=http://localhost:5000 .
```

Run the frontend container:
```powershell
docker run -p 3000:80 chatbot-frontend
```

## Useful Docker Commands

View running containers:
```powershell
docker ps
```

View all containers (including stopped):
```powershell
docker ps -a
```

View logs (follow mode):
```powershell
docker compose logs -f
```

View logs for specific service:
```powershell
docker compose logs -f backend
docker compose logs -f frontend
```

View container resource usage:
```powershell
docker stats
```

Execute command in running container:
```powershell
docker compose exec backend bash
docker compose exec frontend sh
```

Remove all stopped containers and unused images:
```powershell
docker compose down --rmi all
docker system prune -f
```

## Jenkins CI/CD Pipeline Setup

### Prerequisites
- Docker Desktop installed and running on Windows
- Docker Compose V2 (included with Docker Desktop)
- Jenkins installed and running (locally or via container)
- Jenkins credentials configured for sensitive data

### Required Jenkins Credentials

The pipeline requires the following credentials to be configured in Jenkins:

1. **openai-api-key** (Secret text)
2. **flask-secret-key** (Secret text)
3. **pinecone-api-key** (Secret text)
4. **slack-token** (Secret text) - for build notifications

To add credentials in Jenkins:
1. Navigate to: Manage Jenkins → Manage Credentials
2. Click on "(global)" domain
3. Click "Add Credentials"
4. Select "Secret text" as Kind
5. Enter the Secret and ID (e.g., `openai-api-key`)
6. Click "Create"

### Pipeline Architecture

The Jenkinsfile defines a 3-stage pipeline:

#### 1. Build Stage
- Creates `.env` file from Jenkins credentials
- Runs `docker compose build` to build both frontend and backend images
- Caches layers for faster subsequent builds

#### 2. Test Stage
- Runs backend tests using `docker compose run --rm backend python test.py`
- Ensures code quality before deployment
- Fails pipeline if tests fail

#### 3. Deliver Stage
- Stops existing containers with `docker compose down`
- Deploys updated containers with `docker compose up --build -d`
- Cleans up unused Docker resources with `docker system prune -f`

#### Post-Build Actions
- **Success**: Sends green Slack notification with deployment URLs
- **Failure**: Sends red Slack notification
- **Unstable**: Sends yellow Slack notification

### Create Pipeline Job in Jenkins

1. Access Jenkins at http://localhost:8080
2. Click "New Item"
3. Enter name: `tax-chatbot-pipeline` (or your preferred name)
4. Select "Pipeline"
5. Click "OK"
6. Under "Pipeline" section:
   - **Definition**: "Pipeline script from SCM"
   - **SCM**: "Git"
   - **Repository URL**: Your GitHub repository URL
   - **Branch**: `*/dev` (or `*/main`)
   - **Script Path**: `Jenkinsfile`
7. Under "Build Triggers" (optional):
   - Check "Poll SCM" for automatic builds on code changes
   - Schedule: `H/5 * * * *` (poll every 5 minutes)
8. Click "Save"

### Run the Pipeline

1. Click "Build Now"
2. Monitor pipeline execution through stages:
   - **Build**: Compiles Docker images (~2-5 minutes first run, ~30s cached)
   - **Test**: Runs backend tests (~30 seconds)
   - **Deliver**: Deploys containers (~1 minute)
3. On success, access the application:
   - **Frontend**: http://localhost:3000
   - **Backend**: http://localhost:5000

### Pipeline Execution Flow

```
┌─────────────┐
│   Build     │ → Creates .env from credentials
│             │   Builds Docker images
└──────┬──────┘
       │
┌──────▼──────┐
│    Test     │ → Runs backend tests
│             │   Validates code quality
└──────┬──────┘
       │
┌──────▼──────┐
│   Deliver   │ → Stops old containers
│             │   Starts new containers
│             │   Cleans up resources
└──────┬──────┘
       │
┌──────▼──────┐
│    Post     │ → Sends Slack notification
│             │   Reports success/failure
└─────────────┘
```

### Important Notes

**Jenkins on Windows:**
- Pipeline uses `sh` commands (Unix shell)
- Works with Jenkins running in WSL, Git Bash, or Docker container with shell access
- If running Jenkins natively on Windows, modify Jenkinsfile to use `bat` instead of `sh`

**Environment Variable Handling:**
- `.env` file is created dynamically in the Build stage from Jenkins credentials
- Never commit `.env` files to version control
- Secrets are injected at build time, not stored in the image

**Docker Socket Access (if Jenkins runs in container):**
- Jenkins container needs access to Docker socket: `-v /var/run/docker.sock:/var/run/docker.sock`
- This allows Jenkins to control the host's Docker daemon

### Troubleshooting

**Pipeline fails with "docker: command not found":**
```powershell
# Verify Docker is installed and in PATH
docker --version
docker compose version

# If running Jenkins in container, ensure Docker socket is mounted
docker inspect jenkins-blueocean | grep -i "docker.sock"
```

**Pipeline fails with "permission denied" on docker.sock:**
```bash
# Add Jenkins user to docker group (Linux/WSL)
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

**Pipeline fails at Test stage:**
```powershell
# Run tests manually to diagnose
cd backend
docker compose run --rm backend python test.py
```

**Slack notifications not working:**
- Verify `slack-token` credential is configured correctly
- Check Slack workspace and channel names in Jenkinsfile
- Ensure Jenkins Slack plugin is installed

**View Jenkins logs:**
```powershell
# If Jenkins runs as service
Get-Content C:\ProgramData\Jenkins\.jenkins\logs\jenkins.log -Tail 50

# If Jenkins runs in Docker
docker logs jenkins-blueocean
```

**View Docker Compose logs during pipeline:**
```powershell
docker compose logs -f
```

### Pipeline Customization

To modify the pipeline behavior, edit the `Jenkinsfile`:

- **Change branch**: Update Repository URL in Jenkins job configuration
- **Add stages**: Insert new stage blocks between existing stages
- **Modify test command**: Change the command in the Test stage
- **Update Slack settings**: Modify `teamDomain` and `channel` in post sections
- **Adjust worker count**: Modify Gunicorn workers in `backend/Dockerfile`

## Security Best Practices

1. **Never commit secrets**: Use `.gitignore` to exclude `.env` files
2. **Use Jenkins credentials**: Store all API keys in Jenkins credential store
3. **Limit credential access**: Scope credentials to specific jobs when possible
4. **Rotate keys regularly**: Update credentials periodically
5. **Use .dockerignore**: Exclude sensitive files from Docker images
6. **Runtime injection**: Pass secrets as environment variables, not in images
7. **Scan images**: Use Docker Scout or Trivy to scan for vulnerabilities

## Notes

- The frontend is built as a static React app and served via Nginx on port 80 (mapped to host port 3000)
- The backend runs with Gunicorn (4 workers, 120s timeout) on port 5000
- Both containers are connected via the `chatbot-network` Docker bridge network
- The frontend's API endpoint is configurable via `REACT_APP_API_URL` build argument
- Jenkinsfile dynamically creates `.env` from Jenkins credentials for secure secret management
- Pipeline uses `docker compose` (V2 syntax) instead of legacy `docker-compose`
- Post-build Slack notifications require Jenkins Slack plugin and proper credentials
- Container restart policy is `unless-stopped` for automatic recovery after host reboot
