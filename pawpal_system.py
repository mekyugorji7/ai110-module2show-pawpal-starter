"""
PawPal+ System Classes
A pet care task scheduling system.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import date, timedelta, time, datetime


@dataclass
class Task:
    """Represents a pet care task with duration and priority."""
    
    name: str
    duration_minutes: int
    priority: int  # 1 = highest priority, 5 = lowest priority
    task_type: str = "general"
    is_completed: bool = False
    pet_name: Optional[str] = None  # Links task to a specific pet
    preferred_time: str = "morning"  # Options: "morning", "afternoon", "evening"
    frequency: str = "once"  # Options: "once", "daily", "weekly"
    due_date: date = field(default_factory=date.today)  # When the task is due
    start_time: Optional[time] = None  # Specific start time (e.g., time(8, 30) for 8:30 AM)
    
    def __post_init__(self):
        """Validate task attributes after initialization."""
        if self.duration_minutes < 0:
            raise ValueError("Duration must be a positive number")
        if not 1 <= self.priority <= 5:
            raise ValueError("Priority must be between 1 (highest) and 5 (lowest)")
        if self.frequency not in ["once", "daily", "weekly"]:
            raise ValueError("Frequency must be 'once', 'daily', or 'weekly'")
    
    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.is_completed = True
    
    def get_end_time(self) -> Optional[time]:
        """Calculate the end time based on start_time and duration.
        
        Returns:
            The end time if start_time is set, None otherwise.
        """
        if self.start_time is None:
            return None
        
        # Convert start_time to datetime, add duration, extract time
        start_dt = datetime.combine(date.today(), self.start_time)
        end_dt = start_dt + timedelta(minutes=self.duration_minutes)
        return end_dt.time()
    
    def overlaps_with(self, other: "Task") -> bool:
        """Check if this task's time overlaps with another task.
        
        Args:
            other: Another Task to check for overlap.
        
        Returns:
            True if the tasks overlap in time, False otherwise.
        """
        # Can't detect overlap without start times
        if self.start_time is None or other.start_time is None:
            return False
        
        self_end = self.get_end_time()
        other_end = other.get_end_time()
        
        if self_end is None or other_end is None:
            return False
        
        # Check for overlap: A overlaps B if A starts before B ends AND A ends after B starts
        return self.start_time < other_end and self_end > other.start_time
    
    def create_next_occurrence(self) -> Optional["Task"]:
        """Create the next occurrence of a recurring task.
        
        Uses timedelta to calculate the next due date:
        - Daily tasks: due_date + 1 day
        - Weekly tasks: due_date + 7 days
        
        Returns:
            A new Task instance if this is a recurring task, None if frequency is 'once'.
        """
        if self.frequency == "once":
            return None
        
        # Calculate next due date using timedelta
        if self.frequency == "daily":
            next_due = self.due_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_due = self.due_date + timedelta(days=7)
        else:
            next_due = self.due_date
        
        # Create a new task with the same attributes but not completed
        return Task(
            name=self.name,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            task_type=self.task_type,
            is_completed=False,
            pet_name=self.pet_name,
            preferred_time=self.preferred_time,
            frequency=self.frequency,
            due_date=next_due,
            start_time=self.start_time  # Keep the same scheduled time
        )
    
    def update_priority(self, new_priority: int) -> None:
        """Update the task's priority level."""
        if not 1 <= new_priority <= 5:
            raise ValueError("Priority must be between 1 (highest) and 5 (lowest)")
        self.priority = new_priority
    
    def get_info(self) -> dict:
        """Return task information as a dictionary."""
        return {
            "name": self.name,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "task_type": self.task_type,
            "is_completed": self.is_completed,
            "pet_name": self.pet_name,
            "preferred_time": self.preferred_time,
            "frequency": self.frequency,
            "due_date": str(self.due_date),
            "start_time": str(self.start_time) if self.start_time else None,
            "end_time": str(self.get_end_time()) if self.start_time else None
        }


@dataclass
class Pet:
    """Represents a pet with its basic information and special needs."""
    
    name: str
    pet_type: str
    age: int = 0
    special_needs: List[str] = field(default_factory=list)
    tasks: List[Task] = field(default_factory=list)  # Tasks for this pet
    
    def add_special_need(self, need: str) -> None:
        """Add a special need for the pet."""
        if need not in self.special_needs:
            self.special_needs.append(need)
    
    def add_task(self, task: Task) -> None:
        """Add a task for this pet."""
        task.pet_name = self.name
        self.tasks.append(task)
    
    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks
    
    def get_info(self) -> dict:
        """Return pet information as a dictionary."""
        return {
            "name": self.name,
            "pet_type": self.pet_type,
            "age": self.age,
            "special_needs": self.special_needs,
            "task_count": len(self.tasks)
        }


