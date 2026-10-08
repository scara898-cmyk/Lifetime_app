import streamlit as st
import os

# --- PAGE CONFIGURATION & STATE ---
st.set_page_config(page_title="To-Do List App", page_icon="✅")
st.title("To-Do List App")
st.write("Welcome User")

# Initialize Session State so Streamlit remembers variables across reruns
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "accounts" not in st.session_state:
    # A dictionary to mock user data: {username: password}
    st.session_state.accounts = {"admin": "password123"} 

TASKS_FILE = "tasks.txt"

# --- ACCOUNT MANAGEMENT SECTION ---
if not st.session_state.logged_in:
    st.subheader("🔐 Account Login / Registration")
    
    # Replaced input() with st.radio
    auth_choice = st.radio("Do you have an account?", ["Yes", "No"], horizontal=True)

    if auth_choice == "Yes":
        username_input = st.text_input("Username")
        password_input = st.text_input("Password", type="password")
        
        # Replaced the while-loop/attempts logic with a button click
        if st.button("Log In"):
            if username_input in st.session_state.accounts and st.session_state.accounts[username_input] == password_input:
                st.session_state.logged_in = True
                st.success("Log in Successful! Click again or refresh to view your menu.")
                st.rerun() # Refresh the page to load the app menu
            else:
                st.error("Invalid username or password.")

    else:
        st.write("### Create a New Account")
        new_user = st.text_input("Create username")
        new_pass = st.text_input("Create password", type="password")
        
        if st.button("Register"):
            if new_user in st.session_state.accounts:
                st.error("Username already exists!")
            elif new_user.strip() == "" or new_pass.strip() == "":
                st.warning("Fields cannot be empty.")
            else:
                st.session_state.accounts[new_user] = new_pass
                st.success("Account created successfully! You can now switch to 'Yes' and log in.")

# --- TASKS SECTION (Only displays if logged_in is True) ---
else:
    # Sidebar logout configuration
    st.sidebar.subheader("Account Actions")
    if st.sidebar.button("Log Out"):
        st.session_state.logged_in = False
        st.rerun()

    st.divider()
    st.subheader("📝 Task Manager Menu")
    
    # Replaced terminal text menu + input() with a clean dropdown selectbox
    menu_options = [
        "Add Task", 
        "View Tasks", 
        "Mark Task as Done", 
        "Remove Task", 
        "Others: Specify"
    ]
    user_choice = st.selectbox("Choose an option:", menu_options)

    # Helper function to read tasks safely
    def read_tasks():
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, "r") as file:
                return [line.strip() for line in file.readlines() if line.strip()]
        return []

    # 1. ADD TASK
    if user_choice == "Add Task":
        st.write("### Add a New Task")
        new_task = st.text_input("Enter the task:")
        if st.button("Submit Task"):
            if new_task.strip():
                with open(TASKS_FILE, "a") as file:
                    file.write(new_task + "\n")
                st.success(f"Task '{new_task}' added successfully.")
            else:
                st.warning("Task cannot be empty.")

    # 2. VIEW TASKS
    elif user_choice == "View Tasks":
        st.write("### Your Tasks")
        tasks = read_tasks()
        if tasks:
            for i, task in enumerate(tasks, start=1):
                st.write(f"**{i}.** {task}")
        else:
            st.info("No tasks found.")

    # 3. MARK TASK AS DONE
    elif user_choice == "Mark Task as Done":
        st.write("### Mark Task as Done")
        tasks = read_tasks()
        if tasks:
            task_to_mark = st.selectbox("Select a task:", tasks)
            if st.button("Mark Checked"):
                updated_tasks = []
                for t in tasks:
                    if t == task_to_mark and not t.endswith("(Done)"):
                        updated_tasks.append(f"{t} (Done)\n")
                    else:
                        updated_tasks.append(f"{t}\n")
                with open(TASKS_FILE, "w") as file:
                    file.writelines(updated_tasks)
                st.success("Task marked as done.")
        else:
            st.info("No tasks found.")

    # 4. REMOVE TASK
    elif user_choice == "Remove Task":
        st.write("### Remove a Task")
        tasks = read_tasks()
        if tasks:
            task_to_remove = st.selectbox("Select a task to delete:", tasks)
            if st.button("Delete Task", type="primary"): # Red styled button
                tasks.remove(task_to_remove)
                with open(TASKS_FILE, "w") as file:
                    for t in tasks:
                        file.write(t + "\n")
                st.success("Task removed successfully.")
        else:
            st.info("No tasks found.")

    # 5. OTHERS
    elif user_choice == "Others: Specify":
        st.write("### Advanced Features")
        other_option = st.selectbox("Select a utility feature:", ["Clear All Tasks", "Filter Pending Tasks", "Show Completion Statistics"])
        
        tasks = read_tasks()

        if other_option == "Clear All Tasks":
            if st.button("Confirm Clear All", type="primary"):
                with open(TASKS_FILE, "w") as file:
                    file.write("")
                st.success("All tasks cleared.")

        elif other_option == "Filter Pending Tasks":
            pending_tasks = [task for task in tasks if "(Done)" not in task]
            if pending_tasks:
                st.write("#### Pending Tasks:")
                for i, task in enumerate(pending_tasks, start=1):
                    st.write(f"⏳ {i}. {task}")
            else:
                st.info("No pending tasks found.")

        elif other_option == "Show Completion Statistics":
            total_tasks = len(tasks)
            completed_tasks = sum(1 for task in tasks if "(Done)" in task)
            pending_tasks = total_tasks - completed_tasks
            
            # Displays nicely styled summary metrics widgets
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Tasks", total_tasks)
            col2.metric("Completed Tasks", completed_tasks)
            col3.metric("Pending Tasks", pending_tasks)