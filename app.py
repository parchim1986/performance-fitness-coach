import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

st.set_page_config(page_title="Google Sheets Test", page_icon="🧪")
st.title("🧪 Google Sheets Verbindung testen")

st.markdown("Dieser Test prüft, ob deine App erfolgreich auf die Tabelle **Fitness Leads** zugreifen und schreiben kann.")

# Verbindung herstellen
try:
    scopes = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = Credentials.from_service_account_info(st.secrets["gcp"], scopes=scopes)
    client = gspread.authorize(credentials)

    st.success("✅ Verbindung zu Google Sheets erfolgreich!")

    try:
        sheet = client.open("Fitness Leads").sheet1
        st.success("✅ Tabelle 'Fitness Leads' gefunden!")
        
        now = datetime.now().strftime("%d.%m.%Y %H:%M")
        test_data = ["TEST", "test@example.com", "0000000000", now]

        sheet.append_row(test_data)
        st.success("✅ Testdaten erfolgreich eingetragen!")
        st.write("Eingetragen:", test_data)
    
    except Exception as sheet_error:
        st.error("❌ Tabelle nicht gefunden oder kein Zugriff.")
        st.code(str(sheet_error))

except Exception as e:
    st.error("❌ Verbindung zu Google Sheets fehlgeschlagen.")
    st.code(str(e))