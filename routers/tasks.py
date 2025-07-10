from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Optional
from database import database
from models import TaskCreate, TaskUpdate, Task, TaskListResponse
from auth import get_current_user
import sqlite3

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=TaskListResponse)
async def get_tasks(
    current_user = Depends(get_current_user),
    completed: Optional[bool] = Query(None, description="Lọc theo trạng thái hoàn thành"),
    limit: int = Query(10, ge=1, le=100, description="Số lượng task tối đa"),
    offset: int = Query(0, ge=0, description="Số task bỏ qua"),
    sort_by: str = Query("created_at", description="Sắp xếp theo trường"),
    order: str = Query("desc", description="Thứ tự sắp xếp (asc/desc)")
):
    """Lấy danh sách tasks của user hiện tại"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Xây dựng query với filter và pagination
    query = "SELECT * FROM tasks WHERE user_id = ?"
    params = [current_user["id"]]
    
    if completed is not None:
        query += " AND completed = ?"
        params.append(completed)
    
    # Thêm ORDER BY
    valid_sort_fields = ["id", "title", "completed", "created_at"]
    if sort_by not in valid_sort_fields:
        sort_by = "created_at"
    
    valid_orders = ["asc", "desc"]
    if order.lower() not in valid_orders:
        order = "desc"
    
    query += f" ORDER BY {sort_by} {order.upper()}"
    
    # Thêm LIMIT và OFFSET
    query += " LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    tasks = cursor.fetchall()
    
    # Đếm tổng số tasks (không có LIMIT)
    count_query = "SELECT COUNT(*) FROM tasks WHERE user_id = ?"
    count_params = [current_user["id"]]
    
    if completed is not None:
        count_query += " AND completed = ?"
        count_params.append(completed)
    
    cursor.execute(count_query, count_params)
    total = cursor.fetchone()[0]
    
    conn.close()
    
    # Chuyển đổi kết quả thành list of Task objects
    task_list = []
    for task in tasks:
        task_list.append(Task(
            id=task["id"],
            user_id=task["user_id"],
            title=task["title"],
            completed=bool(task["completed"]),
            created_at=task["created_at"]
        ))
    
    return TaskListResponse(
        tasks=task_list,
        total=total,
        limit=limit,
        offset=offset
    )

@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: int, current_user = Depends(get_current_user)):
    """Lấy chi tiết một task"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, current_user["id"])
    )
    task = cursor.fetchone()
    conn.close()
    
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task không tồn tại"
        )
    
    return Task(
        id=task["id"],
        user_id=task["user_id"],
        title=task["title"],
        completed=bool(task["completed"]),
        created_at=task["created_at"]
    )

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(task: TaskCreate, current_user = Depends(get_current_user)):
    """Tạo task mới"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "INSERT INTO tasks (user_id, title, completed) VALUES (?, ?, ?)",
        (current_user["id"], task.title, False)
    )
    task_id = cursor.lastrowid
    
    # Lấy task vừa tạo
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    new_task = cursor.fetchone()
    conn.commit()
    conn.close()
    
    return Task(
        id=new_task["id"],
        user_id=new_task["user_id"],
        title=new_task["title"],
        completed=bool(new_task["completed"]),
        created_at=new_task["created_at"]
    )

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int, 
    task_update: TaskUpdate, 
    current_user = Depends(get_current_user)
):
    """Cập nhật task"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Kiểm tra task có tồn tại và thuộc về user hiện tại không
    cursor.execute(
        "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, current_user["id"])
    )
    existing_task = cursor.fetchone()
    
    if not existing_task:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task không tồn tại"
        )
    
    # Xây dựng query update
    update_fields = []
    params = []
    
    if task_update.title is not None:
        update_fields.append("title = ?")
        params.append(task_update.title)
    
    if task_update.completed is not None:
        update_fields.append("completed = ?")
        params.append(task_update.completed)
    
    if not update_fields:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Không có trường nào để cập nhật"
        )
    
    params.append(task_id)
    params.append(current_user["id"])
    
    query = f"UPDATE tasks SET {', '.join(update_fields)} WHERE id = ? AND user_id = ?"
    cursor.execute(query, params)
    conn.commit()
    
    # Lấy task đã cập nhật
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    updated_task = cursor.fetchone()
    conn.close()
    
    return Task(
        id=updated_task["id"],
        user_id=updated_task["user_id"],
        title=updated_task["title"],
        completed=bool(updated_task["completed"]),
        created_at=updated_task["created_at"]
    )

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, current_user = Depends(get_current_user)):
    """Xóa task"""
    conn = database.get_connection()
    cursor = conn.cursor()
    
    # Kiểm tra task có tồn tại và thuộc về user hiện tại không
    cursor.execute(
        "SELECT id FROM tasks WHERE id = ? AND user_id = ?",
        (task_id, current_user["id"])
    )
    task = cursor.fetchone()
    
    if not task:
        conn.close()
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task không tồn tại"
        )
    
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()
    
    return None 