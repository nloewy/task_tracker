import pytest
from task_tracker import (
    add_task,
    update_task,
    delete_task,
    list_tasks,
    mark_task_done,
    mark_task_in_progress,
    StatusEnum
)

@pytest.fixture
def sample_tasks():
    return {
        1: {
            "description": "Test task",
            "status": StatusEnum.TODO.value,
            "createdAt": "2024-01-01T00:00:00-04:00",
            "updatedAt": "2024-01-01T00:00:00-04:00"
        }
    }

def test_add_task_creates_task():
    tasks, msg = add_task({}, "Do something")
    assert 1 in tasks
    assert tasks[1]["description"] == "Do something"
    assert tasks[1]["status"] == StatusEnum.TODO.value
    assert msg.startswith("Created new task:")

def test_update_existing_task(sample_tasks):
    updated, msg = update_task(sample_tasks, 1, "Updated task")
    assert updated[1]["description"] == "Updated task"
    assert msg == "Task updated successfully"

def test_update_invalid_task(sample_tasks):
    with pytest.raises(Exception):
        update_task(sample_tasks, 999, "Will fail")

def test_delete_existing_task(sample_tasks):
    updated, msg = delete_task(sample_tasks, 1)
    assert updated == {}
    assert msg == "Task deleted successfully"

def test_delete_invalid_task(sample_tasks):
    with pytest.raises(Exception):
        delete_task(sample_tasks, 999)

def test_list_tasks_valid_filter(capsys, sample_tasks):
    _, _ = list_tasks(sample_tasks, "todo")
    captured = capsys.readouterr()
    assert "Test task" in captured.out

def test_list_tasks_invalid_filter(sample_tasks):
    with pytest.raises(Exception):
        list_tasks(sample_tasks, "invalid-status")

def test_mark_task_in_progress(sample_tasks):
    updated, msg = mark_task_in_progress(sample_tasks, 1)
    assert updated[1]["status"] == StatusEnum.IN_PROGRESS.value
    assert msg == "Task moved to 'in-progress'"

def test_mark_task_done(sample_tasks):
    updated, msg = mark_task_done(sample_tasks, 1)
    assert updated[1]["status"] == StatusEnum.DONE.value
    assert msg == "Task moved to 'done'"
