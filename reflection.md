# PawPal+ Project Reflection

## 1. System Design

The three core actions a user should be able to perform are:
- Entering Pet/Owner Information about themselves and their pet (name, pet name, pet species)
- Adding and Editing Tasks with duration and priority
- Generate Schedule based on added tasks


**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

I had 5 classes in my design:

- **Owner**: Stores owner information and time constraints. Responsible for tracking the pet owner's name, how much time they have available for pet care (in minutes), and their preferences. Key methods include setting available time and retrieving owner info.

- **Pet**: Stores pet information. Responsible for tracking the pet's name, type (dog, cat, etc.), age, and any special needs. This class allows adding special needs and retrieving pet details.

- **Task**: Stores task details including duration, priority, and type. Responsible for representing individual care tasks like walks, feeding, or medications. Each task has a priority level (1 = highest, 5 = lowest) and can be marked as complete.

- **Scheduler**: Contains the core logic for generating and sorting plans. Responsible for adding/removing tasks, sorting them by priority, checking if tasks fit within available time, and producing a DailyPlan based on constraints.

- **DailyPlan**: Stores the generated schedule and reasoning. Responsible for holding the list of scheduled tasks, calculating total duration, and explaining why tasks were scheduled in a particular order.


**b. Design changes**

- Did your design change during implementation?

Yes

classDiagram
    class Owner {
        +name: str
        +available_time_minutes: int
        +preferences: List~str~
        +pets: List~Pet~
        +add_pet(pet)
        +get_all_tasks() List~Task~
    }
    
    class Pet {
        +name: str
        +pet_type: str
        +tasks: List~Task~
        +add_task(task)
        +get_tasks() List~Task~
    }
    
    class Task {
        +name: str
        +duration_minutes: int
        +priority: int
        +pet_name: str
        +mark_complete()
        +update_priority()
    }
    
    class Scheduler {
        +owner: Owner
        +tasks: List~Task~
        +add_task()
        +edit_task()
        +remove_task()
        +generate_plan() DailyPlan
    }
    
    class DailyPlan {
        +scheduled_tasks: List~Task~
        +unscheduled_tasks: List~Task~
        +total_duration: int
        +reasoning: str
        +display() str
    }
    
    Owner "1" --> "*" Pet : owns
    Pet "1" --> "*" Task : has
    Scheduler --> Owner : uses
    Scheduler --> DailyPlan : generates

- If yes, describe at least one change and why you made it.

- Added pets: List[Pet] attribute and add_pet to owner class, original design had no way to track which bets belonged to which owner
- Added tasks: List[Task] to Pet and pet_name to Task, tasks weren't linked to specific pets in the original design, if an owner has a dog and a cat, we need to know which tasks belong to which pet
- Scheduler now accepts an Owner object instead of just available_time as the original design passed only the time constraint. By passing the full Owner, the scheduler can access preferences and potentially adjust scheduling based on owner needs—not just time.


## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
