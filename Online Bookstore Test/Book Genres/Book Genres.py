import csv

# Đường dẫn tới tập tin CSV chứa dữ liệu sách
file_path = 'Book dataset/book_data.csv'

output_file = 'Book dataset/Genres.csv'

# Tạo một set để chứa tất cả các thể loại genres duy nhất
unique_genres = set()

with open(file_path, 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Lấy chuỗi genres từ cột 'genres'
        genres_str = row['genres']
        # Chuyển chuỗi genres thành danh sách các từ khóa
        genres_list = eval(genres_str)
        # Thêm tất cả các từ khóa vào unique_genres
        unique_genres.update(genres_list)

sorted_genres = sorted(list(unique_genres))

with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Genres'])
    for genre in sorted_genres:
        writer.writerow([genre])

print("Đã viết thành công các thể loại genres vào tập tin:", output_file)

