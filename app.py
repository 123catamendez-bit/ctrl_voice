import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

# ==================== CONFIGURACIÓN DE MQTT ==================== #
def on_publish(client, userdata, result):
    print("📡 Dato publicado correctamente.\n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

broker = "broker.mqttdashboard.com"
port = 1883
client1 = paho.Client("catica")
client1.on_message = on_message

# ==================== ESTILOS GALÁCTICOS ==================== #
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background: radial-gradient(circle at 20% 20%, #12002F, #000010 80%);
    color: white;
    overflow: hidden;
    position: relative;
}

[data-testid="stAppViewContainer"]::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 200%;
    height: 200%;
    background: transparent url('https://cdn.pixabay.com/photo/2016/11/18/22/23/star-1837306_1280.png') repeat;
    background-size: 500px 500px;
    animation: moveStars 100s linear infinite;
    opacity: 0.3;
    z-index: 0;
}

@keyframes moveStars {
    from { transform: translateY(0px); }
    to { transform: translateY(-500px); }
}

h1, h2, h3, h4, h5, h6, p, span, label {
    color: #E6E6FA !important;
    text-shadow: 0px 0px 6px rgba(180, 120, 255, 0.8);
}

button[kind="primary"] {
    background-color: #5E17EB !important;
    color: white !important;
    border-radius: 12px !important;
    border: 1px solid #AA7CFF !important;
}

button:hover {
    background-color: #7A3FFF !important;
}

</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# ==================== TÍTULOS Y CONTENIDO ==================== #
st.title("🪐 INTERFACES MULTIMODALES")
st.subheader("🎙️ CONTROL GALÁCTICO POR VOZ 🚀")

image = Image.open('20.jpeg')  # // imagen representativa del micrófono o control
st.image(image, width=250)

st.markdown("---")
st.write("✨ **Toca el botón y comunica tus comandos al universo...**")

# ==================== BOTÓN DE VOZ ==================== #
stt_button = Button(label="🚀 Iniciar Comunicación", width=250)

stt_button.js_on_event("button_click", CustomJS(code="""
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if (value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
"""))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0
)

# ==================== PROCESAMIENTO DE VOZ ==================== #
if result:
    if "GET_TEXT" in result:
        text_captured = result.get("GET_TEXT").strip()
        st.markdown(f"🛰️ Has dicho: **{text_captured}**")

        client1.on_publish = on_publish
        client1.connect(broker, port)
        message = json.dumps({"Act1": text_captured})
        ret = client1.publish("voice_ctrl", message)

    try:
        os.mkdir("temp")
    except:
        pass