@dataclass
class Owner:
    """Represents the pet owner with their constraints and preferences."""
    
    name: str
    available_time_minutes: int = 60
    preferences: List[str] = field(default_factory=list)
    pets: List[Pet] = field(default_factory=list)  # Owner's pets
    
    def __post_init__(self):
        """Validate owner attributes after initialization."""
        if self.available_time_minutes < 0:
            raise ValueError("Available time must be a positive number")
    
    def set_available_time(self, minutes: int) -> None:
        """Set the owner's available time for pet care tasks."""
        if minutes < 0:
            raise ValueError("Available time must be a positive number")
        self.available_time_minutes = minutes
    
    def add_preference(self, preference: str) -> None:
        """Add a care preference for the owner."""
        if preference not in self.preferences:
            self.preferences.append(preference)
    
    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks from all pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks
    
    def get_info(self) -> dict:
        """Return owner information as a dictionary."""
        return {
            "name": self.name,
            "available_time_minutes": self.available_time_minutes,
            "preferences": self.preferences,
            "pet_count": len(self.pets)
        }


@dataclass
class DailyPlan:
    """Represents a generated daily schedule with tasks and reasoning."""
    
    scheduled_tasks: List[Task] = field(default_factory=list)
    unscheduled_tasks: List[Task] = field(default_factory=list)  # Tasks that didn't fit
    total_duration: int = 0
    reasoning: str = ""
    plan_date: date = field(default_factory=date.today)
    
    def add_task(self, task: Task) -> None:
        """Add a task to the daily plan."""
        self.scheduled_tasks.append(task)
        self.total_duration += task.duration_minutes
    
    def add_unscheduled_task(self, task: Task) -> None:
        """Add a task that couldn't be scheduled."""
        self.unscheduled_tasks.append(task)
    
    def get_summary(self) -> str:
        """Return a summary of the daily plan."""
        scheduled_count = len(self.scheduled_tasks)
        unscheduled_count = len(self.unscheduled_tasks)
        summary = f"Daily Plan for {self.plan_date}\n"
        summary += f"Scheduled: {scheduled_count} tasks ({self.total_duration} minutes)\n"
        if unscheduled_count > 0:
            summary += f"Unscheduled: {unscheduled_count} tasks (not enough time)\n"
        return summary
    
    def explain_reasoning(self) -> str:
        """Return the reasoning behind the schedule."""
        return self.reasoning
    
    def display(self) -> str:
        """Display the daily plan as a formatted string."""
        output = self.get_summary()
        output += "\n--- Scheduled Tasks ---\n"
        for i, task in enumerate(self.scheduled_tasks, 1):
            output += f"{i}. {task.name} ({task.duration_minutes} min, priority {task.priority})\n"
        if self.unscheduled_tasks:
            output += "\n--- Could Not Schedule ---\n"
            for task in self.unscheduled_tasks:
                output += f"- {task.name} ({task.duration_minutes} min)\n"
        return output


