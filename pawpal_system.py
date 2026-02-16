"""
PawPal+ System Classes
A pet care task scheduling system.
"""

from dataclasses import dataclass, field
from typing import Optional
from datetime import date


@dataclass
class Owner:
    """Represents the pet owner with their constraints and preferences."""
    
    name: str
    available_time_minutes: int = 60
    preferences: list = field(default_factory=list)
    
    def set_available_time(self, minutes: int) -> None:
        """Set the owner's available time for pet care tasks."""
        pass
    
    def add_preference(self, preference: str) -> None:
        """Add a care preference for the owner."""
        pass
    
    def get_info(self) -> dict:
        """Return owner information as a dictionary."""
        pass


@dataclass
class Pet:
    """Represents a pet with its basic information and special needs."""
    
    name: str
    pet_type: str
    age: int = 0
    special_needs: list = field(default_factory=list)
    
    def add_special_need(self, need: str) -> None:
        """Add a special need for the pet."""
        pass
    
    def get_info(self) -> dict:
        """Return pet information as a dictionary."""
        pass


@dataclass
class Task:
    """Represents a pet care task with duration and priority."""
    
    name: str
    duration_minutes: int
    priority: int  # 1 = highest priority, 5 = lowest priority
    task_type: str = "general"
    is_completed: bool = False
    
    def mark_complete(self) -> None:
        """Mark the task as completed."""
        pass
    
    def update_priority(self, new_priority: int) -> None:
        """Update the task's priority level."""
        pass
    
    def get_info(self) -> dict:
        """Return task information as a dictionary."""
        pass


@dataclass
class DailyPlan:
    """Represents a generated daily schedule with tasks and reasoning."""
    
    scheduled_tasks: list = field(default_factory=list)
    total_duration: int = 0
    reasoning: str = ""
    plan_date: date = field(default_factory=date.today)
    
    def add_task(self, task: Task) -> None:
        """Add a task to the daily plan."""
        pass
    
    def get_summary(self) -> str:
        """Return a summary of the daily plan."""
        pass
    
    def explain_reasoning(self) -> str:
        """Return the reasoning behind the schedule."""
        pass
    
    def display(self) -> None:
        """Display the daily plan."""
        pass


class Scheduler:
    """Handles scheduling logic to generate daily plans from tasks."""
    
    def __init__(self, available_time: int = 60):
        """Initialize the scheduler with available time constraint."""
        self.tasks: list = []
        self.available_time: int = available_time
    
    def add_task(self, task: Task) -> None:
        """Add a task to the scheduler."""
        pass
    
    def remove_task(self, task_name: str) -> None:
        """Remove a task by name from the scheduler."""
        pass
    
    def sort_by_priority(self) -> list:
        """Sort and return tasks by priority (highest first)."""
        pass
    
    def fits_in_time(self, task: Task) -> bool:
        """Check if a task fits within the remaining available time."""
        pass
    
    def generate_plan(self) -> DailyPlan:
        """Generate a daily plan based on priorities and time constraints."""
        pass
