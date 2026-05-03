import streamlit as st
import pandas as pd
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Personal Hub", layout="wide")

# Initialize Data in Session State (This stays active as long as the tab is open)
if 'finance_data' not in st.session_state:
    st.session_state.finance_data = pd.DataFrame(columns=["Date", "Type", "Category", "Amount"])

if 'todo_list' not in st.session_state:
    st.session_state.todo_list = []

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Finance Tracker", "To-Do List"])

# --- PAGE 1: FINANCE TRACKER ---
if page == "Finance Tracker":
    st.title("💰 Finance Tracker")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Add Transaction")
        t_type = st.selectbox("Type", ["Expense", "Income"])
        t_cat = st.text_input("Category (e.g., Food, Salary, Rent)")
        t_amt = st.number_input("Amount", min_value=0.0, step=10.0)
        t_date = st.date_input("Date", datetime.now())

        if st.button("Add Record"):
            new_data = pd.DataFrame([[t_date, t_type, t_cat, t_amt]],
                                    columns=["Date", "Type", "Category", "Amount"])
            st.session_state.finance_data = pd.concat([st.session_state.finance_data, new_data], ignore_index=True)
            st.success("Record Added!")

    with col2:
        st.subheader("Summary")
        df = st.session_state.finance_data

        if not df.empty:
            income = df[df['Type'] == 'Income']['Amount'].sum()
            expense = df[df['Type'] == 'Expense']['Amount'].sum()
            balance = income - expense

            m1, m2, m3 = st.columns(3)
            m1.metric("Total Income", f"₹{income}")
            m2.metric("Total Expense", f"₹{expense}")
            m3.metric("Net Balance", f"₹{balance}")

            st.dataframe(df, use_container_width=True)

            # Simple Chart
            if expense > 0:
                st.write("Expense Breakdown")
                st.bar_chart(df[df['Type'] == 'Expense'].set_index('Category')['Amount'])
        else:
            st.info("No data recorded yet.")

# --- PAGE 2: TO-DO LIST ---
elif page == "To-Do List":
    st.title("✅ Task Manager")

    # Add Task
    new_task = st.text_input("Add a new task:", placeholder="e.g., Pay electricity bill...")
    if st.button("Add Task") and new_task:
        st.session_state.todo_list.append({"task": new_task, "done": False})

    st.write("---")

    # Display Tasks
    if not st.session_state.todo_list:
        st.info("Your to-do list is empty!")
    else:
        for i, task_item in enumerate(st.session_state.todo_list):
            cols = st.columns([0.1, 0.9])
            # Checkbox to mark as done
            is_done = cols[0].checkbox("", value=task_item["done"], key=f"check_{i}")
            st.session_state.todo_list[i]["done"] = is_done

            # Strike through text if done
            if is_done:
                cols[1].write(f"~~{task_item['task']}~~")
            else:
                cols[1].write(task_item["task"])

    if st.button("Clear Completed Tasks"):
        st.session_state.todo_list = [t for t in st.session_state.todo_list if not t["done"]]
        st.rerun()
