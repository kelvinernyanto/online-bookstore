INSERT INTO author(name, birth_date, nationality)
VALUES
	('Bram Stoker', '1847-11-08', 'Irish'),
	('Arthur Conan Doyle', '1859-05-22', 'British'),
	('J.R.R Tolkien', '1892-01-03', 'British'),
	('C.S Lewis', '1898-11-29', 'British'),
	('Mary Shelley', '1797-08-30', 'British');

INSERT INTO provider(name, address, phone)
VALUES
	('Penguin Random House', NULL , NULL),
	('HarperCollins', NULL, NULL);

INSERT INTO book(title, publication_year, genre, price_usd, provider_id)
VALUES 
	('Dracula', 1897, 'Gothic Horror', 100, 1),
	('Frankenstein', 1818, 'Gothic Horror', 80, 1),
	('The Adventures of Sherlock Holmes', 1892, 'Detective Fiction', 120, 1),
	('The Hobbit', 1937, 'Fantasy', 75, 2),
	('The Fellowship of the Ring', 1954, 'Fantasy', 60, 2),
	('The Two Towers', 1954, 'Fantasy', 65, 2),
	('The Return of the King', 1955, 'Fantasy', 80, 2),
	('The Lion, the Witch and the Wardrobe', 1950, 'Fantasy', 70, 2),
	('Prince Caspian', 1951, 'Fantasy', 85, 2),
	('The Voyage of the Dawn Treader', 1952, 'Fantasy', 90, 2);

INSERT INTO book_author(book_id, author_id)
VALUES
	(1, 1),
	(2, 5),
	(3, 2),
	(4, 3),
	(5, 3),
	(6, 3),
	(7, 3),
	(8, 4),
	(9, 4),
	(10, 4);