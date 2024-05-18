# Sử dụng image python chính thức làm base image
FROM python:3.9-slim

# Đặt biến môi trường để đảm bảo các lệnh Python không được lưu trữ trong bộ đệm
ENV PYTHONUNBUFFERED 1

# Tạo thư mục làm việc trong container
WORKDIR /app

# Sao chép các tệp yêu cầu vào container
COPY requirements.txt /app/

# Cập nhật pip và cài đặt các thư viện phụ thuộc từ requirements.txt
RUN pip install --upgrade pip setuptools wheel && pip install --no-cache-dir -r requirements.txt

# Sao chép toàn bộ mã nguồn của dự án vào container
COPY . /app/

# Mở port mà ứng dụng sẽ chạy
EXPOSE 8000

# Lệnh để chạy server Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
