// API Configuration
const API_BASE_URL = 'http://localhost:8000';

// Global variables
let currentUser = null;
let currentToken = null;
let currentPage = 0;
let totalTasks = 0;
const tasksPerPage = 10;

// DOM elements
const loginForm = document.getElementById('login-form');
const registerForm = document.getElementById('register-form');
const userInfo = document.getElementById('user-info');
const mainContent = document.getElementById('main-content');
const currentUserSpan = document.getElementById('current-user');

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    // Check if user is already logged in
    const savedToken = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');

    if (savedToken && savedUser) {
        currentToken = savedToken;
        currentUser = JSON.parse(savedUser);
        showMainContent();
        loadTasks();
    }
});

// Authentication functions
async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (!username || !password) {
        showToast('Vui lòng nhập đầy đủ thông tin', 'error');
        return;
    }

    try {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            const data = await response.json();
            currentToken = data.access_token;
            currentUser = { username };

            // Save to localStorage
            localStorage.setItem('token', currentToken);
            localStorage.setItem('user', JSON.stringify(currentUser));

            showMainContent();
            loadTasks();
            showToast('Đăng nhập thành công!', 'success');

            // Clear form
            document.getElementById('username').value = '';
            document.getElementById('password').value = '';
        } else {
            const error = await response.json();
            showToast(error.detail || 'Đăng nhập thất bại', 'error');
        }
    } catch (error) {
        showToast('Lỗi kết nối', 'error');
    }
}

async function register() {
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;

    if (!username || !password) {
        showToast('Vui lòng nhập đầy đủ thông tin', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/register`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            showToast('Đăng ký thành công! Vui lòng đăng nhập', 'success');
            showLogin();
            // Clear form
            document.getElementById('reg-username').value = '';
            document.getElementById('reg-password').value = '';
        } else {
            const error = await response.json();
            showToast(error.detail || 'Đăng ký thất bại', 'error');
        }
    } catch (error) {
        showToast('Lỗi kết nối', 'error');
    }
}

function logout() {
    currentToken = null;
    currentUser = null;
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    showLoginForm();
    showToast('Đã đăng xuất', 'info');
}

function showLogin() {
    loginForm.style.display = 'flex';
    registerForm.style.display = 'none';
}

function showRegister() {
    loginForm.style.display = 'none';
    registerForm.style.display = 'flex';
}

function showLoginForm() {
    loginForm.style.display = 'flex';
    registerForm.style.display = 'none';
    userInfo.style.display = 'none';
    mainContent.style.display = 'none';
}

function showMainContent() {
    loginForm.style.display = 'none';
    registerForm.style.display = 'none';
    userInfo.style.display = 'flex';
    mainContent.style.display = 'block';
    currentUserSpan.textContent = `Xin chào, ${currentUser.username}!`;
}

// Task management functions
async function loadTasks() {
    const tasksList = document.getElementById('tasks-list');
    const loading = document.getElementById('loading');
    const noTasks = document.getElementById('no-tasks');
    const pagination = document.getElementById('pagination');

    // Show loading
    tasksList.innerHTML = '';
    loading.style.display = 'block';
    noTasks.style.display = 'none';
    pagination.style.display = 'none';

    try {
        // Build query parameters
        const params = new URLSearchParams({
            limit: tasksPerPage,
            offset: currentPage * tasksPerPage
        });

        const statusFilter = document.getElementById('status-filter').value;
        const sortBy = document.getElementById('sort-by').value;
        const sortOrder = document.getElementById('sort-order').value;

        if (statusFilter !== '') {
            params.append('completed', statusFilter);
        }
        params.append('sort_by', sortBy);
        params.append('order', sortOrder);

        const response = await fetch(`${API_BASE_URL}/tasks?${params}`, {
            headers: {
                'Authorization': `Bearer ${currentToken}`
            }
        });

        if (response.ok) {
            const data = await response.json();
            totalTasks = data.total;

            if (data.tasks.length === 0) {
                noTasks.style.display = 'block';
            } else {
                renderTasks(data.tasks);
                updatePagination();
            }
        } else {
            showToast('Lỗi tải danh sách tasks', 'error');
        }
    } catch (error) {
        showToast('Lỗi kết nối', 'error');
    } finally {
        loading.style.display = 'none';
    }
}

function renderTasks(tasks) {
    const tasksList = document.getElementById('tasks-list');
    tasksList.innerHTML = '';

    tasks.forEach(task => {
        const taskElement = createTaskElement(task);
        tasksList.appendChild(taskElement);
    });
}

function createTaskElement(task) {
    const taskDiv = document.createElement('div');
    taskDiv.className = `task-item ${task.completed ? 'completed' : ''}`;
    taskDiv.dataset.taskId = task.id;

    const createdDate = new Date(task.created_at).toLocaleString('vi-VN');

    taskDiv.innerHTML = `
        <div class="task-header">
            <div class="task-title">${escapeHtml(task.title)}</div>
            <div class="task-actions">
                <button onclick="toggleTask(${task.id}, ${!task.completed})" class="btn ${task.completed ? 'btn-warning' : 'btn-success'}">
                    <i class="fas fa-${task.completed ? 'undo' : 'check'}"></i>
                    ${task.completed ? 'Hoàn tác' : 'Hoàn thành'}
                </button>
                <button onclick="editTask(${task.id})" class="btn btn-secondary">
                    <i class="fas fa-edit"></i> Sửa
                </button>
                <button onclick="deleteTask(${task.id})" class="btn btn-danger">
                    <i class="fas fa-trash"></i> Xóa
                </button>
            </div>
        </div>
        <div class="task-date">Tạo lúc: ${createdDate}</div>
    `;

    return taskDiv;
}

async function addTask() {
    const titleInput = document.getElementById('new-task-title');
    const title = titleInput.value.trim();

    if (!title) {
        showToast('Vui lòng nhập tên công việc', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/tasks`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentToken}`
            },
            body: JSON.stringify({ title })
        });

        if (response.ok) {
            titleInput.value = '';
            loadTasks();
            showToast('Thêm task thành công!', 'success');
        } else {
            const error = await response.json();
            showToast(error.detail || 'Lỗi thêm task', 'error');
        }
    } catch (error) {
        showToast('Lỗi kết nối', 'error');
    }
}

async function toggleTask(taskId, completed) {
    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentToken}`
            },
            body: JSON.stringify({ completed })
        });

        if (response.ok) {
            loadTasks();
            showToast(`Task đã ${completed ? 'hoàn thành' : 'hoàn tác'}!`, 'success');
        } else {
            const error = await response.json();
            showToast(error.detail || 'Lỗi cập nhật task', 'error');
        }
    } catch (error) {
        showToast('Lỗi kết nối', 'error');
    }
}

