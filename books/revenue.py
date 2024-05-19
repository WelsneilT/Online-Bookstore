import os
import sqlite3
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pickle

# Kết nối với cơ sở dữ liệu SQLite
conn = sqlite3.connect('db.sqlite3')

# Truy vấn dữ liệu từ bảng books_order
query = "SELECT * FROM books_order"
orders = pd.read_sql_query(query, conn)

# Đóng kết nối với cơ sở dữ liệu
conn.close()

# Hiển thị dữ liệu ban đầu
print("Dữ liệu ban đầu:")
print(orders.head())

# Chuyển đổi dữ liệu thành DataFrame của pandas
orders['created_at'] = pd.to_datetime(orders['created_at'])
data = {
    'id': orders['id'],
    'user_id': orders['user_id'],
    'first_name': orders['first_name'],
    'last_name': orders['last_name'],
    'email': orders['email'],
    'country': orders['country'],
    'phone_number': orders['phone_number'],
    'address': orders['address'],
    'shipping_address': orders['shipping_address'],
    'town_city': orders['town_city'],
    'zip_code': orders['zip_code'],
    'order_notes': orders['order_notes'],
    'total_price': orders['total_price'],
    'created_at': orders['created_at'],
    'updated_at': orders['updated_at'],
    'success': orders['success'],
    'canceled_reason': orders['canceled_reason']
}

df = pd.DataFrame(data)
print("Dữ liệu sau khi chuyển đổi:")
print(df.head())

# Tạo thêm dữ liệu giả lập cho mỗi ngày từ 1/4 đến 20/5
date_range = pd.date_range(start='2024-04-01', end='2024-05-20')
num_samples = len(date_range)

np.random.seed(42)
random_prices = np.random.uniform(low=2.0, high=100.0, size=num_samples)

additional_data = {
    'id': np.arange(df['id'].max() + 1, df['id'].max() + 1 + num_samples),
    'user_id': [1] * num_samples,  # Giá trị giả lập cho user_id
    'first_name': ['Tống'] * num_samples,
    'last_name': ['Tân'] * num_samples,
    'email': ['td.tan2711@gmail.com'] * num_samples,
    'country': ['Vietnam'] * num_samples,
    'phone_number': ['0327728199'] * num_samples,
    'address': ['25/89 Thịnh Quang'] * num_samples,
    'shipping_address': ['25/89 Thịnh Quang'] * num_samples,
    'town_city': ['Hà Nội'] * num_samples,
    'zip_code': ['000084'] * num_samples,
    'order_notes': [''] * num_samples,
    'total_price': random_prices,
    'created_at': date_range,
    'updated_at': date_range,
    'success': [True] * num_samples,
    'canceled_reason': [''] * num_samples
}

additional_df = pd.DataFrame(additional_data)

# Kết hợp dữ liệu hiện tại với dữ liệu giả lập
combined_df = pd.concat([df, additional_df], ignore_index=True)
print("Dữ liệu kết hợp:")
print(combined_df.head())

# Chuẩn bị dữ liệu cho mô hình
combined_df['date'] = combined_df['created_at'].dt.date
daily_revenue = combined_df.groupby('date')['total_price'].sum().reset_index()

# Chuyển đổi cột 'date' thành kiểu datetime và tạo cột 'days'
daily_revenue['date'] = pd.to_datetime(daily_revenue['date'])
daily_revenue['days'] = (daily_revenue['date'] - daily_revenue['date'].min()).dt.days

# Chia dữ liệu thành biến độc lập (X) và biến phụ thuộc (y)
X = daily_revenue[['days']]
y = daily_revenue['total_price']

# Chia dữ liệu thành tập huấn luyện và tập kiểm tra
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Huấn luyện mô hình hồi quy tuyến tính
model = LinearRegression()
model.fit(X_train, y_train)

# Dự đoán doanh thu ngày tiếp theo
def predict_next_day_revenue():
    next_day = [[daily_revenue['days'].max() + 1]]
    predicted_revenue = model.predict(next_day)
    return predicted_revenue[0], next_day[0][0]

predicted_revenue, next_day = predict_next_day_revenue()
print(f'Dự đoán doanh thu cho ngày tiếp theo: {predicted_revenue}')

# Đánh giá mô hình và hiển thị biểu đồ
plt.figure(figsize=(12, 6))
plt.plot(daily_revenue['days'], daily_revenue['total_price'], marker='o', linestyle='-', color='grey', alpha=0.6, label='Actual Revenue')
plt.scatter(next_day, predicted_revenue, color='red', label='Next Day Prediction', marker='X', s=100)
plt.xlabel('Days')
plt.ylabel('Revenue')
plt.title('Actual vs Predicted Revenue')
plt.legend()
plt.grid(True)
plt.show()

# In ra độ chính xác của mô hình
print(f'R^2 Score: {model.score(X_test, y_test)}')

# Lưu mô hình vào file
with open('revenue_prediction_model.pkl', 'wb') as model_file:
    pickle.dump(model, model_file)

# Tải mô hình từ file và dự đoán lại
with open('revenue_prediction_model.pkl', 'rb') as model_file:
    loaded_model = pickle.load(model_file)

predicted_revenue = loaded_model.predict([[daily_revenue['days'].max() + 1]])
print(f'Dự đoán doanh thu cho ngày tiếp theo với mô hình đã tải: {predicted_revenue[0]}')
