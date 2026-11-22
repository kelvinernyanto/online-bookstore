CREATE TABLE author(
    author_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    birth_date DATE,
    nationality VARCHAR(50)
);

CREATE TABLE provider(
	provider_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	name VARCHAR(150) NOT NULL,
	address TEXT,
	phone VARCHAR(30)
);

CREATE TABLE book(
	book_id INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	title VARCHAR(150) NOT NULL,
	publication_year INT,
	genre VARCHAR(150),
	price_usd NUMERIC(12,2) NOT NULL CHECK (price_usd >= 0),
	provider_id INT NOT NULL REFERENCES provider(provider_id)
);

CREATE TABLE book_author(
	book_id INT REFERENCES book(book_id),
	author_id INT REFERENCES author(author_id),
	PRIMARY KEY (book_id, author_id)
);