import os
import time
import glob
import streamlit as st
import pytesseract
from PIL import Image, ImageOps
from gtts import gTTS
from deep_translator import GoogleTranslator

text = " "

def text_to_speech(input_language, output_language, text, tld):
    # Traducción mediante deep-translator compatible con Python 3.14
    trans_text = GoogleTranslator(source=input_language, target=output_language).translate(text)
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20].strip()
        if not my_file_name:
            my_file_name = "audio"
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)

st.title("Reconocimiento Óptico de Caracteres")
st.subheader("Elige la fuente de la imágen, esta puede venir de la cámara o cargando un archivo")

cam_ = st.checkbox("Usar Cámara")

if cam_:
    img_file_buffer = st.camera_input("Toma una Foto")
else:
    img_file_buffer = None
    
with st.sidebar:
    st.subheader("Procesamiento para Cámara")
    filtro = st.radio("Filtro para imagen con cámara", ('Con Filtro', 'Sin Filtro'))

bg_image = st.file_uploader("Cargar Imagen:", type=["png", "jpg", "jpeg"])
if bg_image is not None:
    uploaded_file = bg_image
    st.image(uploaded_file, caption='Imagen cargada.', use_container_width=True)
    
    # Procesar la imagen cargada con PIL
    image_uploaded = Image.open(uploaded_file)
    text = pytesseract.image_to_string(image_uploaded)
    st.write(text)

if img_file_buffer is not None:
    # Cargar la foto de la cámara con PIL
    image_cam = Image.open(img_file_buffer)

    if filtro == 'Con Filtro':
        image_processed = ImageOps.invert(image_cam.convert('RGB'))
    else:
        image_processed = image_cam
        
    text = pytesseract.image_to_string(image_processed) 
    st.write(text) 

with st.sidebar:
    st.subheader("Parámetros de traducción")
    
    try:
        os.mkdir("temp")
    except:
        pass

    in_lang = st.selectbox(
        "Seleccione el lenguaje de entrada",
        ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"),
    )
    if in_lang == "Ingles":
        input_language = "en"
    elif in_lang == "Español":
        input_language = "es"
    elif in_lang == "Bengali":
        input_language = "bn"
    elif in_lang == "koreano":
        input_language = "ko"
    elif in_lang == "Mandarin":
        input_language = "zh-CN"
    elif in_lang == "Japones":
        input_language = "ja"
    
    out_lang = st.selectbox(
        "Select your output language",
        ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"),
    )
    if out_lang == "Ingles":
        output_language = "en"
    elif out_lang == "Español":
        output_language = "es"
    elif out_lang == "Bengali":
        output_language = "bn"
    elif out_lang == "koreano":
        output_language = "ko"
    elif out_lang == "Mandarin":
        output_language = "zh-CN"
    elif out_lang == "Japones":
        output_language = "ja"
    
    english_accent = st.selectbox(
        "Seleccione el acento",
        (
            "Default",
            "India",
            "United Kingdom",
            "United States",
            "Canada",
            "Australia",
            "Ireland",
            "South Africa",
        ),
    )
    
    if english_accent == "Default":
        tld = "com"
    elif english_accent == "India":
        tld = "co.in"
    elif english_accent == "United Kingdom":
        tld = "co.uk"
    elif english_accent == "United States":
        tld = "com"
    elif english_accent == "Canada":
        tld = "ca"
    elif english_accent == "Australia":
        tld = "com.au"
    elif english_accent == "Ireland":
        tld = "ie"
    elif english_accent == "South Africa":
        tld = "co.za"

    display_output_text = st.checkbox("Mostrar texto")

    if st.button("convert"):
        result, output_text = text_to_speech(input_language, output_language, text, tld)
        audio_file = open(f"temp/{result}.mp3", "rb")
        audio_bytes = audio_file.read()
        st.markdown(f"## Tu audio:")
        st.audio(audio_bytes, format="audio/mp3", start_time=0)
    
        if display_output_text:
            st.markdown(f"## Texto de salida:")
            st.write(f" {output_text}")


 
    
    
