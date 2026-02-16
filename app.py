import streamlit as st
import pawpal_system as ps

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session State Initialization ---
# Initialize Owner if not already in session
if "owner" not in st.session_state:
    st.session_state.owner = ps.Owner(name="Jordan", available_time_minutes=60)

# Initialize Scheduler tied to the Owner
if "scheduler" not in st.session_state:
    st.session_state.scheduler = ps.Scheduler(owner=st.session_state.owner)

# Initialize current plan as None
if "current_plan" not in st.session_state:
    st.session_state.current_plan = None

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

# --- Owner Setup ---
st.subheader("Owner Setup")
owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
available_time = st.number_input(
    "Available time (minutes)", 
    min_value=1, 
    max_value=480, 
    value=st.session_state.owner.available_time_minutes
)

# Update owner if values changed
if owner_name != st.session_state.owner.name:
    st.session_state.owner.name = owner_name
if available_time != st.session_state.owner.available_time_minutes:
    # Use Owner.set_available_time() method
    st.session_state.owner.set_available_time(available_time)
    st.session_state.scheduler.available_time = available_time

# Display owner summary using Owner.get_info()
with st.expander("View Owner Summary"):
    owner_info = st.session_state.owner.get_info()
    st.json(owner_info)

st.divider()

# --- Pet Setup ---
st.subheader("Pet Setup")
col_pet1, col_pet2 = st.columns(2)
with col_pet1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_pet2:
    species = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet"):
    # Check if pet already exists by name
    existing_names = [p.name for p in st.session_state.owner.pets]
    if pet_name not in existing_names:
        # Create Pet using the Pet class constructor
        new_pet = ps.Pet(name=pet_name, pet_type=species)
        # Use Owner.add_pet() method to add the pet
        st.session_state.owner.add_pet(new_pet)
        st.success(f"Added {pet_name} the {species}!")
    else:
        st.warning(f"{pet_name} is already added.")

# Display current pets using Pet.get_info()
if st.session_state.owner.pets:
    st.write("**Your pets:**")
    pet_info_list = [pet.get_info() for pet in st.session_state.owner.pets]
    st.table(pet_info_list)
else:
    st.info("No pets added yet.")

st.divider()

# --- Task Management ---
st.subheader("Tasks")
st.caption("Add tasks to the scheduler.")

col1, col2, col3, col4 = st.columns(4)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    # Priority: 1=highest, 5=lowest in the system
    priority_map = {"high": 1, "medium": 3, "low": 5}
    priority_label = st.selectbox("Priority", ["high", "medium", "low"], index=0)
    priority = priority_map[priority_label]
with col4:
    # Allow assigning task to a specific pet
    pet_names = ["(No pet)"] + [p.name for p in st.session_state.owner.pets]
    selected_pet = st.selectbox("For pet", pet_names)

if st.button("Add Task"):
    # Check if task with same name already exists using Scheduler.get_tasks()
    existing_task_names = [t.name for t in st.session_state.scheduler.get_tasks()]
    if task_title not in existing_task_names:
        # Create Task using the Task class constructor
        new_task = ps.Task(name=task_title, duration_minutes=int(duration), priority=priority)
        
        # If a pet is selected, use Pet.add_task() to link task to pet
        if selected_pet != "(No pet)":
            for pet in st.session_state.owner.pets:
                if pet.name == selected_pet:
                    pet.add_task(new_task)  # Links task to pet (sets pet_name)
                    break
        
        # Use Scheduler.add_task() to add task to the scheduler
        st.session_state.scheduler.add_task(new_task)
        st.success(f"Added task: {task_title}" + (f" for {selected_pet}" if selected_pet != "(No pet)" else ""))
    else:
        st.warning(f"Task '{task_title}' already exists.")

# Display current tasks using Task.get_info()
scheduler_tasks = st.session_state.scheduler.get_tasks()
if scheduler_tasks:
    st.write("**Current tasks in scheduler:**")
    task_data = [task.get_info() for task in scheduler_tasks]
    st.table(task_data)
else:
    st.info("No tasks yet. Add one above.")

st.divider()

# --- Generate Schedule ---
st.subheader("Build Schedule")
st.caption(f"Available time: {st.session_state.owner.available_time_minutes} minutes")

if st.button("Generate Schedule"):
    if not st.session_state.scheduler.get_tasks():
        st.warning("Add some tasks first before generating a schedule.")
    else:
        # Generate the plan using the Scheduler
        st.session_state.current_plan = st.session_state.scheduler.generate_plan()
        st.success("Schedule generated!")

# Display the current plan if it exists
if st.session_state.current_plan:
    plan = st.session_state.current_plan
    st.markdown("### Your Daily Plan")
    
    # Use DailyPlan.get_summary() for quick overview
    st.info(plan.get_summary())
    
    # Use DailyPlan.display() for full formatted output
    st.text(plan.display())
    
    # Use DailyPlan.explain_reasoning() to show the scheduler's logic
    with st.expander("View Reasoning"):
        st.text(plan.explain_reasoning())
