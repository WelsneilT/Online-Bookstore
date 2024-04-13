import csv

# Đọc tập tin CSV gốc
with open('Book dataset/book_data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    
    genres_counts = {}
    for row in reader:
        
        genres_str = row['genres']
        
        genres_list = eval(genres_str)
        
        for genre in genres_list:
            genres_counts[genre] = genres_counts.get(genre, 0) + 1


sorted_genres_counts = sorted(genres_counts.items(), key=lambda x: x[0])

with open('Book dataset/Genres with quantity sorted.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Genres', 'Quantity'])
    for genre, quantity in sorted_genres_counts:
        writer.writerow([genre, quantity])

print("Đã viết thành công số lượng mỗi thể loại genres vào tập tin:", 'Book dataset/Genres with quantity sorted.csv')
