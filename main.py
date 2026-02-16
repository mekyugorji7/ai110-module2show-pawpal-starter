"""
PawPal+ Demo Script
Demonstrates the scheduling system with lightweight conflict detection.
Warnings are printed but the program continues running.
"""

from datetime import time
from pawpal_system import Owner, Pet, Task, Scheduler


def main():
    print("=" * 65)
    print("PawPal+ - Lightweight Conflict Detection Demo")
    print("=" * 65)
    print("\nThis demo shows that conflicts trigger WARNINGS, not crashes.")
    print("The program continues to run even when conflicts are detected.\n")
    
    # Create owner and scheduler
    owner = Owner(name="Sarah", available_time_minutes=120)
    scheduler = Scheduler(owner=owner)
    
    # ========== ADD TASKS WITH CONFLICT CHECKING ==========
    print("-" * 65)
    print("ADDING TASKS (with conflict checking enabled)")
    print("-" * 65)
    
    # Task 1: Morning walk at 7:00 AM (no conflict yet)
    task1 = Task(
        name="Morning walk", 
        duration_minutes=30, 
        priority=1, 
        pet_name="Buddy",
        start_time=time(7, 0)  # 7:00 AM - 7:30 AM
    )
    warning = scheduler.add_task(task1, check_conflicts=True)
    print(f"\n1. Added: 'Morning walk' (07:00 - 07:30) for Buddy")
    if warning:
        print(f"   {warning}")
    else:
        print("   ✓ No conflicts")
    
    # Task 2: Buddy breakfast at 7:15 AM (CONFLICTS with morning walk - same pet!)
    task2 = Task(
        name="Buddy breakfast", 
        duration_minutes=10, 
        priority=1, 
        pet_name="Buddy",
        start_time=time(7, 15)  # 7:15 AM - 7:25 AM (OVERLAPS!)
    )
    warning = scheduler.add_task(task2, check_conflicts=True)
    print(f"\n2. Added: 'Buddy breakfast' (07:15 - 07:25) for Buddy")
    if warning:
        print(f"   {warning}")
    else:
        print("   ✓ No conflicts")
    
    # Task 3: Whiskers breakfast at 7:20 AM (CONFLICTS - different pet but owner busy)
    task3 = Task(
        name="Whiskers breakfast", 
        duration_minutes=10, 
        priority=1, 
        pet_name="Whiskers",
        start_time=time(7, 20)  # 7:20 AM - 7:30 AM (OVERLAPS!)
    )
    warning = scheduler.add_task(task3, check_conflicts=True)
    print(f"\n3. Added: 'Whiskers breakfast' (07:20 - 07:30) for Whiskers")
    if warning:
        print(f"   {warning}")
    else:
        print("   ✓ No conflicts")
    
    # Task 4: Afternoon play at 2:00 PM (no conflict)
    task4 = Task(
        name="Afternoon play", 
        duration_minutes=20, 
        priority=3, 
        pet_name="Buddy",
        start_time=time(14, 0)  # 2:00 PM - 2:20 PM
    )
    warning = scheduler.add_task(task4, check_conflicts=True)
    print(f"\n4. Added: 'Afternoon play' (14:00 - 14:20) for Buddy")
    if warning:
        print(f"   {warning}")
    else:
        print("   ✓ No conflicts")
    
    # Task 5: Brush fur at 2:00 PM (CONFLICTS with afternoon play - same time!)
    task5 = Task(
        name="Brush Whiskers", 
        duration_minutes=15, 
        priority=2, 
        pet_name="Whiskers",
        start_time=time(14, 0)  # 2:00 PM - 2:15 PM (SAME TIME!)
    )
    warning = scheduler.add_task(task5, check_conflicts=True)
    print(f"\n5. Added: 'Brush Whiskers' (14:00 - 14:15) for Whiskers")
    if warning:
        print(f"   {warning}")
    else:
        print("   ✓ No conflicts")
    
    # ========== PROGRAM CONTINUES DESPITE CONFLICTS ==========
    print("\n" + "=" * 65)
    print("PROGRAM CONTINUES RUNNING (lightweight approach)")
    print("=" * 65)
    
    print(f"\nTotal tasks added: {len(scheduler.get_tasks())}")
    print("\nAll tasks in scheduler:")
    print("-" * 50)
    for task in scheduler.get_tasks():
        end_time = task.get_end_time()
        print(f"  {task.start_time.strftime('%H:%M')} - {end_time.strftime('%H:%M')}: {task.name} ({task.pet_name})")
    
    # ========== FULL CONFLICT REPORT ==========
    print("\n" + "=" * 65)
    print("FULL CONFLICT REPORT")
    print("=" * 65)
    
    if scheduler.has_conflicts():
        print(f"\n{scheduler.get_conflict_report()}")
    else:
        print("\n✓ No conflicts detected.")
    
    


if __name__ == "__main__":
    main()
