# Task Manager API

Một API quản lý task đơn giản được xây dựng với FastAPI, JWT authentication và SQLite.

## Tính năng

- ✅ Đăng ký và đăng nhập người dùng
- ✅ JWT authentication
- ✅ CRUD operations cho tasks
- ✅ Filter, pagination và sorting
- ✅ Giao diện Swagger UI
- ✅ Frontend đơn giản với HTML/CSS/JS
- ✅ Bảo mật với bcrypt hash password

## Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd task-manager-api
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Tạo file `.env`:
```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./task_manager.db
```

4. Chạy ứng dụng:
```bash
uvicorn main:app --reload
```

## Sử dụng

- API Documentation: http://localhost:8000/docs
- Frontend: http://localhost:8000
- API Endpoints: http://localhost:8000/api

## API Endpoints

### Authentication
- `POST /register` - Đăng ký người dùng mới
- `POST /login` - Đăng nhập

### Tasks (yêu cầu authentication)
- `GET /tasks/` - Lấy danh sách tasks
- `POST /tasks/` - Tạo task mới
- `GET /tasks/{task_id}` - Lấy chi tiết task
- `PUT /tasks/{task_id}` - Cập nhật task
- `DELETE /tasks/{task_id}` - Xóa task

## Cấu trúc dự án

```
task-manager-api/
├── main.py              # Entry point
├── auth.py              # JWT authentication
├── database.py          # Database connection
├── models.py            # Data models
├── config.py            # Configuration
├── routers/
│   └── tasks.py         # Task routes
├── static/
│   ├── style.css        # Frontend styles
│   └── script.js        # Frontend logic
├── requirements.txt      # Dependencies
└── README.md           # Documentation
```

## Bảo mật

- Mật khẩu được hash với bcrypt
- JWT tokens với thời gian hết hạn
- Input validation với Pydantic
- SQL injection protection

## Deployment

Xem file `DEPLOYMENT.md` để biết hướng dẫn triển khai chi tiết.

## Changelog

Xem file `CHANGELOG.md` để biết lịch sử thay đổi.

---

**Lưu ý**: Đây là dự án demo, không nên sử dụng trong production mà không có các biện pháp bảo mật bổ sung. 
