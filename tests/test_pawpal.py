"""
Tests for PawPal+ System
"""

import sys
sys.path.insert(0, '..')

import pytest
from pawpal_system import Task, Pet, Scheduler, Owner
from datetime import date, time, timedelta


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


class TestSortingEdgeCases:
    """Test sorting correctness for tasks."""
    
    def test_sort_by_priority_empty_list(self):
        # Arrange: Create scheduler with no tasks
        scheduler = Scheduler(available_time=60)
        
        # Act: Sort empty task list
        result = scheduler.sort_by_priority()
        
        # Assert: Should return empty list without errors
        assert result == []
    
    def test_sort_by_priority_returns_correct_order(self):
        # Arrange: Create tasks with different priorities (out of order)
        scheduler = Scheduler(available_time=120)
        scheduler.add_task(Task(name="Low priority", duration_minutes=10, priority=5))
        scheduler.add_task(Task(name="High priority", duration_minutes=10, priority=1))
        scheduler.add_task(Task(name="Medium priority", duration_minutes=10, priority=3))
        
        # Act: Sort by priority
        result = scheduler.sort_by_priority()
        
        # Assert: Tasks should be in priority order (1, 3, 5)
        assert result[0].name == "High priority"
        assert result[1].name == "Medium priority"
        assert result[2].name == "Low priority"
    
    def test_sort_by_time_returns_chronological_order(self):
        # Arrange: Create tasks with different preferred times (out of order)
        scheduler = Scheduler(available_time=120)
        scheduler.add_task(Task(name="Evening task", duration_minutes=10, priority=1, preferred_time="evening"))
        scheduler.add_task(Task(name="Morning task", duration_minutes=10, priority=1, preferred_time="morning"))
        scheduler.add_task(Task(name="Afternoon task", duration_minutes=10, priority=1, preferred_time="afternoon"))
        
        # Act: Sort by time
        result = scheduler.sort_by_time()
        
        # Assert: Tasks should be in chronological order (morning -> afternoon -> evening)
        assert result[0].name == "Morning task"
        assert result[1].name == "Afternoon task"
        assert result[2].name == "Evening task"
    
    def test_sort_by_time_unknown_preferred_time_sorts_last(self):
        # Arrange: Create tasks including one with invalid preferred_time
        scheduler = Scheduler(available_time=120)
        task_invalid = Task(name="Unknown time", duration_minutes=10, priority=1)
        task_invalid.preferred_time = "midnight"  # Invalid time slot
        scheduler.add_task(task_invalid)
        scheduler.add_task(Task(name="Morning task", duration_minutes=10, priority=1, preferred_time="morning"))
        
        # Act: Sort by time
        result = scheduler.sort_by_time()
        
        # Assert: Unknown preferred_time should sort last (fallback value 4)
        assert result[0].name == "Morning task"
        assert result[1].name == "Unknown time"


class TestRecurringTasks:
    """Test recurrence logic for daily and weekly tasks."""
    
    def test_daily_task_creates_next_occurrence(self):
        # Arrange: Create a daily task with specific due date
        today = date.today()
        scheduler = Scheduler(available_time=60)
        task = Task(
            name="Feed breakfast",
            duration_minutes=10,
            priority=1,
            frequency="daily",
            due_date=today
        )
        scheduler.add_task(task)
        
        # Act: Complete the task
        next_task = scheduler.complete_task("Feed breakfast")
        
        # Assert: New task created for the following day
        assert next_task is not None
        assert next_task.due_date == today + timedelta(days=1)
        assert next_task.is_completed is False
        assert next_task.name == "Feed breakfast"
    
    def test_weekly_task_creates_next_occurrence(self):
        # Arrange: Create a weekly task
        today = date.today()
        scheduler = Scheduler(available_time=60)
        task = Task(
            name="Grooming session",
            duration_minutes=30,
            priority=2,
            frequency="weekly",
            due_date=today
        )
        scheduler.add_task(task)
        
        # Act: Complete the task
        next_task = scheduler.complete_task("Grooming session")
        
        # Assert: New task created for 7 days later
        assert next_task is not None
        assert next_task.due_date == today + timedelta(days=7)
    
    def test_one_time_task_no_next_occurrence(self):
        # Arrange: Create a one-time task
        scheduler = Scheduler(available_time=60)
        task = Task(
            name="Vet appointment",
            duration_minutes=60,
            priority=1,
            frequency="once"
        )
        scheduler.add_task(task)
        
        # Act: Complete the task
        next_task = scheduler.complete_task("Vet appointment")
        
        # Assert: No new task created
        assert next_task is None
    
    def test_recurring_task_preserves_attributes(self):
        # Arrange: Create a daily task with specific attributes
        scheduler = Scheduler(available_time=60)
        task = Task(
            name="Morning walk",
            duration_minutes=30,
            priority=1,
            frequency="daily",
            pet_name="Buddy",
            preferred_time="morning",
            start_time=time(8, 0)
        )
        scheduler.add_task(task)
        
        # Act: Complete the task
        next_task = scheduler.complete_task("Morning walk")
        
        # Assert: New task preserves all attributes
        assert next_task.pet_name == "Buddy"
        assert next_task.preferred_time == "morning"
        assert next_task.start_time == time(8, 0)
        assert next_task.priority == 1
        assert next_task.duration_minutes == 30
    
    def test_daily_task_across_month_boundary(self):
        # Arrange: Create a daily task on last day of January
        jan_31 = date(2026, 1, 31)
        scheduler = Scheduler(available_time=60)
        task = Task(
            name="Evening feeding",
            duration_minutes=10,
            priority=1,
            frequency="daily",
            due_date=jan_31
        )
        scheduler.add_task(task)
        
        # Act: Complete the task
        next_task = scheduler.complete_task("Evening feeding")
        
        # Assert: New task should be Feb 1
        assert next_task.due_date == date(2026, 2, 1)


