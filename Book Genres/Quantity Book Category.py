import csv

# Read the original CSV file
with open('Book dataset/book_data.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    # Count the number of items per category
    category_counts = {}
    for row in reader:
        category = row['Category']
        category_counts[category] = category_counts.get(category, 0) + 1

# Write category counts to a new CSV file
with open('Book dataset/Category with quantity.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Category', 'Quantity'])
    for category, quantity in category_counts.items():
        writer.writerow([category, quantity])
