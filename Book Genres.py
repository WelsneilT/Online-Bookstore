import pandas as pd

# Đọc dữ liệu từ tệp CSV
books_df = pd.read_csv("Book dataset/Book_data.csv")

# Khởi tạo một set để chứa tất cả các thể loại duy nhất
all_genres = set()

# Lặp qua từng dòng trong cột 'genres' và thêm thể loại vào set
for genres in books_df['genres']:
    # Loại bỏ dấu ngoặc kép và dấu ngoặc vuông từ chuỗi
    genres = genres.replace("[", "").replace("]", "").replace("'", "")
    # Tách các thể loại bằng dấu phẩy và thêm vào set
    all_genres.update(genres.split(", "))

# Chuyển set thành list để có thể sắp xếp các thể loại theo thứ tự bảng chữ cái
all_genres_list = sorted(list(all_genres))

# Tạo DataFrame mới từ list các thể loại
genres_df = pd.DataFrame(all_genres_list, columns=['Genre'])

# Ghi DataFrame vào tệp CSV
genres_df.to_csv("./Book dataset/Genres_data.csv", index=False)
