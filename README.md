# The Reading Room — Online Bookstore

A Flask and PostgreSQL application for browsing and managing a book catalog.

## Features

- View all books and their prices in USD.
- Search books by title.
- Filter books by author.
- Combine title search and author filtering.
- Add a book with one provider and one or more authors.
- Update a book's price.
- Delete a book through a confirmation page.
- Validate form input on the server.

## Technology

- Python 3.12
- Flask and Jinja
- PostgreSQL
- Psycopg 3
- HTML, CSS, and JavaScript

DBeaver can be used to create the database and execute SQL scripts.

## Project Structure

```text
online-bookstore/
├── database/
│   ├── 01_schema.sql
│   ├── 02_seed_data.sql
│   └── 03_queries.sql
├── static/
│   ├── style.css
│   └── validation.js
├── templates/
│   ├── index.html
│   ├── add_book.html
│   ├── edit_price.html
│   └── delete_book.html
├── .env.example
├── .gitignore
├── app.py
├── db.py
├── requirements.txt
└── README.md
```

The local `.env` file and `.venv` directory are not included.

## Setup on Windows

### 1. Open the project

Extract or clone the project, then open PowerShell in its root directory.

Ensure Python 3.12 and PostgreSQL are installed and the PostgreSQL server is running.

### 2. Create a virtual environment

```powershell
py -3.12 -m venv .venv
```

### 3. Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Create and initialize the database

Using DBeaver or another PostgreSQL client:

1. Create a database named `online_bookstore`.
2. Open an SQL editor connected to that database.
3. Execute `database/01_schema.sql`.
4. Execute `database/02_seed_data.sql` once.

The seed script assumes newly created tables with identity sequences
starting at 1. Do not rerun it against an existing populated database.

Expected initial data:

| Table | Rows |
|---|---:|
| author | 5 |
| provider | 2 |
| book | 10 |
| book_author | 10 |

`database/03_queries.sql` contains optional lookup and modification
examples. It is not required to start the application. Use a separate
test database for these examples and run each transaction through its
final `ROLLBACK`.

Identity values can have gaps after rolled-back inserts. This is normal.

### 5. Configure the database connection

Copy the example configuration:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and enter your own PostgreSQL connection details:

```dotenv
DB_HOST=localhost
DB_PORT=5432
DB_NAME=online_bookstore
DB_USER=postgres
DB_PASSWORD="your_local_password"
```

Do not commit or share your real `.env` file.

### 6. Start the application

```powershell
.\.venv\Scripts\python.exe -m flask --app app run
```

Open this address in a browser:

```text
http://127.0.0.1:5000
```

Keep the terminal running while using the application.
Press `Ctrl + C` to stop the server.

For local development with automatic reloading:

```powershell
.\.venv\Scripts\python.exe -m flask --app app run --debug
```

The Flask development server is intended for local development,
not public production hosting.

## Database Design

- `author`: stores author details.
- `provider`: stores book provider details.
- `book`: stores the title, original publication year, genre,
  USD price, and provider reference.
- `book_author`: links books and authors using a composite primary key.

Each book has one provider. A book can have multiple authors,
and an author can write multiple books.

Adding a book and its author relationships uses one transaction.
Deleting a book removes its author relationships first, then the book,
within one transaction.

## Application Routes

| Route | Methods | Purpose |
|---|---|---|
| `/` | GET | Browse and search the catalog |
| `/books/add` | GET, POST | Display the add form and save a new book |
| `/books/<book_id>/edit-price` | GET, POST | Display the price form and save changes |
| `/books/<book_id>/delete` | GET, POST | Display confirmation and delete a book |

## Data Notes

- Seed prices are fictional demonstration prices in USD.
- Publication years refer to the first publication of the works.
- Publishers are used as simulated providers for this assignment.
- Book cover designs are decorative, not official cover images.
- Displayed catalog identifiers are database IDs, not original volume numbers.

## Manual Verification

- Confirm the initial catalog contains 10 books.
- Search for `hobbit` and `HOBBIT`; both should find The Hobbit.
- Filter by Tolkien; the seed data should return four books.
- Combine a title search with an author filter.
- Search for a nonexistent title and check the empty-results message.
- Add a test book with two authors and verify both author filters.
- Enter a price of `10` and confirm it is stored and displayed as `10.00`.
- Update the test book's price and refresh to check persistence.
- Cancel deletion and verify that the book remains.
- Confirm deletion and verify that the book is removed.
- Verify that invalid prices, blank titles, and missing author selections
  are rejected.
- Check that edit/delete URLs for nonexistent book IDs return 404.

## Scope

This is a local coursework application for catalog management.
It does not implement user authentication, checkout, or payment processing.

## Submission

Include source code, templates, static files, SQL scripts,
`requirements.txt`, `.env.example`, this README, and the assignment report.

Exclude:

- `.env`
- `.venv/`
- `__pycache__/`
- Any files containing real credentials

`.gitignore` does not exclude files from a manually created ZIP archive.
Check the archive contents before submitting.