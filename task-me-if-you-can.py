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

# Templates für das Design
TEMPLATES = {
    "Hell": {"background_color": "#f9f9f9"},
    "Dunkel": {"background_color": "#333333", "text_color": "#ffffff"},
    "Pastell": {"background_color": "#e8eaf6"}
}

# Initialisierung Session State
if 'tasks' not in st.session_state:
    st.session_state.tasks = []
if 'template' not in st.session_state:
    st.session_state.template = "Hell"

# Template Auswahl
st.sidebar.title("Design Template")
st.session_state.template = st.sidebar.selectbox("Wähle dein Design:", list(TEMPLATES.keys()))

# Design anwenden
st.markdown(
    f"""
    <style>
        .main {{
            background-color: {TEMPLATES[st.session_state.template]['background_color']};
            color: {TEMPLATES[st.session_state.template].get('text_color', '#000000')};
        }}
    </style>
    """,
    unsafe_allow_html=True
)

# Neue Task hinzufügen
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

# Aufgaben anzeigen & bearbeiten
st.header("📝 Deine Aufgaben")
show_done = st.checkbox("Erledigte Aufgaben anzeigen", value=False)

for i, task in enumerate(st.session_state.tasks):
    if task['done'] and not show_done:
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
            st.session_state.tasks.pop(i)
            st.experimental_rerun()
    with col4:
        task['priority'] = st.selectbox("Priorität", ["Hoch", "Mittel", "Niedrig"], index=["Hoch", "Mittel", "Niedrig"].index(task['priority']), key=f"prio_{i}")

# Fällige Aufgaben mit Erinnerung
st.header("⏰ Erinnerungen")
today = datetime.date.today()
for task in st.session_state.tasks:
    if not task['done'] and task['due_date'] <= today:
        st.warning(f"Aufgabe '{task['title']}' ist fällig oder überfällig!")
