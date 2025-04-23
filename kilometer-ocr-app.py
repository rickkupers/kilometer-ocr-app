import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import tempfile

st.set_page_config(page_title="Kilometerstand Uitlezer", layout="centered")
st.title("📸 Kilometerstand uitlezen via foto")

uploaded_file = st.file_uploader("Upload een foto van de kilometerteller", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Tijdelijk bestand opslaan
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_path = tmp_file.name

    # Afbeelding tonen
    image = Image.open(tmp_path)
    st.image(image, caption='Ingevoerde afbeelding', use_column_width=True)

    # OCR uitvoeren
    with st.spinner("Bezig met uitlezen..."):
        reader = easyocr.Reader(['en'])
        results = reader.readtext(tmp_path)

    # Resultaten filteren en tonen
    gevonden_standen = []
    for detection in results:
        text = detection[1]
        if text.replace('.', '').replace(',', '').isdigit():
            gevonden_standen.append(text)

    if gevonden_standen:
        st.success(f"📍 Herkende kilometerstand(en): {', '.join(gevonden_standen)}")
    else:
        st.warning("Geen duidelijke kilometerstand gevonden. Probeer een scherpere foto met minder reflectie.")
