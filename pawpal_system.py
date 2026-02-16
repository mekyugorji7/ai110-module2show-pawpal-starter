"""
PawPal+ System Classes
A pet care task scheduling system.
"""

from dataclasses import dataclass, field
from typing import Optional, List
from datetime import date


@dataclass
class Task:
    """Represents a pet care task with duration and priority."""
    
    name: str
    duration_minutes: int
    priority: int  # 1 = highest priority, 5 = lowest priority
    task_type: str = "general"
    is_completed: bool = False
    pet_name: Optional[str] = None  # Links task to a specific pet
    
    def __post_init__(self):
        """Validate task attributes after initialization."""
        if self.duration_minutes < 0:
            raise ValueError("Duration must be a positive number")
        if not 1 <= self.priority <= 5:
            raise ValueError("Priority must be between 1 (highest) and 5 (lowest)")
    
    def mark_complete(self) -> None:
        """Mark the task as completed."""
        self.is_completed = True
    
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
            "pet_name": self.pet_name
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
    
    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        self.tasks.append(task)
    
    def remove_task(self, task_name: str) -> bool:
        """Remove a task by name from the scheduler. Returns True if found and removed."""
        for task in self.tasks:
            if task.name == task_name:
                self.tasks.remove(task)
                return True
        return False
    
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
