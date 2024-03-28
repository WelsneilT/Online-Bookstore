import pandas as pd

# Đọc dữ liệu từ tệp CSV
books_df = pd.read_csv("Book dataset/Book_data.csv")

# Khởi tạo một dictionary để đếm số lượng sách cho mỗi thể loại
genres_count = {}

# Lặp qua từng dòng trong cột 'genres' và đếm số lượng sách cho mỗi thể loại
for genres in books_df['genres']:
    # Loại bỏ dấu ngoặc kép và dấu ngoặc vuông từ chuỗi
    genres = genres.replace("[", "").replace("]", "").replace("'", "")
    # Tách các thể loại bằng dấu phẩy
    genre_list = genres.split(", ")
    # Đếm số lượng sách cho mỗi thể loại
    for genre in genre_list:
        if genre in genres_count:
            genres_count[genre] += 1
        else:
            genres_count[genre] = 1

# Chuyển dictionary thành DataFrame
quantity_each_genres_df = pd.DataFrame(list(genres_count.items()), columns=['Genre', 'Quantity'])

# Ghi DataFrame vào tệp CSV
quantity_each_genres_df.to_csv("./Book dataset/Quantity Each Genres.csv", index=False)

# In ra tổng số thể loại
total_genres = len(genres_count)
print("Tổng số thể loại:", total_genres)
