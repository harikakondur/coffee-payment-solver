# Coffee Payment Solver

## Description

This project is a coffee payment solver used to determine which person among a group is to pay next. It is implemented using Python with a graphical interface (GUI) using tkinter and MySQL for the backend.

## MySQL Setup

1. Run the provided SQL script (cofee.sql) to create the necessary database and tables.

2. Open `config.py` and update the MySQL details.

    ```python
    # config.py

    MYSQL_HOST = "your_mysql_host"
    MYSQL_USER = "your_mysql_username"
    MYSQL_PASSWORD = "your_mysql_password"
    MYSQL_DATABASE = "coffee"
    ```

    Replace `"your_mysql_host"`, `"your_mysql_username"`, and `"your_mysql_password"` with your MySQL server details.

3. Ensure you have a MySQL server running.

## Libraries

- Tkinter

## How to Run

1. Make sure the MySQL server is running.
2. Run the Python script `gui.py`.

## Usage
- Click the "Who's turn?" button to see who should pay next.
- Click the "Pay" button to initiate and record a payment.

