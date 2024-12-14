# Stage 4 - Django Project

## Project Overview
Stage 4 enhances the features introduced in the previous stages by implementing advanced functionality, improving performance, and incorporating user authentication and external integrations.

## Repository Structure
```
stage-4/
├── api/                # Contains the API-related files and configurations
├── uninest/            # Core Django project directory
├── db.sqlite3          # Default SQLite database file
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies for the project
```

### 1. `api/`
The `api/` directory now includes endpoints with authentication and authorization, enabling secure data access. Additional views, serializers, and URL configurations support extended functionality, including pagination and filtering.

### 2. `uninest/`
The core Django project directory has been updated to support authentication mechanisms, such as token-based or session-based authentication. Settings and middleware configurations are fine-tuned to enhance security and performance.

### 3. `db.sqlite3`
The SQLite database continues to serve as the development database. Additional tables and relationships were created to support the new features introduced in this stage.

### 4. `manage.py`
No major changes; it remains the primary tool for executing Django commands.

### 5. `requirements.txt`
New dependencies have been added to support authentication, external API integration, and other advanced features. Install them using:
```bash
pip install -r requirements.txt
```

## Getting Started
Follow these steps to set up and run the project locally:

### Prerequisites
- Python (>= 3.8)
- pip (Python package manager)

### Installation
1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd stage-4
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run database migrations:
   ```bash
   python manage.py migrate
   ```

5. Start the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/`.

## Key Updates in Stage 4
- Implemented user authentication and authorization using Django's built-in features or third-party libraries.
- Added pagination, filtering, and advanced query capabilities to the APIs.
- Integrated external APIs or services for enhanced functionality.
- Improved the overall performance and security of the application.
