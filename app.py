import streamlit as st
import pawpal_system as ps
from datetime import time

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

# --- Session State Initialization ---
if "owner" not in st.session_state:
    st.session_state.owner = ps.Owner(name="Jordan", available_time_minutes=60)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = ps.Scheduler(owner=st.session_state.owner)

if "current_plan" not in st.session_state:
    st.session_state.current_plan = None

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to **PawPal+** - your intelligent pet care scheduling assistant.

Plan tasks, detect conflicts, and keep your pets happy with smart scheduling.
"""
)

st.divider()

# --- Owner Setup ---
st.subheader("👤 Owner Setup")
col_owner1, col_owner2 = st.columns(2)
with col_owner1:
    owner_name = st.text_input("Owner name", value=st.session_state.owner.name)
with col_owner2:
    available_time = st.number_input(
        "Available time (minutes)", 
        min_value=1, 
        max_value=480, 
        value=st.session_state.owner.available_time_minutes
    )

if owner_name != st.session_state.owner.name:
    st.session_state.owner.name = owner_name
if available_time != st.session_state.owner.available_time_minutes:
    st.session_state.owner.set_available_time(available_time)
    st.session_state.scheduler.available_time = available_time

with st.expander("View Owner Summary"):
    owner_info = st.session_state.owner.get_info()
    st.json(owner_info)

st.divider()

# --- Pet Setup ---
st.subheader("🐕 Pet Setup")
col_pet1, col_pet2 = st.columns(2)
with col_pet1:
    pet_name = st.text_input("Pet name", value="Mochi")
with col_pet2:
    species = st.selectbox("Species", ["dog", "cat", "bird", "rabbit", "other"])

if st.button("Add Pet"):
    existing_names = [p.name for p in st.session_state.owner.pets]
    if pet_name not in existing_names:
        new_pet = ps.Pet(name=pet_name, pet_type=species)
        st.session_state.owner.add_pet(new_pet)
        st.success(f"✅ Added {pet_name} the {species}!")
    else:
        st.warning(f"⚠️ {pet_name} is already added.")

if st.session_state.owner.pets:
    st.write("**Your pets:**")
    pet_info_list = [pet.get_info() for pet in st.session_state.owner.pets]
    st.table(pet_info_list)
else:
    st.info("No pets added yet. Add your first pet above!")

st.divider()

# --- Task Management ---
st.subheader("📋 Task Management")

# Task creation form
with st.expander("➕ Add New Task", expanded=True):
    col1, col2 = st.columns(2)
    with col1:
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority_map = {"🔴 High (1)": 1, "🟡 Medium (3)": 3, "🟢 Low (5)": 5}
        priority_label = st.selectbox("Priority", list(priority_map.keys()), index=0)
        priority = priority_map[priority_label]
    
    with col2:
        pet_names = ["(No pet)"] + [p.name for p in st.session_state.owner.pets]
        selected_pet = st.selectbox("Assign to pet", pet_names)
        
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        preferred_time = st.selectbox("Preferred time", ["morning", "afternoon", "evening"])
        
        # Optional specific start time
        use_start_time = st.checkbox("Set specific start time")
        start_time = None
        if use_start_time:
            start_time_input = st.time_input("Start time", value=time(8, 0))
            start_time = start_time_input

    if st.button("Add Task", type="primary"):
        existing_task_names = [t.name for t in st.session_state.scheduler.get_tasks()]
        if task_title not in existing_task_names:
            new_task = ps.Task(
                name=task_title,
                duration_minutes=int(duration),
                priority=priority,
                frequency=frequency,
                preferred_time=preferred_time,
                start_time=start_time
            )
            
            if selected_pet != "(No pet)":
                for pet in st.session_state.owner.pets:
                    if pet.name == selected_pet:
                        pet.add_task(new_task)
                        break
            
            # Add task with conflict checking
            warning = st.session_state.scheduler.add_task(new_task, check_conflicts=True)
            
            if warning:
                st.warning(warning)
            st.success(f"✅ Added task: {task_title}" + (f" for {selected_pet}" if selected_pet != "(No pet)" else ""))
        else:
            st.error(f"❌ Task '{task_title}' already exists.")

st.divider()

# --- Task Display with Sorting & Filtering ---
st.subheader("📊 View Tasks")

scheduler_tasks = st.session_state.scheduler.get_tasks()

if scheduler_tasks:
    # Sorting and filtering controls
    col_sort, col_filter, col_status = st.columns(3)
    
    with col_sort:
        sort_option = st.selectbox(
            "Sort by",
            ["Priority (High to Low)", "Preferred Time (Chronological)", "Default Order"]
        )
    
    with col_filter:
        pet_filter_options = ["All Pets"] + [p.name for p in st.session_state.owner.pets]
        pet_filter = st.selectbox("Filter by pet", pet_filter_options)
    
    with col_status:
        status_filter = st.selectbox(
            "Filter by status",
            ["All Tasks", "Incomplete Only", "Completed Only"]
        )
    
    # Apply sorting using Scheduler methods
    if sort_option == "Priority (High to Low)":
        display_tasks = st.session_state.scheduler.sort_by_priority()
    elif sort_option == "Preferred Time (Chronological)":
        display_tasks = st.session_state.scheduler.sort_by_time()
    else:
        display_tasks = scheduler_tasks
    
    # Apply pet filter using Scheduler.filter_by_pet()
    if pet_filter != "All Pets":
        display_tasks = [t for t in display_tasks if t.pet_name == pet_filter]
    
    # Apply status filter using Scheduler.filter_by_completion()
    if status_filter == "Incomplete Only":
        incomplete_tasks = st.session_state.scheduler.filter_by_completion(completed=False)
        display_tasks = [t for t in display_tasks if t in incomplete_tasks]
    elif status_filter == "Completed Only":
        completed_tasks = st.session_state.scheduler.filter_by_completion(completed=True)
        display_tasks = [t for t in display_tasks if t in completed_tasks]
    
    # Display task count
    total_count = len(scheduler_tasks)
    filtered_count = len(display_tasks)
    
    if filtered_count == total_count:
        st.info(f"📋 Showing all {total_count} tasks")
    else:
        st.info(f"📋 Showing {filtered_count} of {total_count} tasks (filtered)")
    
    # Build table data with status indicators
    if display_tasks:
        table_data = []
        for task in display_tasks:
            status_icon = "✅" if task.is_completed else "⏳"
            priority_icon = {1: "🔴", 2: "🟠", 3: "🟡", 4: "🟢", 5: "🟢"}
            
            time_display = task.preferred_time
            if task.start_time:
                time_display = f"{task.start_time.strftime('%H:%M')} ({task.preferred_time})"
            
            table_data.append({
                "Status": status_icon,
                "Task": task.name,
                "Duration": f"{task.duration_minutes} min",
                "Priority": f"{priority_icon.get(task.priority, '⚪')} {task.priority}",
                "Pet": task.pet_name or "—",
                "Time": time_display,
                "Frequency": task.frequency
            })
        
        st.table(table_data)
    else:
        st.warning("No tasks match the current filters.")
    
    # --- Conflict Detection ---
    st.divider()
    st.subheader("⚠️ Conflict Detection")
    
    if st.session_state.scheduler.has_conflicts():
        st.error("🚨 Schedule conflicts detected!")
        conflict_report = st.session_state.scheduler.get_conflict_report()
        st.code(conflict_report)
        
        # Detailed conflict info
        conflicts = st.session_state.scheduler.detect_conflicts()
        for task1, task2, conflict_type in conflicts:
            if conflict_type == "same_pet":
                st.warning(f"⚠️ **Same pet conflict**: '{task1.name}' and '{task2.name}' overlap for {task1.pet_name}")
            else:
                st.warning(f"⚠️ **Owner conflict**: '{task1.name}' and '{task2.name}' overlap (can't do both at once)")
    else:
        st.success("✅ No scheduling conflicts detected!")
    
    # --- Task Completion ---
    st.divider()
    st.subheader("✔️ Complete Tasks")
    
    incomplete_tasks = st.session_state.scheduler.filter_by_completion(completed=False)
    if incomplete_tasks:
        task_to_complete = st.selectbox(
            "Select task to mark complete",
            ["(Select a task)"] + [t.name for t in incomplete_tasks]
        )
        
        if st.button("Mark Complete"):
            if task_to_complete != "(Select a task)":
                next_task = st.session_state.scheduler.complete_task(task_to_complete)
                st.success(f"✅ Marked '{task_to_complete}' as complete!")
                
                if next_task:
                    st.info(f"🔄 Recurring task: Next occurrence created for {next_task.due_date}")
                
                st.rerun()
    else:
        st.success("🎉 All tasks completed!")

else:
    st.info("No tasks yet. Add your first task above!")

st.divider()

# --- Generate Schedule ---
st.subheader("📅 Build Schedule")
st.caption(f"Available time: **{st.session_state.owner.available_time_minutes} minutes**")

# Show quick stats
incomplete_count = len(st.session_state.scheduler.filter_by_completion(completed=False))
total_duration = sum(t.duration_minutes for t in st.session_state.scheduler.filter_by_completion(completed=False))

col_stat1, col_stat2, col_stat3 = st.columns(3)
with col_stat1:
    st.metric("Incomplete Tasks", incomplete_count)
with col_stat2:
    st.metric("Total Duration", f"{total_duration} min")
with col_stat3:
    time_status = "✅ Fits" if total_duration <= st.session_state.owner.available_time_minutes else "⚠️ Over"
    st.metric("Time Status", time_status)

if st.button("Generate Schedule", type="primary"):
    if not st.session_state.scheduler.get_tasks():
        st.warning("⚠️ Add some tasks first before generating a schedule.")
    else:
        st.session_state.current_plan = st.session_state.scheduler.generate_plan()
        st.success("✅ Schedule generated!")

# Display the current plan
if st.session_state.current_plan:
    plan = st.session_state.current_plan
    st.markdown("### 📋 Your Daily Plan")
    
    # Summary metrics
    col_plan1, col_plan2, col_plan3 = st.columns(3)
    with col_plan1:
        st.metric("Scheduled", f"{len(plan.scheduled_tasks)} tasks")
    with col_plan2:
        st.metric("Total Time", f"{plan.total_duration} min")
    with col_plan3:
        if plan.unscheduled_tasks:
            st.metric("Unscheduled", f"{len(plan.unscheduled_tasks)} tasks", delta="-", delta_color="inverse")
        else:
            st.metric("Unscheduled", "0 tasks")
    
    # Scheduled tasks table
    if plan.scheduled_tasks:
        st.markdown("#### ✅ Scheduled Tasks")
        scheduled_data = []
        for i, task in enumerate(plan.scheduled_tasks, 1):
            scheduled_data.append({
                "#": i,
                "Task": task.name,
                "Duration": f"{task.duration_minutes} min",
                "Priority": task.priority,
                "Pet": task.pet_name or "—"
            })
        st.table(scheduled_data)
    
    # Unscheduled tasks warning
    if plan.unscheduled_tasks:
        st.markdown("#### ⚠️ Could Not Schedule")
        st.warning(f"{len(plan.unscheduled_tasks)} task(s) didn't fit in available time:")
        unscheduled_data = []
        for task in plan.unscheduled_tasks:
            unscheduled_data.append({
                "Task": task.name,
                "Duration": f"{task.duration_minutes} min",
                "Priority": task.priority,
                "Reason": "Not enough time"
            })
        st.table(unscheduled_data)
    
    # Reasoning expander
    with st.expander("🧠 View Scheduling Reasoning"):
        st.text(plan.explain_reasoning())

st.divider()
st.caption("🐾 PawPal+ - Smart Pet Care Scheduling")
