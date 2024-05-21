import os
import sqlite3
import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import pickle

# Hàm tính chi phí tồn kho
def inventory_cost(order_qty, demand, holding_cost, shortage_cost):
    overstock = max(0, order_qty - demand)
    shortage = max(0, demand - order_qty)
    return holding_cost * overstock + shortage_cost * shortage

# Hàm mục tiêu cần tối ưu hóa
def objective_function(order_qty, demands, holding_cost, shortage_cost):
    return sum(inventory_cost(order_qty, demand, holding_cost, shortage_cost) for demand in demands)

# Thuật toán Simulated Annealing
def simulated_annealing(demands, holding_cost, shortage_cost, initial_temp, cooling_rate, max_iter):
    current_solution = random.randint(min(demands), max(demands))
    current_cost = objective_function(current_solution, demands, holding_cost, shortage_cost)
    best_solution = current_solution
    best_cost = current_cost
    temperature = initial_temp

    cost_history = [current_cost]  # Lưu lịch sử chi phí để vẽ biểu đồ

    for i in range(max_iter):
        new_solution = current_solution + random.randint(-10, 10)
        new_cost = objective_function(new_solution, demands, holding_cost, shortage_cost)

        if new_cost < current_cost or random.uniform(0, 1) < np.exp((current_cost - new_cost) / temperature):
            current_solution = new_solution
            current_cost = new_cost

            if new_cost < best_cost:
                best_solution = new_solution
                best_cost = new_cost

        temperature *= cooling_rate
        cost_history.append(current_cost)  # Lưu chi phí hiện tại vào lịch sử chi phí

    return best_solution, best_cost, cost_history

# Kết nối với cơ sở dữ liệu SQLite
conn = sqlite3.connect('db.sqlite3')

# Truy vấn dữ liệu từ bảng books_order
query = "SELECT * FROM books_order"
orders = pd.read_sql_query(query, conn)

# Đóng kết nối với cơ sở dữ liệu
conn.close()

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

# Lấy ngày hiện tại
today = pd.Timestamp.today()

# Tạo thêm dữ liệu giả lập cho mỗi ngày từ 1/4 đến ngày hiện tại
date_range = pd.date_range(start='2024-04-01', end=today)
num_samples = len(date_range)

np.random.seed(42)
random_prices = np.random.uniform(low=2.0, high=50, size=num_samples)

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

# Chuẩn bị dữ liệu cho mô hình
combined_df['date'] = combined_df['created_at'].dt.date
daily_revenue = combined_df.groupby('date')['total_price'].sum().reset_index()

# Chuyển đổi cột 'date' thành kiểu datetime và tạo cột 'days'
daily_revenue['date'] = pd.to_datetime(daily_revenue['date'])
daily_revenue['days'] = (daily_revenue['date'] - daily_revenue['date'].min()).dt.days

# Sử dụng dữ liệu từ daily_revenue để làm nhu cầu sản phẩm hàng ngày
demands = daily_revenue['total_price'].astype(int).tolist()

# Tham số thuật toán Simulated Annealing
holding_cost = 2  # Chi phí lưu trữ mỗi đơn vị hàng tồn kho
shortage_cost = 5  # Chi phí thiếu hàng mỗi đơn vị
initial_temp = 1000
cooling_rate = 0.95
max_iter = 1000

# Tối ưu hóa
best_order_qty, best_cost, cost_history = simulated_annealing(demands, holding_cost, shortage_cost, initial_temp, cooling_rate, max_iter)


# Vẽ biểu đồ
plt.figure(figsize=(20, 8))

# Biểu đồ số lượng sách bán ra trong từng ngày
plt.plot(daily_revenue['date'], daily_revenue['total_price'], label='Số lượng sách bán ra trong từng ngày')

# Vẽ đường thẳng cho số lượng hàng đặt tối ưu
plt.axhline(y=best_order_qty, color='r', linestyle='--', label='Số lượng hàng đặt tối ưu')
# Hiển thị số lượng hàng đặt tối ưu
plt.text(daily_revenue['date'].min(), best_order_qty, f'{best_order_qty}', color='black', va='bottom', ha='right')

plt.xlabel('Ngày')
plt.ylabel('Số lượng')
plt.title('Số lượng sách bán ra trong từng ngày và số lượng hàng đặt tối ưu')
plt.legend()
plt.grid(True)

# Định dạng lại trục x để hiển thị ngày tháng
plt.gcf().autofmt_xdate()

# Lưu biểu đồ thành file hình ảnh
if not os.path.exists('static/admin'):
    os.makedirs('static/admin')
plt.savefig('static/admin/inventory_optimization.png')

# Lưu mô hình vào file
with open('inventory_optimization_model.pkl', 'wb') as model_file:
    pickle.dump((best_order_qty, best_cost, cost_history), model_file)

# Tải mô hình từ file và kiểm tra lại
with open('inventory_optimization_model.pkl', 'rb') as model_file:
    best_order_qty, best_cost, cost_history = pickle.load(model_file)

print(f'Số lượng hàng đặt tối ưu với mô hình đã tải: {best_order_qty}')
print(f'Chi phí tối ưu với mô hình đã tải: {best_cost}')



    