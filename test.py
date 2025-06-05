import streamlit as st
import pandas as pd
import datetime
import random

st.set_page_config(page_title="TaskMeIfYouCan", layout="wide")
st.markdown("""
    <style>
        html, body, [class*="css"]  {
            font-family: 'Helvetica Neue', sans-serif;
        }
        .block-container {
            padding: 2rem 4rem;
        }
        .stProgress > div > div > div > div {
            background-color: #007aff;
            height: 20px;
            border-radius: 10px;
        }
        .stSlider > div[data-baseweb="slider"] > div {
            padding: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# Motivierende Sprüche
MOTIVATION_QUOTES = [
    "Tu’s jetzt, sonst kommt der Lern-Goblin um Mitternacht. 🧌",
    "Erinnerst du dich an Motivation? Nein? Dann fang an! 🫵",
    "Diese Aufgabe erledigt sich nicht durch Scrollen. 📱✖️",
    "Du hast mehr Zeit als Ausreden. Los jetzt. 😠",
    "Wenn du’s nicht machst, mach ich’s... aber schlecht. 🧟‍♂️",
    "Deadline? Klingt wie dein Schicksal. 🔪",
    "Du bist nicht zu müde. Dein innerer Schweinehund hat nur WLAN. 🐷📶",
    "Jeder Klick auf ‚Später‘ löscht ein Hirnzellchen. 🧠🔥",
    "Mach jetzt. Oder Duolingo schickt dir eine Eule in den Schlaf. 🦉",
    "Entweder du erledigst die Aufgabe – oder sie erledigt dich. ☠️"
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
    st.title("🎓 Task Manager – Für smarte Studis")
    st.markdown(f"<h4 style='color:#888;'>{random.choice(MOTIVATION_QUOTES)}</h4>", unsafe_allow_html=True)

    with st.form("new_task_form"):
        st.markdown("### Neue Aufgabe hinzufügen")
        col1, col2 = st.columns(2)
        with col1:
            title = st.text_input("Titel der Aufgabe")
            priority = st.selectbox("Priorität", ["Hoch", "Mittel", "Niedrig"])
        with col2:
            due_date = st.date_input("Fälligkeitsdatum", datetime.date.today())
            shared_with = st.text_input("Teilen mit (optional)")

        progress = st.slider("Fortschritt (%)", 0, 100, 0)
        submitted = st.form_submit_button("➕ Aufgabe hinzufügen")

        if submitted and title:
            st.session_state.tasks.append({
                "title": title,
                "due_date": due_date,
                "priority": priority,
                "shared_with": shared_with,
                "done": False,
                "progress": progress
            })

    st.markdown("## 📌 Deine Aufgaben")

    updated_tasks = []
    for i, task in enumerate(st.session_state.tasks):
        if task['done']:
            updated_tasks.append(task)
            continue

        with st.container():
            col1, col2, col3, col4 = st.columns([5, 1, 1, 1])
            with col1:
                task['title'] = st.text_input(f"{i}_title", task['title'])
                st.markdown(f"**Fälligkeit:** {task['due_date']}  |  **Priorität:** {task['priority']}")
                st.progress(task['progress'])
                task['progress'] = st.slider(f"{i}_progress", 0, 100, task['progress'])
            with col2:
                task['done'] = st.checkbox("Erledigt", value=task['done'], key=f"done_{i}")
            with col3:
                if st.button("🗑️", key=f"delete_{i}"):
                    st.session_state.deleted_tasks.append(task)
                    continue
            with col4:
                task['priority'] = st.selectbox("Priorität", ["Hoch", "Mittel", "Niedrig"],
                    index=["Hoch", "Mittel", "Niedrig"].index(task['priority']), key=f"prio_{i}")

        updated_tasks.append(task)

    st.session_state.tasks = updated_tasks

    st.markdown("---")
    st.markdown("## ⏰ Erinnerungen")
    today = datetime.date.today()
    for task in st.session_state.tasks:
        if not task['done'] and task['due_date'] <= today:
            st.warning(f"⚠️ Aufgabe '{task['title']}' ist fällig oder überfällig!")

# Seite: Erledigte Aufgaben
elif page == "Erledigte Aufgaben":
    st.title("✅ Erledigte Aufgaben")
    erledigte_tasks = [task for task in st.session_state.tasks if task['done']]

    if not erledigte_tasks:
        st.info("Noch keine erledigten Aufgaben vorhanden.")
    else:
        for task in erledigte_tasks:
            with st.container():
                st.markdown(f"**{task['title']}** – 🗓️ {task['due_date']}  |  🔥 Priorität: {task['priority']}")
                st.progress(task['progress'])

# Seite: Gelöschte Aufgaben
elif page == "Gelöschte Aufgaben":
    st.title("🗑️ Gelöschte Aufgaben")

    if not st.session_state.deleted_tasks:
        st.info("Keine Aufgaben wurden gelöscht.")
    else:
        for task in st.session_state.deleted_tasks:
            with st.container():
                st.markdown(f"❌ **{task['title']}** – 📅 {task['due_date']}  |  📌 {task['priority']}")
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

st.markdown(
    """
<style>
/* Hintergrund dunkel */
body, .stApp {
    background-color: #98F5FF;
    color: #98F5FF;
    /* FUNKTIONIERT */
}

/* Schrift anpassen */
html, body, [class^="css"] {
    font-family: 'Helvetica';
    font-size: 16px;
    color: #f5f5f5;
    /* FUNKTIONIERT */
}

/* Inputfelder größer und heller */
input, textarea, select {
    font-size: 1.2rem !important;
    background-color: #2a2a2a !important;
    color: #ffffff !important;
    border: 1px solid #555 !important;
    border-radius: 8px !important;
}

/* Buttons anpassen */
button[kind="primary"] {
    background-color: #4CAF50 !important;
    color: white !important;
    border: none !important;
}

/* Fortschrittsbalken */
div[data-testid="stProgress"] > div > div > div {
    background-color: #4CAF50 !important;
}

/* Sektionen und Karten */
[data-testid="stVerticalBlock"] {
    background-color: #2b2b2b;
    padding: 1rem;
    border-radius: 10px;
    margin-bottom: 1rem;
}

/* Zentrierung (optional) */
h1, h2, h3 {
    color: #ffffff;
}
</style>
""", 
unsafe_allow_html=True,
)
