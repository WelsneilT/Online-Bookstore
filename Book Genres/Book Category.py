import csv

# Read the original CSV file
with open('Book dataset/book_data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    # Extract unique categories
    categories = set(row['Category'] for row in reader)

# Write categories to a new CSV file
with open('Book dataset/Category.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Category'])
    for category in categories:
        writer.writerow([category])
