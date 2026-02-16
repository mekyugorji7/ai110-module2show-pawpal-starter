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

The scheduler considers four main constraints:

1. Available Time - The owner's total time budget 

2. Task Priority - Each task has a priority level (1 = highest, 5 = lowest). Higher priority tasks are scheduled first.

3. Task Duration - How long each task takes. The scheduler checks if a task fits before adding it.

4. Time Conflicts - If tasks have specific start times, the scheduler detects overlapping tasks (same pet or different pets) and warns the user.

- How did you decide which constraints mattered most?

Priority was chosen as the primary constraint because in pet care, some tasks are non-negotiable (medications, feeding) while others are flexible like playtime and grooming. A pet owner would rather skip a low-priority task than miss giving their pet medication. Time budgeting is the hard limit—you can't schedule more than you have time for.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes

The scheduler uses a greedy algorithm that adds tasks in priority order until time runs out rather than maximizing the number of tasks. It doesn't backtrack or swap tasks to find the optimal combination that might fit more tasks overall.

For example, if you have 30 minutes available and tasks of [25 min (priority 1), 10 min (priority 2), 10 min (priority 3)], the scheduler picks the 25-min task first, leaving only 5 minutes, wasting potential time.

- Why is that tradeoff reasonable for this scenario?

Pet owners need a clear, predictable schedule. In pet care, high-priority tasks (medications, feeding) genuinely need to happen first. Using a greedy approach to skip more low-priority tasks than a priority-1 task is the most reasonable in this scenario.


## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI during this project to plan, brainstorm, implement, and test my code. The kind of prompts that were most helpful in using this project were ones that questioned my interpretation of the project. Having a second pair of eyes through AI look at my code really helped me find other ways I could implementfeatures I wanted to better.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment I did not accept an AI suggestion as-is was when it wanted to throw an exception everytime a user were to add an overlapping task. I realized this was not what the system intended as we need it to inform the user that the task was overlapping but not prevent them from adding them. This shows the importance of understanding what your buidling and why so you as the architect can gauge whether or not the suggestion is in line with the overall plan.

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested task completion, task addition, sorting logic, recurring tasks, conflict detection, and schedule generation. All of these tests were important because they verified that the app correctly receives tasks and sorts them based on timing and priority.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I gave my confidence a 4/5 as all 28 of my tests passed but there still may be edge cases I still haven't tried out. If I had more time, I would've played around by stress testing the platform with many tasks and playing around with different timing scenarios.

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

I'm most satisfied with my algorithm. I think it makes alot of sense to use a greedy approach for this project. It works well and ensures that the tasks with high priority are completed first before others.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had more time, I'd make more updates to the UI. While Streamlit is nice for quick applications, I'd redo this app with React to polish the UI/UX more.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

One important thing I learned about designing systems with AI is that AI can scope out systems well as long as you're patient. Instead of giving it one entire feature to implement, starting from the UML foundation diagrams and working up from there is the most ideal way to go to prevent future issues in the code.