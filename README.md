# BookMyShow - Movie Booking System

BookMyShow is an advanced movie booking system designed to provide a seamless experience for users. It allows users to easily book movie tickets and supports three distinct user roles: Super Admin, Theater Admin, and Normal User.

## User Categories

### Super Admin
- **Responsibilities:**
  - Add movies to the database.
- **Note:**
  - Use an email with the domain `@bookmyshow.com` while registering.

### Theater Admin
- **Responsibilities:**
  - Register a theater.
  - Add shows for the registered theater.
- **Note:**
  - Check the box for "Theater Admin" while registering.

### Normal User
- **Responsibilities:**
  - Book shows.

## How the App Works
1. **Super Admin** adds movies to the database.
2. **Theater Admin** registers theaters and updates shows for their theater.
3. **Normal User** books the shows.

## Setup and Installation

1. Clone the repository:
    ```bash
    git clone <repo-url>
    ```
2. Install the required packages:
    ```bash
    pip install flask
    pip install Flask-SQLAlchemy
    pip install flask-login
    pip install flask-migrate
    ```
   If you encounter a "No Module found" error, install the missing module:
    ```bash
    pip install <module-name>
    ```
3. Run the app:
    ```bash
    python main.py
    ```

4. Db migrations
    ``` bash
        flask db init
        flask db migrate
        flask db upgrade/downgrade
    ```

## Requirements
- Flask
- Flask-SQLAlchemy
- flask-login

## Running the App
To run the application, execute the following command in your terminal:
```bash
python main.py
