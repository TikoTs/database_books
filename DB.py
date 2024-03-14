import random
import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('books.sqlite')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS books
    (id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(50),
    pages INTEGER,
    cover_type VARCHAR(100),
    category VARCHAR(50))''')

conn.commit()

books_list = [
    ('The Book Thief', random.randint(100, 401), 'Paper and cardboard cover', 'Historical Fiction'),
    ('To Kill a Mockingbird', random.randint(100, 401), 'Paperback', 'Classic'),
    ('The Great Gatsby', random.randint(100, 401), 'Hardcover', 'Classic'),
    ('1984', random.randint(100, 401), 'Paperback', 'Dystopian Fiction'),
    ('Pride and Prejudice', random.randint(100, 401), 'Leather-bound', 'Romance'),
    ('The Catcher in the Rye', random.randint(100, 401), 'Paperback', 'Coming-of-age Fiction'),
    ('Harry Potter and the Sorcerer\'s Stone', random.randint(100, 401), 'Hardcover', 'Fantasy'),
    ('The Hobbit', random.randint(100, 401), 'Paperback', 'Fantasy'),
    ('The Lord of the Rings', random.randint(100, 401), 'Leather-bound', 'Fantasy'),
    ('The Hunger Games', random.randint(100, 401), 'Hardcover', 'Science Fiction')
]

cursor.executemany("INSERT INTO books (title, pages, cover_type, category) VALUES (?,?,?,?)", books_list)
conn.commit()


def update_pages_of_book():
    while True:
        id = int(input("Enter the ID of the book you want to update the number of pages for: "))
        cursor.execute("SELECT * FROM books WHERE id = ?", (id,))
        record = cursor.fetchone()
        if record:
            break
        else:
            print("Invalid ID. Please enter a valid book ID.")

    new_pages_number = int(input("Enter the new number of pages: "))
    cursor.execute('UPDATE books SET pages=? WHERE id=?', (new_pages_number, id))
    conn.commit()
    print('Your update result:', cursor.execute("SELECT * FROM books WHERE id = ?", (id,)).fetchone())


update_pages_of_book()

pages_numb_avg = (cursor.execute("SELECT AVG(pages) FROM books")).fetchone()[0]
long_book = (cursor.execute("SELECT title FROM books WHERE pages = (SELECT MAX(pages) FROM books)")).fetchone()[0]
print(f'Average number of pages: {pages_numb_avg}')
print(f'The longest book: {long_book}')

# I make  a bar chart where books are sorted by the number of pages
cursor.execute("SELECT title, pages FROM books ORDER BY pages")
books_data = cursor.fetchall()

titles = [book[0] for book in books_data]
pages = [book[1] for book in books_data]

plt.figure(figsize=(10, 6))
plt.barh(titles, pages, color='lightgreen')
plt.xlabel('Number of Pages')
plt.ylabel('Book Title')
plt.title('Number of Pages for Each Book')
plt.tight_layout()

plt.show()

conn.close()
