# Online Book Store
- Chào mừng đến với Online Book Store! Đây là một sản phẩm cung cấp dịch vụ tiện nghi nhất cho người đọc khám phá, tìm kiếm sách từ mọi loại chủ đề.

# Docker
- Yêu cầu cài đặt:
  + Docker
  + Docker Compose (nếu bạn sử dụng Docker Compose)

- Để pull và sử dụng Docker Image sử dụng các lệnh sau:
  + docker pull welsneil/ecom_project:latest
  + docker run -p 8000:8000 welsneil/ecom_project:latest
  + Sau đó vào trình duyệt và gõ link: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
  + https://hub.docker.com/r/welsneil/online_bookstore

## Tính năng

- **Duyệt**: Khám phá bộ sưu tầm hơn 50000 cuốn sách của chúng tôi với đa dạng các chủ đề từ fiction, non-fiction, mystery, romance, science fiction, and more.
- **Tìm kiếm**: Bạn có thể tìm kiếm sách cụ thể qua tiêu đề của sách, tác giả, một cách nhanh chóng.
- **Tài khoản**: Bạn sẽ được tạo tài khoản cá nhân để lưu giữ các đầu sách và lịch sử đơn mua của bạn.
- **Kho sách của bạn**: Chứa các cuốn sách bạn yêu thích dự định mua.
- **Bình luận**: Đọc và để lại những ý kiến hay đánh giá của bạn về sách.Bạn cũng có thể xem các bình luận khác về cuốn sách định đọc.
- **Đề xuất**: Hệ thống sẽ đề xuất sách phù hợp với sở thích và lịch sử đọc của bạn.
- **Hỗ trợ tiếp cận**: Hệ thống hỗ trợ tìm kiếm bằng giọng nói và có chức năng chat với tổng đài nếu có thắc mắc.

## Technologies Used

- **Frontend**: html
- **Backend**: django framework
- **Database**:SQLite
- **Machine learning**: tf-idf, counter vectorizer, k-means cluster
- **API**:google translate, kommunicate, web speech to text

## SET UP môi trường

- pipenv shell
- pipenv install django
- python manage.py check
- pip install pandas
- pip install scikit-learn
- pip install nltk
- python manage.py runserver

## Truy cập link dưới vào trang người quản lý bán hàng
- http://127.0.0.1:8000/admin/


