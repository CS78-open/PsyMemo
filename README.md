# 🧠 PsyMemo

**PsyMemo** è uno strumento digitale open source progettato per supportare psichiatri e medici specialisti nel migliorare l'aderenza terapeutica dei pazienti.
L'applicazione combina la logica di **Google Calendar** con l'**Intelligenza Artificiale Generativa** per creare promemoria efficaci ed empatici in pochi secondi.

🔗 **[VAI ALL'APP ONLINE](https://psymemo.streamlit.app)**

## 🚀 Funzionalità Principali
* **Link "Magici" per il Calendario:** Genera link che, una volta cliccati dal paziente, configurano automaticamente la sveglia sul calendario (con orario corretto e ricorrenza giornaliera).
* **Messaggi Empatici (AI):** Utilizza Google Gemini per scrivere messaggi di accompagnamento personalizzati (tono empatico, professionale o semplice) da inviare via chat.
* **Integrazione WhatsApp & Email:** Crea pulsanti di invio diretto per trasferire il piano terapeutico senza dover fare copia-incolla manuale.
* **Privacy Totale:** Architettura *stateless*. Nessun dato del paziente (nome farmaco, dosaggio) viene salvato su database.

## 🏛️ Conformità PA
Questo software è sviluppato in conformità con le linee guida AgID per il software a riuso nella Pubblica Amministrazione.
* **Licenza:** EUPL v1.2 (European Union Public License).
* **File AgID:** Il repository include il file `publiccode.yml` per la catalogazione.

## 🛠️ Stack Tecnologico
* **Linguaggio:** Python
* **Interfaccia:** Streamlit
* **AI Model:** Google Gemini 2.5 Flash
* **Integrazioni:** Google Calendar API (via URL generation), WhatsApp API (via URL scheme).

## ⚠️ Disclaimer
L'applicazione è un supporto logistico-motivazionale e non sostituisce la prescrizione medica ufficiale. L'uso dell'Intelligenza Artificiale è finalizzato esclusivamente alla stesura del testo di accompagnamento.

---
*Realizzato da [Marco Pingitore](https://www.marcopingitore.it)*
