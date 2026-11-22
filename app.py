from flask import Flask, render_template, request, abort, redirect, url_for
from decimal import Decimal, InvalidOperation
from db import get_connection

app = Flask(__name__)
@app.after_request
def add_validation_script(response):
    if response.mimetype == "text/html":
        html = response.get_data(as_text=True)

        script = (
            '<script src="'
            + url_for("static", filename="validation.js")
            + '" defer></script>'
        )

        if "</body>" in html:
            html = html.replace("</body>", script + "</body>", 1)
            response.set_data(html)

    return response

@app.route("/")
def home():
    search_query = request.args.get("q", "").strip()
    author_id = request.args.get("author_id", type=int)

    with get_connection() as connection:
        with connection.cursor() as cursor:
            search_pattern = f"%{search_query}%"

            if author_id is not None:
                cursor.execute(
                    '''
                    SELECT book.book_id, book.title, book.price_usd
                    FROM book
                    JOIN book_author ON book.book_id = book_author.book_id
                    WHERE book.title ILIKE %s
                        AND book_author.author_id = %s
                    ORDER BY book.book_id
                    ''',
                    (search_pattern, author_id)
                )

            else:
                cursor.execute(
                    '''
                    SELECT book_id, title, price_usd
                    FROM book
                    WHERE title ILIKE %s
                    ORDER BY book_id;
                    ''',
                    (search_pattern,)
                )

            books = cursor.fetchall()

            cursor.execute(
                "SELECT author_id, name FROM author ORDER BY name"
            )
            authors = cursor.fetchall()
            
    return render_template(
        "index.html", 
        books = books, 
        search_query = search_query,
        authors = authors,
        selected_author_id = author_id)

@app.route(
    "/books/<int:book_id>/edit-price",
    methods = ["GET", "POST"]
    )
def edit_price(book_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT book_id, title, price_usd FROM book WHERE book_id = %s;",
                (book_id,)
            )

            book = cursor.fetchone()

            if book is None:
                abort(404)

            if request.method == "POST":
                price_text = request.form.get("price_usd", "").strip()

                try:
                    price = Decimal(price_text)
                except InvalidOperation:
                    abort(400, description = "Price must be a number.")

                if not price.is_finite():
                    abort(400, description = "Price must be a valid number.")

                if price < 0 or price > Decimal("9999999999.99"):
                    abort(400, description = "Price is outside the allowed range.")

                if price != price.quantize(Decimal("0.01")):
                    abort(400, description = "Price must have at most two decimal places.")

                cursor.execute(
                    '''
                    UPDATE book
                    SET price_usd = %s
                    WHERE book_id = %s;
                    ''',
                    (price, book_id)
                )

    if request.method == "POST":
        return redirect(url_for("home", _anchor = "collection"))

    return render_template("edit_price.html", book = book)

@app.route("/books/add", methods=["GET", "POST"])
def add_book():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        publication_year = request.form.get("publication_year", "").strip()
        genre = request.form.get("genre", "").strip()
        price_text = request.form.get("price_usd", "").strip()
        provider_id = request.form.get("provider_id", "").strip()
        author_ids = request.form.getlist("author_ids")

        if not title or len(title) > 150:
            abort(400, description="Title must contain 1-150 characters.")

        if len(genre) > 150:
            abort(400, description="Genre must not exceed 150 characters.")

        if not author_ids:
            abort(400, description="Choose at least one author.")

        try:
            price = Decimal(price_text)
        except InvalidOperation:
            abort(400, description="Price must be a number.")

        if not price.is_finite():
            abort(400, description="Price must be a valid number.")

        if price < 0 or price > Decimal("9999999999.99"):
            abort(400, description="Price is outside the allowed range.")

        if price != price.quantize(Decimal("0.01")):
            abort(
                400,
                description="Price must have at most two decimal places."
            )

        try:
            year = int(publication_year) if publication_year else None
            provider_id = int(provider_id)
            author_ids = [int(author_id) for author_id in author_ids]
        except ValueError:
            abort(400, description="Year and IDs must be whole numbers.")

        if year is not None and not 1 <= year <= 9999:
            abort(400, description="Year must be between 1 and 9999.")

        if provider_id <= 0 or any(
            author_id <= 0 for author_id in author_ids
        ):
            abort(400, description="Invalid provider or author ID.")

        author_ids = list(dict.fromkeys(author_ids))

        with get_connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT provider_id
                    FROM provider
                    WHERE provider_id = %s;
                    """,
                    (provider_id,)
                )

                if cursor.fetchone() is None:
                    abort(400, description="Provider was not found.")

                for author_id in author_ids:
                    cursor.execute(
                        """
                        SELECT author_id
                        FROM author
                        WHERE author_id = %s;
                        """,
                        (author_id,)
                    )

                    if cursor.fetchone() is None:
                        abort(400, description="An author was not found.")

                cursor.execute(
                    """
                    INSERT INTO book (
                        title,
                        publication_year,
                        genre,
                        price_usd,
                        provider_id
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING book_id;
                    """,
                    (title, year, genre or None, price, provider_id)
                )

                new_book_id = cursor.fetchone()[0]

                for author_id in author_ids:
                    cursor.execute(
                        """
                        INSERT INTO book_author (book_id, author_id)
                        VALUES (%s, %s);
                        """,
                        (new_book_id, author_id)
                    )

        return redirect(url_for("home", _anchor="collection"))

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT provider_id, name
                FROM provider
                ORDER BY name;
                """
            )
            providers = cursor.fetchall()

            cursor.execute(
                """
                SELECT author_id, name
                FROM author
                ORDER BY name;
                """
            )
            authors = cursor.fetchall()

    return render_template(
        "add_book.html",
        providers=providers,
        authors=authors
    )

@app.route(
    "/books/<int:book_id>/delete",
    methods = ["GET", "POST"]
    )
def delete_book(book_id):
    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT book_id, title FROM book WHERE book_id = %s;",
                (book_id,)
            )

            book = cursor.fetchone()

            if book is None:
                abort(404)

            if request.method == "POST":
                cursor.execute(
                    "DELETE FROM book_author WHERE book_id = %s;",
                    (book_id,)
                )

                cursor.execute(
                    "DELETE FROM book WHERE book_id = %s;",
                    (book_id,)
                )

    if request.method == "POST":
        return redirect(url_for("home", _anchor="collection"))

    return render_template("delete_book.html", book=book)