class TestConflictDetection:
    """Test conflict detection for overlapping task times."""
    
    def test_adjacent_tasks_no_conflict(self):
        # Arrange: Create two tasks that touch but don't overlap (8:00-8:30 and 8:30-9:00)
        scheduler = Scheduler(available_time=120)
        task1 = Task(
            name="Morning walk",
            duration_minutes=30,
            priority=1,
            start_time=time(8, 0)
        )
        task2 = Task(
            name="Breakfast",
            duration_minutes=30,
            priority=1,
            start_time=time(8, 30)
        )
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        # Act: Check for conflicts
        has_conflict = scheduler.has_conflicts()
        
        # Assert: No conflict (end time equals start time is not overlap)
        assert has_conflict is False
    
    def test_overlapping_tasks_detected(self):
        # Arrange: Create two overlapping tasks (8:00-9:00 and 8:30-9:30)
        scheduler = Scheduler(available_time=120)
        task1 = Task(
            name="Long walk",
            duration_minutes=60,
            priority=1,
            start_time=time(8, 0)
        )
        task2 = Task(
            name="Grooming",
            duration_minutes=60,
            priority=2,
            start_time=time(8, 30)
        )
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        # Act: Check for conflicts
        conflicts = scheduler.detect_conflicts()
        
        # Assert: Conflict detected
        assert len(conflicts) == 1
        assert conflicts[0][0].name == "Long walk"
        assert conflicts[0][1].name == "Grooming"
    
    def test_same_start_time_conflict(self):
        # Arrange: Create two tasks at the exact same time
        scheduler = Scheduler(available_time=120)
        task1 = Task(
            name="Feed cat",
            duration_minutes=10,
            priority=1,
            start_time=time(9, 0),
            pet_name="Whiskers"
        )
        task2 = Task(
            name="Feed dog",
            duration_minutes=10,
            priority=1,
            start_time=time(9, 0),
            pet_name="Buddy"
        )
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        # Act: Check for conflicts
        has_conflict = scheduler.has_conflicts()
        conflicts = scheduler.detect_conflicts()
        
        # Assert: Conflict detected (owner can't do both at once)
        assert has_conflict is True
        assert conflicts[0][2] == "different_pets"
    
    def test_no_start_time_no_conflict(self):
        # Arrange: Create two tasks without start times
        scheduler = Scheduler(available_time=120)
        task1 = Task(name="Walk", duration_minutes=30, priority=1)
        task2 = Task(name="Feed", duration_minutes=10, priority=1)
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        # Act: Check overlap
        overlaps = task1.overlaps_with(task2)
        has_conflict = scheduler.has_conflicts()
        
        # Assert: No conflict detectable without start times
        assert overlaps is False
        assert has_conflict is False
    
    def test_completed_tasks_excluded_from_conflicts(self):
        # Arrange: Create two overlapping tasks, mark one complete
        scheduler = Scheduler(available_time=120)
        task1 = Task(
            name="Completed task",
            duration_minutes=60,
            priority=1,
            start_time=time(8, 0)
        )
        task1.mark_complete()
        task2 = Task(
            name="Active task",
            duration_minutes=60,
            priority=1,
            start_time=time(8, 30)
        )
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        # Act: Check for conflicts
        has_conflict = scheduler.has_conflicts()
        
        # Assert: No conflict (completed tasks excluded)
        assert has_conflict is False


