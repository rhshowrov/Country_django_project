# Django Country Project

A Django-based web application powered by Django REST Framework.

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/rhshowrov/Country_django_project.git
cd Country_django_project
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate          # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Required Dependencies and Versions

- python 3.12
- asgiref==3.8.1
- certifi==2025.4.26
- charset-normalizer==3.4.2
- Django==4.2.20
- django-filter==25.1
- django-viewcomponent==1.0.11
- djangorestframework==3.16.0
- idna==3.10
- Markdown==3.8
- requests==2.32.3
- sqlparse==0.5.3
- tzdata==2025.2
- urllib3==2.4.0

> Make sure these versions match for compatibility.

---

## Database Setup and Configuration

This project uses SQLite as the default database.

* **To use the default SQLite database (db.sqlite3):**  
  No action is required. The project will run with it by default.

* **To start from scratch with a fresh database:**

```bash
rm db.sqlite3                   # On Windows: del db.sqlite3
python manage.py migrate
```

* **Then, populate the database using the custom management command:**

```bash
python manage.py populate_database
```

This will insert initial/sample data into the database.

---

## Running the Application

Start the development server with:

```bash
python manage.py runserver
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) in your browser.

---

## Optional Notes

- If you do not wish to use the provided database, you can delete `db.sqlite3` and start fresh
- The `populate_database` command is optional but useful for testing/demo purposes
- To create an admin user, run:
  ```bash
  python manage.py createsuperuser
  ```



