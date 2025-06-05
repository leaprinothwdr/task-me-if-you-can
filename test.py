import streamlit as st
import pandas as pd
import datetime
import random

# Beispielhafte motivierende Sprüche
MOTIVATION_QUOTES = [
    "Du schaffst das! 💪",
    "Bleib dran – es lohnt sich! ✨",
    "Jeder Schritt bringt dich näher ans Ziel! 🛤️",
    "Fokus und Ausdauer bringen dich weiter! 🧠",
    "Mach weiter, du bist auf dem richtigen Weg! 🏁"
]

# Initialisierung Session State
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'deleted_tasks' not in st.session_state:
    st.session_state.deleted_tasks = []

# Seitenwahl
st.sidebar.title("📚 Navigation")
page = st.sidebar.radio("Wähle eine Seite:", ["Aktive Aufgaben", "Erledigte Aufgaben", "Gelöschte Aufgaben", "Kalender"])

# Seite: Aktive Aufgaben
if page == "Aktive Aufgaben":
    st.title("🎓 Studenten Task Manager")
    st.subheader(random.choice(MOTIVATION_QUOTES))

    with st.form("new_task_form"):
        title = st.text_input("Neue Aufgabe")
        due_date = st.date_input("Fälligkeitsdatum", datetime.date.today())
        priority = st.selectbox("Priorität", ["Hoch", "Mittel", "Niedrig"])
        shared_with = st.text_input("Teile mit (Name oder E-Mail optional)")
        progress = st.slider("Fortschritt (%)", 0, 100, 0)
        submitted = st.form_submit_button("Aufgabe hinzufügen")

        if submitted and title:
            st.session_state.tasks.append({
                "title": title,
                "due_date": due_date,
                "priority": priority,
                "shared_with": shared_with,
                "done": False,
                "progress": progress
            })

    st.header("📝 Deine Aufgaben")

    updated_tasks = []
    for i, task in enumerate(st.session_state.tasks):
        if task['done']:
            updated_tasks.append(task)
            continue

        col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
        with col1:
            new_title = st.text_input(f"{i}_title", task['title'])
            task['title'] = new_title
            st.progress(task['progress'])
            task['progress'] = st.slider(f"{i}_progress", 0, 100, task['progress'])
        with col2:
            task['done'] = st.checkbox("Erledigt", value=task['done'], key=f"done_{i}")
        with col3:
            if st.button("Löschen", key=f"delete_{i}"):
                st.session_state.deleted_tasks.append(task)
                continue  # Aufgabe wird nicht zu updated_tasks hinzugefügt
        with col4:
            task['priority'] = st.selectbox("Priorität", ["Hoch", "Mittel", "Niedrig"], index=["Hoch", "Mittel", "Niedrig"].index(task['priority']), key=f"prio_{i}")

        updated_tasks.append(task)

    st.session_state.tasks = updated_tasks

    # Fällige Aufgaben mit Erinnerung
    st.header("⏰ Erinnerungen")
    today = datetime.date.today()
    for task in st.session_state.tasks:
        if not task['done'] and task['due_date'] <= today:
            st.warning(f"Aufgabe '{task['title']}' ist fällig oder überfällig!")

# Seite: Erledigte Aufgaben
elif page == "Erledigte Aufgaben":
    st.title("✅ Erledigte Aufgaben")

    erledigte_tasks = [task for task in st.session_state.tasks if task['done']]

    if not erledigte_tasks:
        st.info("Noch keine erledigten Aufgaben vorhanden.")
    else:
        for i, task in enumerate(erledigte_tasks):
            st.markdown(f"**{task['title']}** – Priorität: {task['priority']} – Fällig am: {task['due_date']}")
            st.progress(task['progress'])

# Seite: Gelöschte Aufgaben
elif page == "Gelöschte Aufgaben":
    st.title("🗑️ Gelöschte Aufgaben")

    if not st.session_state.deleted_tasks:
        st.info("Keine Aufgaben wurden gelöscht.")
    else:
        for task in st.session_state.deleted_tasks:
            st.markdown(f"❌ **{task['title']}** – Priorität: {task['priority']} – Fällig am: {task['due_date']}")
            st.progress(task['progress'])

# Seite: Kalender
elif page == "Kalender":
    st.title("📅 Aufgaben-Kalender")

    if not st.session_state.tasks:
        st.info("Keine Aufgaben vorhanden.")
    else:
        calendar_data = pd.DataFrame([
            {
                "Aufgabe": task['title'],
                "Fälligkeitsdatum": pd.to_datetime(task['due_date']),
                "Status": "✅" if task['done'] else "🕒",
                "Priorität": task['priority']
            }
            for task in st.session_state.tasks
        ]).sort_values("Fälligkeitsdatum")

        st.dataframe(calendar_data, use_container_width=True)
