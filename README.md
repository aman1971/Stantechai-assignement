# Task Management API

A FastAPI-based CRUD application for managing tasks with MySQL database backend, API Key authentication, pagination, filtering, and sorting.

## Features

- ✅ Full CRUD operations (Create, Read, Update, Delete)
- ✅ **API Key Authentication** for secure access
- ✅ **Pagination** with metadata (page, page_size, total_items, total_pages)
- ✅ **Filtering** by completion status
- ✅ **Sorting** by creation date (newest first)
- ✅ MySQL database integration with SQLAlchemy ORM
- ✅ MVC (Model-View-Controller) architecture
- ✅ Environment-based configuration with .env
- ✅ Alembic database migrations
- ✅ Automatic API documentation (Swagger UI & ReDoc)
- ✅ Comprehensive unit and integration tests
- ✅ Proper error handling and HTTP status codes

## Requirements

- Python 3.8+
- MySQL 5.7+

**OR**

- Docker & Docker Compose (recommended for quick setup)

## Setup Instructions

### Option 1: Docker Setup (Recommended - Easiest)

If you have Docker installed, follow these steps:

```bash
# 1. Copy environment template
cp .env.docker.example .env

# 2. Edit .env and set your password
nano .env

# 3. Build and start the application with MySQL
docker-compose up -d --build

# The API will be available at http://localhost:8000
# Swagger UI: http://localhost:8000/docs
```

⚠️ **Important**: Make sure to set a secure password in the `.env` file before running!

For detailed Docker instructions, see [DOCKER_SETUP.md](DOCKER_SETUP.md)

### Option 2: Manual Setup (Local Development)

#### 1. Create Python Virtual Environment

Create and activate a virtual environment to isolate project dependencies:

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

#### 2. Install Dependencies

With the virtual environment activated, install required packages:

```bash
pip install -r requirements.txt
```

#### 3. Configure Environment Variables

Create a `.env` file in the project root directory:

```bash
# Copy the example file
cp .env.example .env
```

Update the `.env` file with your MySQL database credentials:

```env
DATABASE_USER=root
DATABASE_PASSWORD=your_secure_password_here
DATABASE_HOST=localhost
DATABASE_PORT=3306
DATABASE_NAME=task_db
```

**Note**: Replace `your_secure_password_here` with your actual MySQL password.

#### 4. Create MySQL Database

Create the database using MySQL command line:

```bash
mysql -u root -p -e "CREATE DATABASE task_db;"
```

Or using MySQL client:

```sql
CREATE DATABASE task_db;
```

#### 5. Run Database Migrations

Apply database migrations to create tables:

```bash
alembic upgrade head
```

#### 6. Run the Application

Start the FastAPI server:

```bash
uvicorn app.main:app --reload
```

The API will be available at: **http://localhost:8000**

## Generate API Key

Before using the API, generate an API key:

```bash
curl -X POST http://localhost:8000/api-keys/generate \
  -H "Content-Type: application/json" \
  -d '{"name": "My API Key"}'
```

Save the generated key - you'll need it for all subsequent requests!

## API Documentation

### 📚 Interactive API Documentation

All API endpoints are automatically documented and available at:

- **Swagger UI**: http://localhost:8000/docs (Interactive, test endpoints directly)
- **ReDoc**: http://localhost:8000/redoc (Clean, readable documentation)

### 🔑 Using API Key Authentication

1. Open Swagger UI: http://localhost:8000/docs
2. Generate an API key using `/api-keys/generate` endpoint
3. Click the **"Authorize"** button (green lock icon)
4. Enter your API key in the "Value" field
5. Click "Authorize" and "Close"
6. Now you can test all protected endpoints!

## API Endpoints Overview

### API Key Management (Public - No Auth Required)
- `POST /api-keys/generate` - Generate new API key
- `GET /api-keys/` - List all API keys
- `DELETE /api-keys/{id}` - Deactivate API key

### Task Management (Protected - Requires API Key Header: `X-API-Key`)

#### Create Task
```bash
POST /items/
Body: {"title": "Task title", "description": "Task description", "completed": false}
```

#### List Tasks with Pagination, Filtering & Sorting
```bash
GET /items/?page=1&page_size=10&completed=false
```
**Features:**
- **Pagination**: `page` (page number), `page_size` (items per page, max 100)
- **Filtering**: `completed=true` or `completed=false`
- **Sorting**: Automatically sorted by creation date (newest first)

