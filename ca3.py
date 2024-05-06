import streamlit as st
import time
import re
import logging
import logging.handlers

def setup_papertrail_logging():
    papertrail_handler = logging.handlers.SysLogHandler(address=('logs4.papertrailapp.com', 43181))
    formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', datefmt='%b %d %H:%M:%S')
    papertrail_handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    logger.addHandler(papertrail_handler)
    return logger

logger = setup_papertrail_logging()

st.sidebar.header("Hinweis zu den Stichwörtern:")
st.sidebar.markdown("""
1. Maßnahme
2. Salz
3. Ernährung
4. Training
5. Feierabend
6. Abschluss
""")

st.sidebar.header("Hinweis zum Format:")
st.sidebar.markdown("""
Stichwörter: Text.

Zum Beispiel:
- **Präventive Maßnahmen diskutieren**: Ich leide in meiner Familie an Bluthochdruck und hätte gerne Ratschläge zur Vorbeugung.
""", unsafe_allow_html=True)

st.sidebar.header("Persona: Jim")
st.sidebar.markdown("""
- Alter: 30 Jahre
- Beruf: Büroangestellter
- Gesundheitszustand: Familiäre Vorgeschichte von Bluthochdruck
- Ernährungsgewohnheiten:
    - Mag keine zu salzigen Speisen
    - Isst ungern Gemüse und Obst
    - Liebt Fleisch
- Aktivitätslevel:
    - Geht am Wochenende bei gutem Wetter spazieren
    - Fühlt sich oft nach der Arbeit angestrengt
""")



keyword_to_response = {
    'maßnahme:|maßnahme': "Verstanden. Wenn man eine familiäre Vorgeschichte hat, steigt das Risiko, an Bluthochdruck zu erkranken. Sie erkennen, das ist ein wichtiger Punkt. Um Ihnen weitere Vorschläge machen zu können, benötige ich genauere Informationen über Ihre Lebensgewohnheiten. Wie ernähren Sie sich? Wie viel Salz nehmen Sie beispielweise täglich zu sich?",
    "salz:|salz": "Verstehe. Es scheint, dass Sie gut in dieser Angelegenheit handeln. Eine salzarme Ernährung verhindert die Bindung von überschüssigem Wasser im Körper, stabilisiert den Blutdruck und schützt so Herz und Organe. Sie müssen Ihre tägliche Salzaufnahme auf maximal 5 Gramm beschränken, was etwa einem Teelöffel entspricht. Außerdem erklären Sie uns bitte, wie das Verhältnis von Obst, Gemüse und Fetten in Ihrer täglichen Ernährung ist.",
    "ernährung:|ernährung": "Ich verstehe. Eine ausgewogene Ernährung kann dazu beitragen, Blutdruck vorzubeugen. Angesichts Ihrer Ernährungsgewohnheiten müssen Sie mehr frisches Gemüse und Obst essen. Bei der Auswahl von Fleischprodukten müssen Sie sich auf hochwertige Fette konzentrieren, wie sie zum Beispiel in magerem Fleisch und Fisch enthalten sind. Um die Vorteile einer ausgewogenen Ernährung voll auszuschöpfen, müssen Sie sich angemessen körperlich betätigen. Bewegen Sie sich regelmäßig oder treiben Sie Sport?",
    "training:|training": "Verstanden. Regelmäßige körperliche Aktivität kann oft einen positiven Einfluss auf hohen Blutdruck haben. Es scheint, dass Sie an sportlichen Aktivitäten interessiert sind, allerdings ist die Häufigkeit Ihrer Bewegung momentan eher gering. Sie müssen drei Mal pro Woche für 30 bis 45 Minuten ein regelmäßiges Ausdauertraining absolvieren. Gibt es bestimmte Zeiten, die für Sie am besten wären, um das Training in Ihren Alltag einzuplanen? Beispielsweise nach der Arbeit?",
    "feierabend:|feierabend": "Das verstehe ich. Es ist immer eine Herausforderung, Arbeit und Sport im Gleichgewicht zu bringen. Aber Sie müssen die körperliche Aktivität schrittweise in Ihren Alltag integrieren. Zum Beispiel machen Sie isometrischen Kraftübungen: Stellen Sie sich mit dem Rücken an die Wand, gehen Sie langsam in die Hocke und halten Sie diese Position für zwei Minuten. Das wiederholen Sie viermal hintereinander mit Pausen an drei Tagen pro Woche. Kann ich Ihnen noch mit etwas anderem behilflich sein?",
    "abschluss:|abschluss": "Kein Problem. Bitte beachten Sie, dass Sie sich bei konkreten medizinischen Fragen an einen Facharzt wenden müssen. Ich wünsche Ihnen gute Gesundheit!"
}

st.title("Medical AI Chatbot")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Guten Tag! Wir wissen, dass die familiäre Vorgeschichte die Gesundheit einer Person beeinflussen kann. Die Anpassung von Lebensgewohnheiten ist der Schlüssel zur Krankheitsprävention. Hat Ihre Familie ähnliche Gesundheitsprobleme? Haben Sie darüber nachgedacht, wie Sie durch die Verbesserung Ihrer täglichen Gewohnheiten Ihre Gesundheit optimieren können?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if "last_input" not in st.session_state:
    st.session_state.last_input = ""
    
if prompt := st.chat_input("Bitte geben Sie Ihren Text im richtigen Format ein."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    logger.info(f"User input logged: {prompt}")  

    found_response = False
    for pattern, response in keyword_to_response.items():
        if re.search(pattern, prompt.lower()):
            assistant_response = response
            found_response = True
            break
    if not found_response:
        assistant_response = "Es tut mir leid, ich kann Ihre Eingabe nicht verarbeiten."

    time.sleep(2)
    response_placeholder = st.empty()

    current_text = ""
    for word in assistant_response.split():
        current_text += word + " "
        response_placeholder.text(current_text)
        time.sleep(0.05)  # Delay for 0.5 seconds between words
    response_placeholder.empty()
    with st.chat_message("assistant"):
        st.markdown(assistant_response)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
