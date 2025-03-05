# FastAPI CRUD CLI Application

[Working CLI App](https://github.com/user-attachments/assets/7344d25b-5090-436f-9714-54f94186132f)

A feature-rich CRUD (Create, Read, Update, Delete) application built with FastAPI and MySQL, featuring a beautiful command-line interface powered by Rich.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [CLI Interface](#cli-interface)
- [MySQL Schema](#mysql-schema)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

This application demonstrates a complete CRUD implementation using FastAPI as the backend with MySQL database and a sleek CLI client instead of a traditional web interface. It showcases:

- FastAPI REST API with MySQL integration
- Raw SQL queries using SQLAlchemy's text() function
- Environment-based configuration
- Beautiful command-line interface with Rich
- Complete CRUD functionality

## Features

- **FastAPI Backend**: High-performance REST API with automatic documentation
- **MySQL Database**: Persistent storage with proper SQL queries
- **Rich CLI Interface**: Beautiful terminal-based user interface
- **CRUD Operations**: Full Create, Read, Update, Delete functionality
- **Pagination**: Support for handling large datasets
- **Environment Configuration**: Easy configuration via .env file
- **Error Handling**: Robust error handling in both backend and CLI
- **Port Conflict Resolution**: Intelligent handling of port conflicts

## Technology Stack

- **Backend**: FastAPI, SQLAlchemy, PyMySQL
- **Database**: MySQL
- **CLI**: Rich, Requests
- **Configuration**: python-dotenv
- **Server**: Uvicorn

## Project Structure

```
fastapi_crud_cli/
├── app/                      # Backend API code
│   ├── crud/                 # CRUD operations
│   │   ├── __init__.py
│   │   ├── create.py         # Create operations with MySQL syntax
│   │   ├── read.py           # Read operations with MySQL syntax
│   │   ├── update.py         # Update operations with MySQL syntax
│   │   └── delete.py         # Delete operations with MySQL syntax
│   ├── models/               # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── item.py           # Item database model
│   ├── routes/               # API routes
│   │   ├── __init__.py
│   │   └── item.py           # Item API endpoints
│   ├── schemas/              # Pydantic schemas
│   │   ├── __init__.py
│   │   └── item.py           # Item schema definitions
│   ├── __init__.py
│   ├── database.py           # Database connection setup
│   └── main.py               # FastAPI application
├── cli/                      # CLI client
│   ├── __init__.py
│   └── cli.py                # Terminal UI using Rich
├── .env                      # Environment variables
├── app_launcher.py           # Application launcher
└── requirements.txt          # Python dependencies
```

## Installation

1. **Clone the repository**

```bash
git clone https://github.com/prakash-aryan/fastapi_crud_cli.git
cd fastapi_crud_cli
```

2. **Set up a virtual environment**

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Set up MySQL**

```bash
# Install MySQL Server if not already installed
sudo apt update
sudo apt install mysql-server

# Secure MySQL installation
sudo mysql_secure_installation

# Create database and user
sudo mysql -u root -p
```

In MySQL prompt:

```sql
CREATE DATABASE crud;
CREATE USER 'crud'@'localhost' IDENTIFIED BY '12345678';
GRANT ALL PRIVILEGES ON crud.* TO 'crud'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

## Configuration

Create a `.env` file in the project root with the following content:

```
# FastAPI Configuration
API_HOST=127.0.0.1
API_PORT=8000

# MySQL Database Configuration
DB_HOST=localhost
DB_PORT=3306
DB_NAME=crud
DB_USER=crud
DB_PASSWORD=12345678
```

Adjust the values according to your setup.

## Usage

1. **Run the application**

```bash
python app_launcher.py
```

This will:
- Start the FastAPI server
- Launch the CLI interface

2. **Alternative: Run components separately**

Start FastAPI server:
```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Start CLI client:
```bash
python -m cli.cli
```

## API Endpoints

The FastAPI backend provides the following REST endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Welcome message |
| `/api/items/` | GET | Get all items with pagination |
| `/api/items/{item_id}` | GET | Get a specific item |
| `/api/items/` | POST | Create a new item |
| `/api/items/{item_id}` | PUT | Update an existing item |
| `/api/items/{item_id}` | DELETE | Delete an item |

You can also access the auto-generated API documentation at:
- http://127.0.0.1:8000/docs (Swagger UI)
- http://127.0.0.1:8000/redoc (ReDoc)

## CLI Interface

The CLI interface provides a user-friendly way to interact with the API:

### Main Menu

- **Create New Item**: Add a new item to the database
- **View All Items**: List all items with pagination
- **View Single Item**: View details of a specific item
- **Update Item**: Modify an existing item
- **Delete Item**: Remove an item from the database

### Navigation

- Use the number keys (1-6) to select menu options
- Follow on-screen prompts for data input
- Press Enter to confirm or navigate back to menus

## MySQL Schema

The application uses a simple MySQL schema:

```sql
CREATE TABLE items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description VARCHAR(1000),
    completed BOOLEAN DEFAULT FALSE
);
```

## Troubleshooting

### Port Conflicts

If port 8000 is already in use, the app_launcher will:
1. Detect the conflict
2. Offer to use the existing server
3. Try a different port
4. Allow you to exit

### Database Connection Issues

If you encounter database connection problems:

1. Verify MySQL is running:
   ```bash
   sudo systemctl status mysql
   ```

2. Check your credentials in the `.env` file

3. Ensure the `crud` database exists:
   ```bash
   mysql -u crud -p
   SHOW DATABASES;
   ```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---
