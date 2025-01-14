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
        self.setup_session_state()
        self.load_language_resources()
        self.setup_sidebar()
        
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

    def setup_sidebar(self):
        with st.sidebar:
            st.title("⚙️ " + self.get_text('settings'))
            
            selected_lang = st.selectbox(
                self.get_text('select_language'),
                ['Français', 'English'],
                index=0 if st.session_state.language == 'fr' else 1
            )
            st.session_state.language = 'fr' if selected_lang == 'Français' else 'en'
            
            st.markdown("### " + self.get_text('model_config'))
            model_size = st.selectbox(
                self.get_text('select_model'),
                ["tiny", "base"],
                index=0,
                help="'tiny' est plus rapide, 'base' est plus précis"
            )
            
            if model_size != getattr(st.session_state.transcriber, 'model_name', None):
                st.session_state.transcriber = AudioTranscriber(
                    model_name=model_size,
                    language=st.session_state.language
                )

    def main(self):
        st.title("🎙️ " + self.get_text('app_title'))
        
        with st.expander("ℹ️ " + self.get_text('info_title'), expanded=True):
            st.info(self.get_text('app_info'))

        col1, col2 = st.columns([2, 1])
        
        with col1:
            audio_file = st.file_uploader(
                self.get_text('choose_file'),
                type=["mp3", "wav", "m4a"],
                help=self.get_text('supported_formats')
            )

        if audio_file:
            st.audio(audio_file)
            
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            if st.button(self.get_text('start_transcription'), type="primary"):
                try:
                    if not st.session_state.transcriber:
                        st.session_state.transcriber = AudioTranscriber(
                            model_name="tiny",
                            language=st.session_state.language
                        )
                    
                    transcriber = st.session_state.transcriber
                    
                    def update_progress(message, progress):
                        progress_bar.progress(int(progress))
                        status_text.text(f"{message} ({progress:.0f}%)")
                        
                    transcriber.progress_callback = update_progress
                    
                    with st.spinner(self.get_text('processing')):
                        transcription = transcriber.transcribe(audio_file)
                        st.session_state.transcription_result = transcription
                    
                    st.success(self.get_text('success_message'))
                    self.display_output_section()
                    
                except Exception as e:
                    st.error(f"{self.get_text('error_message')}: {str(e)}")

if __name__ == "__main__":
    app = TranscriptionApp()
    app.main()