**Response includes:**
```json
{
  "items": [...],
  "pagination": {
    "page": 1,
    "page_size": 10,
    "total_items": 50,
    "total_pages": 5,
    "has_next": true,
    "has_previous": false
  }
}
```

#### Get Single Task
```bash
GET /items/{id}
```

#### Update Task
```bash
PUT /items/{id}
Body: {"title": "Updated title", "completed": true}
```

#### Delete Task
```bash
DELETE /items/{id}
```

## Quick Start Example

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Start the server
uvicorn app.main:app --reload

# 3. In another terminal, generate API key
export API_KEY=$(curl -s -X POST http://localhost:8000/api-keys/generate \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Key"}' | python3 -c "import json,sys; print(json.load(sys.stdin)['key'])")

# 4. Create a task
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"title": "My First Task", "completed": false}'

# 5. Get all tasks (paginated)
curl -X GET "http://localhost:8000/items/?page=1&page_size=10" \
  -H "X-API-Key: $API_KEY"

# 6. Get completed tasks only
curl -X GET "http://localhost:8000/items/?page=1&page_size=10&completed=true" \
  -H "X-API-Key: $API_KEY"
```

## Running Tests

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_api.py -v
```

## Database Schema

### Tasks Table
| Field | Type | Constraints |
|-------|------|-------------|
| id | INT | Primary Key, Auto Increment |
| title | VARCHAR(200) | Unique, Not Null |
| description | TEXT | Nullable |
| completed | BOOLEAN | Default: False |
| created_at | DATETIME | Auto-generated |
| updated_at | DATETIME | Auto-updated |

### API Keys Table
| Field | Type | Constraints |
|-------|------|-------------|
| id | INT | Primary Key, Auto Increment |
| key | VARCHAR(64) | Unique, Not Null |
| name | VARCHAR(200) | Not Null |
| is_active | BOOLEAN | Default: True |
| created_at | DATETIME | Auto-generated |
| last_used_at | DATETIME | Nullable |

## Alembic Migration Commands

```bash
# Apply all migrations
alembic upgrade head

# Rollback last migration
alembic downgrade -1

# Create new migration after model changes
alembic revision --autogenerate -m "description"

# View current migration version
alembic current

# View migration history
alembic history
```

## Configuration Management

The application uses environment-based configuration:

- **`.env` file**: Database credentials and settings
- **`app/config.py`**: Configuration loader using Pydantic Settings
- **Dynamic loading**: All modules import configuration from `config.py`

Example:
```python
from app.config import get_settings

settings = get_settings()
database_url = settings.database_url
```

## Technology Stack

- **Framework**: FastAPI 0.104.1
- **ORM**: SQLAlchemy 2.0.23
- **Database**: MySQL (via PyMySQL)
- **Migrations**: Alembic 1.12.1
- **Validation**: Pydantic 2.5.0
- **Authentication**: API Key (Header-based)
- **Testing**: Pytest 7.4.3
- **Server**: Uvicorn 0.24.0

## Security Features

- ✅ API Key authentication on all task endpoints
- ✅ Secure key generation using `secrets` module
- ✅ Keys stored with usage tracking
- ✅ Keys can be deactivated without deletion
- ✅ Environment variables for sensitive data

## Project Architecture

The application follows **MVC (Model-View-Controller)** architecture:

- **Models** (`app/models/`): Database models (SQLAlchemy)
- **Schemas** (`app/schemas/`): Request/Response validation (Pydantic)
- **Controllers** (`app/routes/`): API route handlers
- **Services** (`app/services/`): Business logic
- **Utils** (`app/utils/`): Reusable utilities

## Troubleshooting

### Virtual Environment Issues
```bash
# Deactivate current environment
deactivate

# Remove and recreate
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Database Connection Issues
- Verify MySQL is running: `mysql -u root -p`
- Check `.env` file credentials
- Ensure database exists: `SHOW DATABASES;`

### Migration Issues
```bash
# Check current migration status
alembic current

# Reset and reapply migrations
alembic downgrade base
alembic upgrade head
```

## License

This project is for educational and evaluation purposes.

## Version

**v2.0.0** - With API Key Authentication, Pagination, Filtering, and Sorting
