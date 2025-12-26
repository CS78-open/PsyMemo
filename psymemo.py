import streamlit as st
import google.generativeai as genai
import urllib.parse
import os
from datetime import datetime, timedelta, time

# Configurazione Pagina
st.set_page_config(page_title="PsyMemo", page_icon="🧠", layout="centered")

# --- SIDEBAR (LOGO E INFO) ---
st.sidebar.title("🧠 PsyMemo")

# Controllo Logo (se carichi il file logo.png, appare qui)
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)
else:
    st.sidebar.write("") # Spazio vuoto se non c'è logo

st.sidebar.info("Generatore di aderenza terapeutica v2.2")
st.sidebar.markdown("---")
api_key = st.sidebar.text_input("Inserisci Google API Key", type="password")

# --- INTERFACCIA PRINCIPALE ---
st.title("Nuova Prescrizione Smart")
st.markdown("Crea promemoria efficaci per i tuoi pazienti in pochi click.")

col1, col2 = st.columns(2)

with col1:
    farmaco = st.text_input("Nome Farmaco", placeholder="es. Sertralina")
    dosaggio = st.text_input("Dosaggio/Istruzioni", placeholder="es. 50mg dopo colazione")

with col2:
    # Orario fisso alle 09:00 per evitare reset
    orario = st.time_input("Orario assunzione", value=time(9, 0))
    tono = st.selectbox("Tono del messaggio", ["Empatico e Caldo", "Professionale e Diretto", "Semplice e Breve"])

# --- LOGICA DEL GENERATORE ---
if st.button("✨ Genera Strumenti"):
    if not api_key:
        st.error("⚠️ Inserisci la API Key nella barra laterale.")
    elif not farmaco:
        st.warning("⚠️ Inserisci almeno il nome del farmaco.")
    else:
        try:
            # 1. CALCOLO DATA E ORA (Calendar)
            data_oggi = datetime.now().date()
            start_dt = datetime.combine(data_oggi, orario)
            end_dt = start_dt + timedelta(minutes=30)
            
            fmt = "%Y%m%dT%H%M%S"
            dates_str = f"{start_dt.strftime(fmt)}/{end_dt.strftime(fmt)}"
            
            titulo_evento = f"Terapia: {farmaco}"
            dettagli_evento = f"Dosaggio: {dosaggio}. Ricorda la costanza."
            
            params = {
                "text": titulo_evento,
                "details": dettagli_evento,
                "dates": dates_str,
                "recur": "RRULE:FREQ=DAILY"
            }
            link_calendar = f"https://calendar.google.com/calendar/render?action=TEMPLATE&{urllib.parse.urlencode(params)}"

            # 2. IA GENERATIVA (Messaggio)
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            
            prompt = f"""
            Scrivi un messaggio breve per un paziente (massimo 3 righe) per WhatsApp.
            Paziente deve prendere: {farmaco}, dosaggio: {dosaggio}.
            Tono: {tono}.
            Obiettivo: Motivare alla costanza. Niente saluti formali iniziali.
            """
            
            with st.spinner('L\'AI sta scrivendo...'):
                response = model.generate_content(prompt)
                messaggio_ai = response.text.strip()
            
            # 3. LINK WHATSAPP E EMAIL
            testo_completo = f"{messaggio_ai}\n\n📅 Clicca qui per salvare il promemoria:\n{link_calendar}"
            testo_encoded = urllib.parse.quote(testo_completo)
            link_whatsapp = f"https://wa.me/?text={testo_encoded}"
            link_email = f"mailto:?subject=La tua terapia ({farmaco})&body={testo_encoded}"

            # --- OUTPUT ---
            st.success("✅ Generato con successo!")
            st.text_area("Anteprima Messaggio:", value=testo_completo, height=180)
            
            c1, c2, c3 = st.columns(3)
            with c1: st.link_button("📱 WhatsApp", link_whatsapp)
            with c2: st.link_button("📧 Email", link_email)
            with c3: st.link_button("📅 Calendario", link_calendar)
                
        except Exception as e:
            st.error(f"Errore: {e}")

# --- FOOTER & CREDITS ---
st.divider()
st.markdown(
    """
    <div style='text-align: center; color: grey; font-size: 0.8em;'>
        App realizzata da <b><a href='https://www.marcopingitore.it' target='_blank' style='text-decoration: none; color: inherit;'>Marco Pingitore</a></b><br>
        Rilasciato sotto licenza <b>EUPL v1.2</b> (European Union Public License).<br>
        Software conforme per il riuso nella Pubblica Amministrazione.
    </div>
    """, 
    unsafe_allow_html=True
)