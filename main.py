"""
PawPal+ Demo Script
Demonstrates the scheduling system with an owner, pets, and tasks.
"""

from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    # Create an owner with 60 minutes of available time
    owner = Owner(name="Sarah", available_time_minutes=60)
    
    # Create two pets
    dog = Pet(name="Buddy", pet_type="dog", age=3)
    cat = Pet(name="Whiskers", pet_type="cat", age=5)
    
    # Add tasks to the dog (different durations and priorities)
    dog.add_task(Task(name="Morning walk", duration_minutes=25, priority=1, task_type="exercise"))
    dog.add_task(Task(name="Feed breakfast", duration_minutes=10, priority=1, task_type="feeding"))
    dog.add_task(Task(name="Play fetch", duration_minutes=20, priority=3, task_type="enrichment"))
    
    # Add tasks to the cat
    cat.add_task(Task(name="Feed breakfast", duration_minutes=5, priority=1, task_type="feeding"))
    cat.add_task(Task(name="Brush fur", duration_minutes=15, priority=2, task_type="grooming"))
    cat.add_task(Task(name="Interactive toy time", duration_minutes=15, priority=4, task_type="enrichment"))
    
    # Add pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)
    
    # Create scheduler with the owner
    scheduler = Scheduler(owner=owner)
    
    # Load all tasks from owner's pets into the scheduler
    for task in owner.get_all_tasks():
        scheduler.add_task(task)
    
    # Generate the daily plan
    plan = scheduler.generate_plan()
    
    # Print Today's Schedule
    print("=" * 50)
    print("🐾 PawPal+ - Today's Schedule 🐾")
    print("=" * 50)
    print(f"Owner: {owner.name}")
    print(f"Available time: {owner.available_time_minutes} minutes")
    print(f"Pets: {', '.join([pet.name for pet in owner.pets])}")
    print("=" * 50)
    print(plan.display())
    print("=" * 50)
    print("Reasoning:")
    print(plan.explain_reasoning())


if __name__ == "__main__":
    main()
