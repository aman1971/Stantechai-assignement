# Docker Setup Guide

## Quick Start with Docker

The easiest way to run this application is using Docker Compose, which will set up both the application and MySQL database automatically.

### Prerequisites

- Docker Desktop (or Docker Engine + Docker Compose)
- No need to install Python, MySQL, or any dependencies manually!

### 1. Configure Environment Variables

Create a `.env` file in the project root for Docker:

```bash
# Copy the template
cp .env.example .env

# Edit the .env file and set your password
nano .env
```

Update the `.env` file with your credentials:

```env
DATABASE_USER=root
DATABASE_PASSWORD=YOUR_SECURE_PASSWORD_HERE
DATABASE_HOST=mysql
DATABASE_PORT=3306
DATABASE_NAME=task_db
```

⚠️ **Important**: Never commit the `.env` file to Git. It's already in `.gitignore`.

### 2. Build and Run with Docker Compose

```bash
# Build and start all services (app + MySQL)
docker-compose up --build

# Or run in detached mode (background)
docker-compose up -d --build
```

That's it! The application will be available at: **http://localhost:8000**

### 3. Access the Application

- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs

### 4. Generate API Key

```bash
curl -X POST http://localhost:8000/api-keys/generate \
  -H "Content-Type: application/json" \
  -d '{"name": "Docker Key"}'
```

### 5. Test the API

```bash
# Save your API key
export API_KEY="your_generated_key_here"

# Create a task
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"title": "Docker Task", "description": "Running in Docker!", "completed": false}'

# Get all tasks
curl -X GET "http://localhost:8000/items/?page=1&page_size=10" \
  -H "X-API-Key: $API_KEY"
```

## Docker Commands

### Start Services
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f app
docker-compose logs -f mysql
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (deletes database data)
docker-compose down -v
```

### Rebuild Application
```bash
# Rebuild after code changes
docker-compose up -d --build

# Rebuild only the app service
docker-compose up -d --build app
```

### Access Container Shell
```bash
# Access app container
docker exec -it task_api bash

# Access MySQL container (will prompt for password from .env)
docker exec -it task_mysql mysql -u root -p task_db
```

### View Container Status
```bash
# List running containers
docker-compose ps

# View resource usage
docker stats
```

## Docker Compose Services

### MySQL Service
- **Image**: mysql:8.0
- **Container**: task_mysql
- **Port**: 3306 (configurable via .env)
- **Database**: task_db (configurable via .env)
- **User**: root (configurable via .env)
- **Password**: Set in .env file (never hardcoded)
- **Data**: Persisted in Docker volume `mysql_data`

### App Service
- **Build**: From Dockerfile
- **Container**: task_api
- **Port**: 8000
- **Depends on**: MySQL (waits for health check)
- **Auto-migrations**: Runs `alembic upgrade head` on startup

## Environment Variables

The application reads environment variables from a `.env` file in the project root.

### Setup

```bash
# Copy the template
cp .env.example .env

# Edit with your credentials
nano .env
```

### Required Variables

```env
DATABASE_USER=root                    # MySQL username
DATABASE_PASSWORD=your_password_here  # MySQL password (CHANGE THIS!)
DATABASE_HOST=mysql                   # Docker service name
DATABASE_PORT=3306                    # MySQL port
DATABASE_NAME=task_db                 # Database name
```

⚠️ **Security Notes**:
- Never commit `.env` file to Git (already in `.gitignore`)
- Use strong passwords in production
- The `.env.example` is a template only
- Each developer/environment should have their own `.env` file

## Database Persistence

MySQL data is stored in a Docker volume named `mysql_data`. This means:
- Data persists across container restarts
- Data survives `docker-compose down`
- Data is deleted with `docker-compose down -v`

### Reset Database
```bash
# Stop services and delete all data
docker-compose down -v

# Start fresh
docker-compose up -d --build
```

## Development with Docker

### Hot Reload
The app container has a volume mount (`.:/app`) that enables hot reload:
1. Make code changes on your host machine
2. Changes are reflected in the container
3. Uvicorn auto-reloads (if using `--reload` flag)

### Run Migrations Manually
```bash
docker exec -it task_api alembic upgrade head
```

### Run Tests in Container
```bash
docker exec -it task_api pytest
docker exec -it task_api pytest -v
```

## Troubleshooting

### Port Already in Use
If port 8000 or 3306 is already in use:

```bash
# Check what's using the port
lsof -i :8000
lsof -i :3306

# Kill the process or change ports in docker-compose.yml
```

### MySQL Connection Issues
```bash
# Check MySQL is healthy
docker-compose ps

# View MySQL logs
docker-compose logs mysql

# Test MySQL connection (use your password from .env)
docker exec -it task_mysql mysql -u root -p -e "SHOW DATABASES;"
```

### Container Won't Start
```bash
# View logs
docker-compose logs app

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Database Not Initialized
```bash
# Manually run migrations
docker exec -it task_api alembic upgrade head

# Check migration status
docker exec -it task_api alembic current
```

## Production Deployment

For production, consider:

1. **Use secrets management** instead of hardcoded passwords
2. **Enable SSL/TLS** for MySQL connection
3. **Use environment-specific .env files**
4. **Set up proper logging**
5. **Use Docker secrets** for sensitive data
6. **Configure resource limits**
7. **Use health checks** for monitoring
8. **Enable backup** for MySQL data

Example production docker-compose.yml additions:
```yaml
services:
  app:
    deploy:
      resources:
        limits:
          cpus: '0.5'
          memory: 512M
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/"]
      interval: 30s
      timeout: 10s
      retries: 3
```

## Cleanup

Remove everything (containers, volumes, networks):
```bash
# Stop and remove all
docker-compose down -v

# Remove images
docker rmi task_api
docker rmi mysql:8.0

# Clean up system
docker system prune -a
```

## Architecture

```
┌─────────────────┐
│   Host Machine  │
│   localhost     │
└────────┬────────┘
         │
         ├──── :8000 ────┐
         │               │
         └──── :3306 ────┤
                         │
         ┌───────────────▼──────────────┐
         │     Docker Network           │
         │      (task_network)          │
         │                              │
         │  ┌──────────┐  ┌──────────┐ │
         │  │   App    │  │  MySQL   │ │
         │  │ :8000    │─▶│ :3306    │ │
         │  │task_api  │  │task_mysql│ │
         │  └──────────┘  └──────────┘ │
         │                              │
         │       Volume: mysql_data     │
         └──────────────────────────────┘
```