class Scheduler:
    """Handles scheduling logic to generate daily plans from tasks."""
    
    def __init__(self, owner: Optional[Owner] = None, available_time: int = 60):
        """Initialize the scheduler with owner and available time constraint."""
        self.owner: Optional[Owner] = owner
        self.tasks: List[Task] = []
        # Use owner's available time if provided, otherwise use parameter
        if owner:
            self.available_time: int = owner.available_time_minutes
        else:
            self.available_time: int = available_time
    
    def add_task(self, task: Task, check_conflicts: bool = False) -> Optional[str]:
        """Add a task to the scheduler.
        
        Args:
            task: The task to add.
            check_conflicts: If True, check for conflicts and return warning message.
        
        Returns:
            Warning message if conflicts detected and check_conflicts=True, None otherwise.
        """
        warning = None
        
        if check_conflicts and task.start_time is not None:
            # Check if new task conflicts with existing tasks
            for existing_task in self.tasks:
                if existing_task.start_time is not None and not existing_task.is_completed:
                    if task.overlaps_with(existing_task):
                        if task.pet_name == existing_task.pet_name:
                            warning = (f"⚠️  WARNING: '{task.name}' conflicts with '{existing_task.name}' "
                                      f"(same pet: {task.pet_name})")
                        else:
                            warning = (f"⚠️  WARNING: '{task.name}' conflicts with '{existing_task.name}' "
                                      f"(owner can't do both at once)")
                        break
        
        # Always add the task (lightweight - doesn't block)
        self.tasks.append(task)
        return warning
    
    def remove_task(self, task_name: str) -> bool:
        """Remove a task by name from the scheduler. Returns True if found and removed."""
        for task in self.tasks:
            if task.name == task_name:
                self.tasks.remove(task)
                return True
        return False
    
    def complete_task(self, task_name: str) -> Optional[Task]:
        """Mark a task as complete and create next occurrence if recurring.
        
        Args:
            task_name: The name of the task to complete.
        
        Returns:
            The new Task instance if recurring, None otherwise.
        """
        for task in self.tasks:
            if task.name == task_name and not task.is_completed:
                # Mark the current task as complete
                task.mark_complete()
                
                # If recurring, create the next occurrence
                if task.frequency in ["daily", "weekly"]:
                    next_task = task.create_next_occurrence()
                    if next_task:
                        self.tasks.append(next_task)
                        return next_task
                return None
        return None
    
    def edit_task(self, task_name: str, **kwargs) -> bool:
        """Edit a task's attributes by name. Returns True if found and edited."""
        for task in self.tasks:
            if task.name == task_name:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                return True
        return False
    
    def sort_by_priority(self) -> List[Task]:
        """Sort and return tasks by priority (highest/1 first)."""
        return sorted(self.tasks, key=lambda t: t.priority)
    
    def sort_by_time(self) -> List[Task]:
        """Sort tasks by preferred time slot (morning -> afternoon -> evening)."""
        time_order = {"morning": 1, "afternoon": 2, "evening": 3}
        return sorted(self.tasks, key=lambda t: time_order.get(t.preferred_time, 4))
    
    def filter_by_completion(self, completed: bool = False) -> List[Task]:
        """Filter tasks by completion status.
        
        Args:
            completed: If True, return completed tasks. If False, return incomplete tasks.
        
        Returns:
            List of tasks matching the completion status.
        """
        return [task for task in self.tasks if task.is_completed == completed]
    
    def filter_by_pet(self, pet_name: str) -> List[Task]:
        """Filter tasks by pet name.
        
        Args:
            pet_name: The name of the pet to filter tasks for.
        
        Returns:
            List of tasks assigned to the specified pet.
        """
        return [task for task in self.tasks if task.pet_name == pet_name]
    
    def detect_conflicts(self) -> List[tuple]:
        """Detect time conflicts between tasks.
        
        A conflict occurs when two tasks have overlapping time ranges.
        
        Returns:
            List of tuples (task1, task2, conflict_type) for each conflict found.
            conflict_type is 'same_pet' or 'different_pets'.
        """
        conflicts = []
        incomplete_tasks = self.filter_by_completion(completed=False)
        
        # Only check tasks that have start times
        timed_tasks = [t for t in incomplete_tasks if t.start_time is not None]
        
        # Compare each pair of tasks
        for i, task1 in enumerate(timed_tasks):
            for task2 in timed_tasks[i + 1:]:
                if task1.overlaps_with(task2):
                    # Determine conflict type
                    if task1.pet_name == task2.pet_name:
                        conflict_type = "same_pet"
                    else:
                        conflict_type = "different_pets"
                    conflicts.append((task1, task2, conflict_type))
        
        return conflicts
    
    def has_conflicts(self) -> bool:
        """Check if there are any time conflicts in the schedule.
        
        Returns:
            True if conflicts exist, False otherwise.
        """
        return len(self.detect_conflicts()) > 0
    
    def get_conflict_report(self) -> str:
        """Generate a human-readable report of all conflicts.
        
        Returns:
            A formatted string describing all conflicts found.
        """
        conflicts = self.detect_conflicts()
        
        if not conflicts:
            return "No scheduling conflicts detected."
        
        report = f"Found {len(conflicts)} conflict(s):\n"
        for i, (task1, task2, conflict_type) in enumerate(conflicts, 1):
            task1_time = f"{task1.start_time.strftime('%H:%M')}-{task1.get_end_time().strftime('%H:%M')}"
            task2_time = f"{task2.start_time.strftime('%H:%M')}-{task2.get_end_time().strftime('%H:%M')}"
            
            if conflict_type == "same_pet":
                report += f"\n  {i}. CONFLICT (same pet - {task1.pet_name}):\n"
            else:
                report += f"\n  {i}. CONFLICT (owner can't do both at once):\n"
            
            report += f"     - '{task1.name}' ({task1_time})\n"
            report += f"     - '{task2.name}' ({task2_time})\n"
        
        return report
    
    def fits_in_time(self, task: Task, remaining_time: int) -> bool:
        """Check if a task fits within the remaining available time."""
        return task.duration_minutes <= remaining_time
    
    def generate_plan(self) -> DailyPlan:
        """Generate a daily plan based on priorities and time constraints."""
        plan = DailyPlan()
        remaining_time = self.available_time
        reasoning_parts = []
        
        # Sort tasks by priority (1 = highest)
        sorted_tasks = self.sort_by_priority()
        reasoning_parts.append(f"Sorted {len(sorted_tasks)} tasks by priority.")
        
        # Schedule tasks that fit within available time
        for task in sorted_tasks:
            if task.is_completed:
                reasoning_parts.append(f"Skipped '{task.name}' - already completed.")
                continue
                
            if self.fits_in_time(task, remaining_time):
                plan.add_task(task)
                remaining_time -= task.duration_minutes
                reasoning_parts.append(
                    f"Scheduled '{task.name}' (priority {task.priority}, {task.duration_minutes} min). "
                    f"Remaining time: {remaining_time} min."
                )
            else:
                plan.add_unscheduled_task(task)
                reasoning_parts.append(
                    f"Could not schedule '{task.name}' - needs {task.duration_minutes} min, "
                    f"only {remaining_time} min remaining."
                )
        
        plan.reasoning = "\n".join(reasoning_parts)
        return plan
    
    def clear_tasks(self) -> None:
        """Clear all tasks from the scheduler."""
        self.tasks = []
    
    def get_tasks(self) -> List[Task]:
        """Return all tasks in the scheduler."""
        return self.tasks
