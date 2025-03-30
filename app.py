
import streamlit as st
import openai

st.set_page_config(page_title="Performance Fitness Coach", page_icon=":muscle:")
st.title("Performance Fitness – Dein AI-Fitness-Coach für Anfänger")

# Dein fester OpenAI API Key
client = openai.OpenAI(api_key="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")

ziel = st.selectbox("Was ist dein Ziel?", ["Muskelaufbau", "Abnehmen", "Fit bleiben", "Reha"])
frage = st.text_area("Stell deinem Coach eine Frage:", "Ich bin Anfänger und will zu Hause Muskeln aufbauen. Was soll ich tun?")

if st.button("Coach fragen"):
    with st.spinner("Der Coach überlegt..."):
        system_prompt = f"Du bist ein motivierender Fitness-Coach. Dein Ziel ist es, Anfängern beim Thema '{ziel}' einfache Tipps und Trainingspläne zu geben. Du sprichst locker und motivierend – wie ein echter Trainer im Studio."

        chat = client.chat.completions.create(
    model="gpt-3.5-turbo",  # <-- Ändere das hier!
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": frage}
    ]
)


        antwort = chat.choices[0].message.content
        st.success("Antwort vom Coach:")
        st.write(antwort)
