import streamlit as st
import google.generativeai as genai
import urllib.parse
from datetime import datetime, timedelta, time  # <--- NOTA: Ho aggiunto "time" qui

# Configurazione Pagina
st.set_page_config(page_title="PsyMemo", page_icon="🧠", layout="centered")

# --- SIDEBAR ---
st.sidebar.title("🧠 PsyMemo")
st.sidebar.info("Generatore di aderenza terapeutica v2.1")
api_key = st.sidebar.text_input("Inserisci Google API Key", type="password")

# --- INTERFACCIA PRINCIPALE ---
st.title("Nuova Prescrizione Smart")

col1, col2 = st.columns(2)

with col1:
    farmaco = st.text_input("Nome Farmaco", placeholder="es. Xanax")
    dosaggio = st.text_input("Dosaggio/Istruzioni", placeholder="es. 10 gocce dopo i pasti")

with col2:
    # ORA FISSA (09:00) PER EVITARE IL RESET
    orario = st.time_input("Orario assunzione", value=time(9, 0)) 
    tono = st.selectbox("Tono del messaggio", ["Empatico e Caldo", "Professionale e Diretto", "Semplice e Breve"])

# --- LOGICA DEL GENERATORE ---
if st.button("✨ Genera Tutto"):
    if not api_key:
        st.error("⚠️ Inserisci la API Key nella barra laterale.")
    elif not farmaco:
        st.warning("⚠️ Inserisci almeno il nome del farmaco.")
    else:
        # 1. CREAZIONE DEL LINK CALENDAR (Metodo Corretto)
        try:
            # Prendiamo la data di oggi e l'orario scelto dall'utente
            data_oggi = datetime.now().date()
            
            # Combiniamo data e orario in un oggetto unico
            start_dt = datetime.combine(data_oggi, orario)
            # Facciamo durare l'evento 30 minuti
            end_dt = start_dt + timedelta(minutes=30)
            
            # Formattiamo per Google Calendar (YYYYMMDDTHHMMSS)
            fmt = "%Y%m%dT%H%M%S"
            dates_str = f"{start_dt.strftime(fmt)}/{end_dt.strftime(fmt)}"
            
            titulo_evento = f"Terapia: {farmaco}"
            dettagli_evento = f"Dosaggio: {dosaggio}. Ricorda la costanza."
            
            # Parametri URL
            params = {
                "text": titulo_evento,
                "details": dettagli_evento,
                "dates": dates_str,
                "recur": "RRULE:FREQ=DAILY" # Ripeti ogni giorno
            }
            # Creiamo il link sicuro
            link_calendar = f"https://calendar.google.com/calendar/render?action=TEMPLATE&{urllib.parse.urlencode(params)}"

            # 2. CREAZIONE DEL MESSAGGIO (AI con Gemini)
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
            
            # 3. CREAZIONE LINK WHATSAPP E EMAIL
            testo_completo = f"{messaggio_ai}\n\n📅 Clicca qui per salvare il promemoria:\n{link_calendar}"
            
            # Codifichiamo il testo per i link (gli spazi diventano %20 ecc.)
            testo_encoded = urllib.parse.quote(testo_completo)
            link_whatsapp = f"https://wa.me/?text={testo_encoded}"
            link_email = f"mailto:?subject=La tua terapia ({farmaco})&body={testo_encoded}"

            # --- OUTPUT A VIDEO ---
            st.success("✅ Generato con successo!")
            
            # Mostriamo il messaggio in un box
            st.text_area("Anteprima Messaggio:", value=testo_completo, height=200)
            
            # I Tre Bottoni d'Azione
            c1, c2, c3 = st.columns(3)
            with c1:
                st.link_button("📱 Invia su WhatsApp", link_whatsapp)
            with c2:
                st.link_button("📧 Invia per Email", link_email)
            with c3:
                st.link_button("📅 Prova il Calendario", link_calendar)
                
        except Exception as e:
            st.error(f"Qualcosa è andato storto: {e}")