async function editTask(taskId) {
    const newTitle = prompt('Nhập tên mới cho task:');
    if (!newTitle || newTitle.trim() === '') return;

    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${currentToken}`
            },
            body: JSON.stringify({ title: newTitle.trim() })
        });

        if (response.ok) {
            loadTasks();
            showToast('Cập nhật task thành công!', 'success');
        } else {
            const error = await response.json();
            showToast(error.detail || 'Lỗi cập nhật task', 'error');
        }
    } catch (error) {
        showToast('Lỗi kết nối', 'error');
    }
}

async function deleteTask(taskId) {
    if (!confirm('Bạn có chắc muốn xóa task này?')) return;

    try {
        const response = await fetch(`${API_BASE_URL}/tasks/${taskId}`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${currentToken}`
            }
        });

        if (response.ok) {
            loadTasks();
            showToast('Xóa task thành công!', 'success');
        } else {
            const error = await response.json();
            showToast(error.detail || 'Lỗi xóa task', 'error');
        }
    } catch (error) {
        showToast('Lỗi kết nối', 'error');
    }
}

// Pagination functions
function updatePagination() {
    const pagination = document.getElementById('pagination');
    const pageInfo = document.getElementById('page-info');
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');

    const totalPages = Math.ceil(totalTasks / tasksPerPage);
    const currentPageNum = currentPage + 1;

    pageInfo.textContent = `Trang ${currentPageNum} / ${totalPages}`;

    prevBtn.disabled = currentPage === 0;
    nextBtn.disabled = currentPage >= totalPages - 1;

    if (totalPages > 1) {
        pagination.style.display = 'flex';
    } else {
        pagination.style.display = 'none';
    }
}

function previousPage() {
    if (currentPage > 0) {
        currentPage--;
        loadTasks();
    }
}

function nextPage() {
    const totalPages = Math.ceil(totalTasks / tasksPerPage);
    if (currentPage < totalPages - 1) {
        currentPage++;
        loadTasks();
    }
}

// Utility functions
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast ${type} show`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Enter key handlers
document.getElementById('new-task-title').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        addTask();
    }
});

document.getElementById('username').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        login();
    }
});

document.getElementById('password').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        login();
    }
});

document.getElementById('reg-username').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        register();
    }
});

document.getElementById('reg-password').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        register();
    }
});