
import streamlit as st
import openai
import gspread
from datetime import datetime
from google.oauth2 import service_account

st.set_page_config(page_title="Performance Fitness Coach", page_icon=":muscle:")
st.title("Performance Fitness – Dein AI-Fitness-Coach für Anfänger")

# Session State vorbereiten
if "antwort" not in st.session_state:
    st.session_state["antwort"] = ""

# Zugriff auf OpenAI API Key
openai_api_key = st.secrets["openai"]["api_key"]
client = openai.OpenAI(api_key=openai_api_key)

ziel = st.selectbox("Was ist dein Ziel?", ["Muskelaufbau", "Abnehmen", "Fit bleiben", "Reha"])
frage = st.text_area("Stell deinem Coach eine Frage:", "Ich bin Anfänger und will zu Hause Muskeln aufbauen. Was soll ich tun?")

if st.button("Coach fragen"):
    with st.spinner("Der Coach überlegt..."):
        system_prompt = f"Du bist ein motivierender Fitness-Coach. Dein Ziel ist es, Anfängern beim Thema '{ziel}' einfache Tipps und Trainingspläne zu geben. Du sprichst locker und motivierend – wie ein echter Trainer im Studio."
        chat = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": frage}
            ]
        )
        st.session_state["antwort"] = chat.choices[0].message.content

# Coach-Antwort anzeigen, wenn vorhanden
if st.session_state["antwort"]:
    st.success("Antwort vom Coach:")
    st.write(st.session_state["antwort"])

    st.markdown("---")
    st.header("📩 Willst du deinen persönlichen Plan per E-Mail?")

    # Leadformular
    name = st.text_input("Dein Name")
    email = st.text_input("Deine E-Mail")
    phone = st.text_input("Deine Telefonnummer")
    consent = st.checkbox("Ich bin einverstanden, dass meine Daten zur Kontaktaufnahme verwendet werden.")

    if st.button("Absenden") and name and email and phone and consent:
        try:
            creds_dict = st.secrets["gcp"]
            credentials = service_account.Credentials.from_service_account_info(creds_dict)
            client = gspread.Client(auth=credentials)
            client.session = gspread.httpsession.HTTPSession(credentials)
            sheet = client.open("Fitness Leads").sheet1
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M")
            sheet.append_row([name, email, phone, timestamp])
            st.success("✅ Danke! Wir melden uns bald bei dir.")
        except Exception as e:
            st.error(f"Fehler beim Speichern: {e}")

    st.markdown("Deine Daten werden vertraulich behandelt und nicht an Dritte weitergegeben.")