class TestScheduleGeneration:
    """Test schedule generation with time constraints."""
    
    def test_generate_plan_exact_fit(self):
        # Arrange: Tasks totaling exactly available time
        scheduler = Scheduler(available_time=60)
        scheduler.add_task(Task(name="Task 1", duration_minutes=30, priority=1))
        scheduler.add_task(Task(name="Task 2", duration_minutes=30, priority=2))
        
        # Act: Generate plan
        plan = scheduler.generate_plan()
        
        # Assert: All tasks scheduled, none unscheduled
        assert len(plan.scheduled_tasks) == 2
        assert len(plan.unscheduled_tasks) == 0
        assert plan.total_duration == 60
    
    def test_generate_plan_task_too_big(self):
        # Arrange: Single task exceeding available time
        scheduler = Scheduler(available_time=30)
        scheduler.add_task(Task(name="Long task", duration_minutes=60, priority=1))
        
        # Act: Generate plan
        plan = scheduler.generate_plan()
        
        # Assert: Task goes to unscheduled
        assert len(plan.scheduled_tasks) == 0
        assert len(plan.unscheduled_tasks) == 1
        assert plan.unscheduled_tasks[0].name == "Long task"
    
    def test_generate_plan_priority_order(self):
        # Arrange: Multiple tasks where not all can fit
        scheduler = Scheduler(available_time=50)
        scheduler.add_task(Task(name="Low priority", duration_minutes=30, priority=5))
        scheduler.add_task(Task(name="High priority", duration_minutes=30, priority=1))
        scheduler.add_task(Task(name="Medium priority", duration_minutes=30, priority=3))
        
        # Act: Generate plan
        plan = scheduler.generate_plan()
        
        # Assert: Higher priority tasks scheduled first
        assert len(plan.scheduled_tasks) == 1
        assert plan.scheduled_tasks[0].name == "High priority"
        assert len(plan.unscheduled_tasks) == 2
    
    def test_generate_plan_all_completed(self):
        # Arrange: All tasks already completed
        scheduler = Scheduler(available_time=60)
        task1 = Task(name="Done task 1", duration_minutes=20, priority=1)
        task1.mark_complete()
        task2 = Task(name="Done task 2", duration_minutes=20, priority=2)
        task2.mark_complete()
        scheduler.add_task(task1)
        scheduler.add_task(task2)
        
        # Act: Generate plan
        plan = scheduler.generate_plan()
        
        # Assert: No tasks scheduled (all completed)
        assert len(plan.scheduled_tasks) == 0
        assert len(plan.unscheduled_tasks) == 0
    
    def test_generate_plan_zero_available_time(self):
        # Arrange: Zero available time
        scheduler = Scheduler(available_time=0)
        scheduler.add_task(Task(name="Any task", duration_minutes=10, priority=1))
        
        # Act: Generate plan
        plan = scheduler.generate_plan()
        
        # Assert: All tasks unscheduled
        assert len(plan.scheduled_tasks) == 0
        assert len(plan.unscheduled_tasks) == 1
    
    def test_generate_plan_empty_tasks(self):
        # Arrange: No tasks
        scheduler = Scheduler(available_time=60)
        
        # Act: Generate plan
        plan = scheduler.generate_plan()
        
        # Assert: Empty plan
        assert len(plan.scheduled_tasks) == 0
        assert len(plan.unscheduled_tasks) == 0
        assert plan.total_duration == 0


class TestValidation:
    """Test input validation for Task and Owner."""
    
    def test_negative_duration_raises_error(self):
        # Arrange/Act/Assert: Negative duration should raise ValueError
        with pytest.raises(ValueError, match="Duration must be a positive number"):
            Task(name="Invalid", duration_minutes=-5, priority=1)
    
    def test_priority_below_range_raises_error(self):
        # Arrange/Act/Assert: Priority 0 should raise ValueError
        with pytest.raises(ValueError, match="Priority must be between 1"):
            Task(name="Invalid", duration_minutes=10, priority=0)
    
    def test_priority_above_range_raises_error(self):
        # Arrange/Act/Assert: Priority 6 should raise ValueError
        with pytest.raises(ValueError, match="Priority must be between 1"):
            Task(name="Invalid", duration_minutes=10, priority=6)
    
    def test_invalid_frequency_raises_error(self):
        # Arrange/Act/Assert: Invalid frequency should raise ValueError
        with pytest.raises(ValueError, match="Frequency must be"):
            Task(name="Invalid", duration_minutes=10, priority=1, frequency="monthly")
    
    def test_negative_available_time_raises_error(self):
        # Arrange/Act/Assert: Negative available time should raise ValueError
        with pytest.raises(ValueError, match="Available time must be a positive number"):
            Owner(name="Test Owner", available_time_minutes=-10)
