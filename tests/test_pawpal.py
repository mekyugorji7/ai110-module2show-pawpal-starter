"""
Tests for PawPal+ System
"""

import sys
sys.path.insert(0, '..')

from pawpal_system import Task, Pet


class TestTaskCompletion:
    """Test that mark_complete() changes the task's status."""
    
    def test_mark_complete_changes_status(self):
        # Arrange: Create a task (is_completed defaults to False)
        task = Task(name="Morning walk", duration_minutes=30, priority=1)
        assert task.is_completed is False
        
        # Act: Mark the task as complete
        task.mark_complete()
        
        # Assert: Verify status changed to True
        assert task.is_completed is True


class TestTaskAddition:
    """Test that adding a task to a Pet increases the pet's task count."""
    
    def test_add_task_increases_count(self):
        # Arrange: Create a pet with no tasks
        pet = Pet(name="Buddy", pet_type="dog")
        assert len(pet.tasks) == 0
        
        # Act: Add a task to the pet
        task = Task(name="Feed breakfast", duration_minutes=10, priority=1)
        pet.add_task(task)
        
        # Assert: Verify task count increased to 1
        assert len(pet.tasks) == 1
    
    def test_add_multiple_tasks_increases_count(self):
        # Arrange: Create a pet with no tasks
        pet = Pet(name="Whiskers", pet_type="cat")
        
        # Act: Add multiple tasks
        pet.add_task(Task(name="Feed breakfast", duration_minutes=5, priority=1))
        pet.add_task(Task(name="Brush fur", duration_minutes=15, priority=2))
        pet.add_task(Task(name="Playtime", duration_minutes=20, priority=3))
        
        # Assert: Verify task count is 3
        assert len(pet.tasks) == 3
