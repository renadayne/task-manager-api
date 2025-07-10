# 🚀 Task Manager API - FastAPI + JWT + SQLite

> **Full-stack Task Management Application** với giao diện đẹp và API mạnh mẽ

![Task Manager](https://img.shields.io/badge/FastAPI-0.104.1-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![SQLite](https://img.shields.io/badge/SQLite-3.x-yellow)
![JWT](https://img.shields.io/badge/JWT-Authentication-orange)

## 📋 Tổng quan

Task Manager API là một ứng dụng quản lý công việc hoàn chỉnh với:

- **Backend**: FastAPI + JWT Authentication + SQLite
- **Frontend**: HTML + CSS + JavaScript (Vanilla)
- **Features**: CRUD Tasks, Filter, Pagination, Sorting
- **UI/UX**: Modern design với glass morphism effect

## ✨ Tính năng nổi bật

### 🔐 Authentication
- ✅ Đăng ký người dùng với bcrypt hash
- ✅ Đăng nhập với JWT token
- ✅ Bearer token authentication
- ✅ Session persistence với localStorage

### 📝 Task Management
- ✅ **CRUD Operations**: Create, Read, Update, Delete tasks
- ✅ **Filter**: Lọc theo trạng thái hoàn thành
- ✅ **Pagination**: Phân trang với limit/offset
- ✅ **Sorting**: Sắp xếp theo id, title, completed, created_at
- ✅ **Real-time**: Cập nhật UI ngay lập tức

### 🎨 User Interface
- ✅ **Modern Design**: Gradient background + glass morphism
- ✅ **Responsive**: Hoạt động tốt trên mobile/desktop
- ✅ **Animations**: Smooth transitions và hover effects
- ✅ **Toast Notifications**: Thông báo đẹp mắt
- ✅ **Loading States**: UX tốt với loading indicators

## 🛠 Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **JWT**: JSON Web Token authentication
- **SQLite**: Lightweight database
- **bcrypt**: Password hashing
- **python-jose**: JWT implementation
- **passlib**: Password hashing library

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling với gradients và animations
- **JavaScript (ES6+)**: Vanilla JS, no frameworks
- **Font Awesome**: Icons
- **Fetch API**: HTTP requests

## 🚀 Quick Start

### 1. Clone & Install
```bash
git clone <repository-url>
cd task-manager-api
pip install -r requirements.txt
```

### 2. Run Server
```bash
uvicorn main:app --reload
```

### 3. Access Application
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📚 API Documentation

### Authentication Endpoints

#### `POST /register`
Đăng ký người dùng mới
```json
{
  "username": "user123",
  "password": "password123"
}
```

#### `POST /login`
Đăng nhập và nhận JWT token
```bash
# Form data
username=user123&password=password123
```
Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

### Task Endpoints (Require JWT)

#### `GET /tasks`
Lấy danh sách tasks với filter và pagination
```bash
GET /tasks?completed=true&limit=10&offset=0&sort_by=created_at&order=desc
```

#### `POST /tasks`
Tạo task mới
```json
{
  "title": "Hoàn thành dự án"
}
```

#### `PUT /tasks/{id}`
Cập nhật task
```json
{
  "title": "Cập nhật tiêu đề",
  "completed": true
}
```

#### `DELETE /tasks/{id}`
Xóa task

## 🗄 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Tasks Table
```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
```

## 🎯 Features Demo

### 1. Authentication Flow
```
1. Đăng ký user mới → 2. Đăng nhập → 3. Nhận JWT token → 4. Sử dụng API
```

### 2. Task Management
```
1. Tạo task → 2. Filter/Sort → 3. Mark complete → 4. Edit/Delete
```

### 3. UI/UX Features
- **Glass Morphism**: Background blur effects
- **Gradient Colors**: Purple-blue gradient theme
- **Hover Animations**: Smooth transitions
- **Toast Messages**: Success/Error notifications
- **Loading States**: Spinner animations

## 📁 Project Structure

```
task-manager-api/
├── main.py              # FastAPI app entry point
├── config.py            # Configuration settings
├── database.py          # SQLite database management
├── auth.py              # JWT authentication logic
├── models.py            # Pydantic models
├── routers/
│   └── tasks.py         # Task API endpoints
├── static/
│   ├── index.html       # Frontend HTML
│   ├── style.css        # Modern CSS styling
│   └── script.js        # Frontend JavaScript
├── requirements.txt     # Python dependencies
├── test_api.py         # API testing script
└── README.md           # This documentation
```

## 🔧 Configuration

### Environment Variables (Optional)
Tạo file `.env`:
```env
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./task_manager.db
```

### Default Settings
- **JWT Secret**: `your-secret-key-here-change-in-production`
- **Token Expiry**: 30 minutes
- **Database**: SQLite file `task_manager.db`

## 🧪 Testing

### API Testing
```bash
python test_api.py
```

### Manual Testing
1. Mở http://localhost:8000
2. Đăng ký user mới
3. Đăng nhập
4. Tạo và quản lý tasks
5. Test filter/sort/pagination

### Test User
```
Username: testuser
Password: testpass123
```

## 🚀 Deployment

### Development
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Production
```bash
# Install production dependencies
pip install gunicorn

# Run with Gunicorn
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker

# With reverse proxy (Nginx)
# Configure Nginx to proxy to localhost:8000
```

### Docker (Optional)
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔒 Security Features

- ✅ **Password Hashing**: bcrypt với salt
- ✅ **JWT Authentication**: Secure token-based auth
- ✅ **SQL Injection Protection**: Parameterized queries
- ✅ **CORS Handling**: Cross-origin requests
- ✅ **Input Validation**: Pydantic models
- ✅ **Error Handling**: Proper HTTP status codes

## 📊 Performance

- **FastAPI**: High-performance async framework
- **SQLite**: Lightweight, no server setup
- **Static Files**: Efficient serving
- **Caching**: Browser cache for static assets
- **Minimal Dependencies**: Lightweight stack

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📝 License

MIT License - feel free to use for personal/commercial projects.

## 🙏 Acknowledgments

- **FastAPI**: Modern Python web framework
- **Font Awesome**: Beautiful icons
- **CSS Gradients**: Modern design inspiration
- **JWT**: Secure authentication standard

---

**🎉 Task Manager API - Built with ❤️ and modern web technologies!**

> *"Simple, fast, and beautiful task management for everyone"* 
