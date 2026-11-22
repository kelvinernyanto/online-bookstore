-- =========================================================
-- LOOKUP EXAMPLES
-- =========================================================

-- 1. List all books with their authors and providers.
-- A book with multiple authors appears once per author.
SELECT
    book.book_id,
    book.title,
    author.name AS author_name,
    provider.name AS provider_name,
    book.price_usd
FROM book
JOIN book_author ON book.book_id = book_author.book_id
JOIN author ON book_author.author_id = author.author_id
JOIN provider ON book.provider_id = provider.provider_id
ORDER BY book.book_id, author.name;


-- 2. Search for books by title.
SELECT
    book.book_id,
    book.title,
    author.name AS author_name,
    book.price_usd
FROM book
JOIN book_author ON book.book_id = book_author.book_id
JOIN author ON book_author.author_id = author.author_id
WHERE book.title ILIKE '%hobbit%'
ORDER BY book.book_id, author.name;


-- 3. Search for books by author.
SELECT
    book.book_id,
    book.title,
    author.name AS author_name,
    book.price_usd
FROM book
JOIN book_author ON book.book_id = book_author.book_id
JOIN author ON book_author.author_id = author.author_id
WHERE author.name ILIKE '%tolkien%'
ORDER BY book.book_id, author.name;


-- 4. Search for books by provider.
SELECT
    book.book_id,
    book.title,
    provider.name AS provider_name,
    book.price_usd
FROM book
JOIN provider ON book.provider_id = provider.provider_id
WHERE provider.name ILIKE '%penguin%'
ORDER BY book.book_id;


-- =========================================================
-- UPDATE EXAMPLE
-- Run this entire transaction to restore the original price.
-- =========================================================

BEGIN;

UPDATE book
SET price_usd = 15.99
WHERE book_id = 1;

SELECT book_id, title, price_usd
FROM book
WHERE book_id = 1;

ROLLBACK;


-- =========================================================
-- INSERT AND DELETE EXAMPLE
-- Run this entire transaction.
-- Requires provider ID 2 and author ID 2 from the seed data.
-- =========================================================

BEGIN;

-- Keep the generated ID for this transaction.
CREATE TEMP TABLE demo_book_id (
    book_id INT PRIMARY KEY
) ON COMMIT DROP;

-- Insert a temporary test book and capture its actual ID.
WITH inserted_book AS (
    INSERT INTO book (
        title,
        publication_year,
        genre,
        price_usd,
        provider_id
    )
    VALUES (
        'Testing',
        2026,
        'Fantasy',
        10.00,
        2
    )
    RETURNING book_id
)
INSERT INTO demo_book_id (book_id)
SELECT book_id
FROM inserted_book;

-- Link the test book to an existing author.
INSERT INTO book_author (book_id, author_id)
SELECT book_id, 2
FROM demo_book_id;

-- Check the inserted book and its author.
SELECT
    book.book_id,
    book.title,
    author.name AS author_name,
    book.price_usd
FROM book
JOIN book_author ON book.book_id = book_author.book_id
JOIN author ON book_author.author_id = author.author_id
WHERE book.book_id IN (
    SELECT book_id FROM demo_book_id
);

-- Remove the relationship before deleting the book.
DELETE FROM book_author
WHERE book_id IN (
    SELECT book_id FROM demo_book_id
);

DELETE FROM book
WHERE book_id IN (
    SELECT book_id FROM demo_book_id
);

-- Expected result: 0.
SELECT COUNT(*) AS remaining_test_books
FROM book
WHERE book_id IN (
    SELECT book_id FROM demo_book_id
);

ROLLBACK;