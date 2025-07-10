# 🚀 Deployment Guide - Task Manager API

Hướng dẫn deploy Task Manager API lên production server.

## 📋 Prerequisites

- Python 3.8+
- pip hoặc uv
- Git
- Server/VPS với Linux (Ubuntu 20.04+ recommended)

## 🛠 Local Development

### 1. Setup Development Environment
```bash
# Clone repository
git clone <repository-url>
cd task-manager-api

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc
venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Development Server
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Access Development
- **Frontend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🚀 Production Deployment

### Option 1: Direct Deployment

#### 1. Server Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and dependencies
sudo apt install python3 python3-pip python3-venv nginx -y

# Create application directory
sudo mkdir -p /var/www/task-manager
sudo chown $USER:$USER /var/www/task-manager
```

#### 2. Deploy Application
```bash
# Clone repository
cd /var/www/task-manager
git clone <repository-url> .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Create production config
cat > .env << EOF
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./task_manager.db
EOF
```

#### 3. Setup Systemd Service
```bash
sudo tee /etc/systemd/system/task-manager.service << EOF
[Unit]
Description=Task Manager API
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/task-manager
Environment=PATH=/var/www/task-manager/venv/bin
ExecStart=/var/www/task-manager/venv/bin/gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Start service
sudo systemctl daemon-reload
sudo systemctl enable task-manager
sudo systemctl start task-manager
```

#### 4. Configure Nginx
```bash
sudo tee /etc/nginx/sites-available/task-manager << EOF
server {
    listen 80;
    server_name your-domain.com;  # Thay đổi domain

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Static files
    location /static/ {
        alias /var/www/task-manager/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Enable site
sudo ln -s /etc/nginx/sites-available/task-manager /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 2: Docker Deployment

#### 1. Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose port
EXPOSE 8000

# Run application
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

#### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  task-manager:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=your-super-secret-key-change-this
      - ALGORITHM=HS256
      - ACCESS_TOKEN_EXPIRE_MINUTES=30
    volumes:
      - ./task_manager.db:/app/task_manager.db
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - ./static:/var/www/static
    depends_on:
      - task-manager
    restart: unless-stopped
```

#### 3. Deploy with Docker
```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f
```

### Option 3: Cloud Deployment

#### Heroku
```bash
# Install Heroku CLI
curl https://cli-assets.heroku.com/install.sh | sh

# Login to Heroku
heroku login

# Create app
heroku create your-task-manager-app

# Set environment variables
heroku config:set SECRET_KEY=your-super-secret-key
heroku config:set ALGORITHM=HS256
heroku config:set ACCESS_TOKEN_EXPIRE_MINUTES=30

# Deploy
git push heroku main

# Open app
heroku open
```

#### Railway
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Deploy
railway up
```

## 🔒 Security Checklist

### Production Security
- [ ] **Change SECRET_KEY**: Sử dụng strong random key
- [ ] **HTTPS**: Cấu hình SSL certificate
- [ ] **Firewall**: Mở chỉ port 80, 443
- [ ] **Database**: Backup thường xuyên
- [ ] **Logs**: Monitor application logs
- [ ] **Updates**: Cập nhật dependencies định kỳ

### Environment Variables
```bash
# Production .env
SECRET_KEY=your-super-secret-256-bit-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=sqlite:///./task_manager.db
```

## 📊 Monitoring

### Health Check
```bash
# Check service status
sudo systemctl status task-manager

# Check logs
sudo journalctl -u task-manager -f

# Check nginx
sudo nginx -t
sudo systemctl status nginx
```

### Performance Monitoring
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs -y

# Monitor resources
htop
iotop
nethogs
```

## 🔄 Backup & Recovery

### Database Backup
```bash
# Create backup script
cat > backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/task-manager"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
cp /var/www/task-manager/task_manager.db $BACKUP_DIR/task_manager_$DATE.db
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
EOF

chmod +x backup.sh

# Add to crontab (daily backup)
echo "0 2 * * * /var/www/task-manager/backup.sh" | crontab -
```

### Recovery
```bash
# Restore database
cp /var/backups/task-manager/task_manager_YYYYMMDD_HHMM.db /var/www/task-manager/task_manager.db

# Restart service
sudo systemctl restart task-manager
```

## 🚀 Scaling

### Horizontal Scaling
```bash
# Load balancer config (nginx)
upstream task_manager {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
    server 127.0.0.1:8002;
    server 127.0.0.1:8003;
}
```

### Database Migration
```bash
# For larger scale, consider PostgreSQL
pip install psycopg2-binary

# Update DATABASE_URL
DATABASE_URL=postgresql://user:password@localhost/task_manager
```

## 📝 Troubleshooting

### Common Issues

#### 1. Service won't start
```bash
# Check logs
sudo journalctl -u task-manager -n 50

# Check permissions
sudo chown -R www-data:www-data /var/www/task-manager
```

#### 2. Nginx 502 error
```bash
# Check if app is running
curl http://127.0.0.1:8000/api

# Check nginx error logs
sudo tail -f /var/log/nginx/error.log
```

#### 3. Database issues
```bash
# Check database file
ls -la /var/www/task-manager/task_manager.db

# Check permissions
sudo chown www-data:www-data /var/www/task-manager/task_manager.db
```

## 🎯 Performance Optimization

### Gunicorn Tuning
```bash
# Optimize workers
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 127.0.0.1:8000 --max-requests 1000 --max-requests-jitter 100
```

### Nginx Optimization
```nginx
# Enable gzip
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

# Static file caching
location /static/ {
    expires 1y;
    add_header Cache-Control "public, immutable";
}
```

---

**🎉 Your Task Manager API is now production-ready!**

> *"Deploy with confidence, scale with ease"* 