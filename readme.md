
# CSN - CMS


# Setup Instructions

## 1. Install Python

Make sure you have Python installed. You can download it from the official Python website: [Python Downloads](https://www.python.org/downloads/)

## 2. Setup Environment

Create a virtual environment and activate it.

```bash
# Create a virtual environment
python -m venv env

# Activate the virtual environment
# On Windows
.\env\Scripts\activate
# On macOS/Linux
source env/bin/activate
```

## 3. Install Packages

Install the required packages from `requirements.txt`.

```bash
# Make sure you're in the project directory
pip install -r requirements.txt
```

## 4. Create Database

Create a MySQL database. Open your MySQL command line or use a GUI tool and run the following command:

```sql
CREATE DATABASE csndb;
```

Update your `app/__init__.py` file with the correct database credentials.

```python
# app/__init__.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/csndb'
```

Replace `root` and `password` with your MySQL username and password.

## 5. Run Migrations

Initialize and run the migrations to create the database tables.

```bash
# Initialize the migrations folder
flask db init

# Generate the migration scripts
flask db migrate -m "Initial migration."

# Apply the migrations to the database
flask db upgrade
```

## 6. Run the Application

Start the Flask application.

```bash
# Run the Flask app
flask run
```

Open your browser and navigate to `http://127.0.0.1:5000/` to see the application running.
