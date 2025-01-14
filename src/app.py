import streamlit as st
from transcriber import AudioTranscriber
from utils import create_word_document, setup_logging, load_translations
import logging
from datetime import datetime

st.set_page_config(
    page_title="Transcription Audio Multilingue",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

class TranscriptionApp:
    def __init__(self):
        self.translations = load_translations()  # Charger les traductions
        self.setup_session_state()
        self.setup_sidebar()
        
    def get_text(self, key: str) -> str:
        """Récupère le texte traduit selon la langue actuelle"""
        return self.translations[st.session_state.language][key]

    def setup_session_state(self):
        if 'language' not in st.session_state:
            st.session_state.language = 'fr'
        if 'progress' not in st.session_state:
            st.session_state.progress = 0
        if 'status' not in st.session_state:
            st.session_state.status = ""
        if 'transcription_result' not in st.session_state:
            st.session_state.transcription_result = None
        if 'transcriber' not in st.session_state:
            st.session_state.transcriber = None

if __name__ == "__main__":
    app = TranscriptionApp()
    app.main()