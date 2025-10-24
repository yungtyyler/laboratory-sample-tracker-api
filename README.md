# LIMS - Sample Tracker API (Backend)

This is the backend API for the LIMS (Laboratory Information Management System) application. It's a secure RESTful API built with Python, Django, and Django REST Framework, designed to manage user authentication and sample data.

**Live API URL:** [https://laboratory-sample-tracker-api.onrender.com](https://laboratory-sample-tracker-api.onrender.com)

**Frontend Client Repo:** [Link to your GitHub repo for the frontend]

## Features

* **Token Authentication:** Secure user registration and login endpoints using DRF's built-in `authtoken`.
* **RESTful API:** Full CRUD (Create, Read, Update, Delete) functionality for `Sample` models.
* **Permissions:** API endpoints are protected, ensuring users can only view and edit their *own* samples.
* **Data Integrity:** Automatically creates an `AuditLog` entry for every sample creation and status update.
* **Custom Endpoints:** Includes a `/api/user/` endpoint to retrieve the current user's details from their token.

## Tech Stack

* **Framework:** Django & Django REST Framework
* **Language:** Python
* **Database:** PostgreSQL
* **Authentication:** DRF Token Authentication
* **CORS:** `django-cors-headers`
* **Deployment:** Render

## API Endpoints

All endpoints are prefixed with `/api/`.

| Endpoint | Method | Permission | Description |
| :--- | :--- | :--- | :--- |
| `/register/` | `POST` | AllowAny | Creates a new user. |
| `/login/` | `POST` | AllowAny | Logs in a user, returns an auth token. |
| `/user/` | `GET` | IsAuthenticated | Returns the logged-in user's details. |
| `/samples/` | `GET` | IsAuthenticated | Returns a list of the user's samples. |
| `/samples/` | `POST` | IsAuthenticated | Creates a new sample for the user. |
| `/samples/<id>/` | `GET` | IsAuthenticated | Returns details for a single sample. |
| `/samples/<id>/` | `PUT` | IsAuthenticated | Updates a sample (e.g., its status). |
| `/samples/<id>/` | `DELETE` | IsAuthenticated | Deletes a sample. |

## Running Locally

1.  **Clone the repository:**
    ```bash
    git clone [your-repo-url]
    cd laboratory-sample-tracker-api
    ```
2.  **Set up a virtual environment:**
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up PostgreSQL:**
    * Create a local PostgreSQL database (e.g., `lims_db`).
    * Create a user (e.g., `lims_user`) with a password.
    * Grant the user privileges on the database.
5.  **Set up environment variables:**
    Create a `.env` file in the root.
    ```env
    SECRET_KEY='your-django-secret-key'
    DEBUG='True'
    ALLOWED_HOSTS='127.0.0.1,localhost'
    DATABASE_URL='postgres://lims_user:password@127.0.0.1:5432/lims_db'
    ```
6.  **Run migrations:**
    ```bash
    python manage.py migrate
    ```
7.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The API will be running at [http://127.0.0.1:8000](http://127.0.0.1:8000).