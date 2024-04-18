import sqlite3

# Connect to the source database
source_conn = sqlite3.connect('book_data.db')
source_cursor = source_conn.cursor()

# Connect to the destination database
dest_conn = sqlite3.connect('db.sqlite3')
dest_cursor = dest_conn.cursor()

# Retrieve data from the source database
source_cursor.execute("SELECT title, author, description, price, coverImg FROM book_data2")
data_to_insert = source_cursor.fetchall()

# Modify the data to include a default value for the follow_author column
modified_data = [(title, author, description, price, coverImg,'Khoi',True) for title, author, description, price, coverImg in data_to_insert]

# Insert data into the destination database
dest_cursor.executemany("INSERT INTO books_book (title, author, description, price, image_url, follow_author,book_available) VALUES (?, ?, ?, ?, ?, ?,?)", modified_data)

# Commit changes and close connections
dest_conn.commit()
source_conn.close()
dest_conn.close()
