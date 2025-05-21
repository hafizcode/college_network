# College Network

A Django-based LAN messaging and file sharing system for college labs.

## Features

- User registration and authentication
- Send and receive messages between users
- File sharing between users
- Admin dashboard for managing users
- Bootstrap-styled responsive UI

## Requirements

- Python 3.13+
- MySQL server
- [uv](https://github.com/astral-sh/uv) package manager

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/hafizcode/college_network.git

cd college_network
```

### 2. Install Dependencies

```sh
uv pip install -r requirements.txt
```
Or, if using `pyproject.toml`:
```sh
uv pip install -r <(uv pip compile pyproject.toml)
```

### 3. Configure Database

- Ensure MySQL is running.
- Create a database named `college_network`.
- Update the credentials in `core/settings.py` if needed.

### 4. Run Migrations

```sh
uv run manage.py migrate
```

### 5. Create a Superuser (Admin)

```sh
uv run manage.py createsuperuser
```

### 6. Run the Development Server

```sh
uv run manage.py runserver
```

Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your browser.

## Usage

- Register as a new user or log in.
- Use the dashboard to send messages and files to other users.
- Admins can manage users via the "Manage Users" link in the navbar.

## File Uploads

Uploaded files are stored in the `media/shared_files/` directory.

## Notes

- For production, set `DEBUG = False` and configure allowed hosts in `core/settings.py`.
- Static files are served automatically in development.

---

**Commands with uv:**

- Run management commands:  
  ```sh
  uv run manage.py <command>
  ```
  Example:
  ```sh
  uv run manage.py runserver
  ```
