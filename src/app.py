import streamlit as st
from transcriber import AudioTranscriber
from utils import create_word_document, setup_logging, load_translations
import logging
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Transcription Audio Multilingue",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Configuration du logging
logger = setup_logging()

class TranscriptionApp:
    def __init__(self):
        self.setup_session_state()
        self.load_language_resources()
        self.setup_sidebar()
        
    def load_language_resources(self):
        """Charge les ressources linguistiques."""
        self.translations = load_translations()
        
    def get_text(self, key):
        """Récupère le texte traduit selon la langue sélectionnée."""
        lang = st.session_state.get('language', 'fr')
        return self.translations[lang].get(key, key)
        
    def setup_session_state(self):
        """Initialise les variables de session."""
        if 'language' not in st.session_state:
            st.session_state.language = 'fr'
        if 'progress' not in st.session_state:
            st.session_state.progress = 0
        if 'status' not in st.session_state:
            st.session_state.status = ""
        if 'log_messages' not in st.session_state:
            st.session_state.log_messages = []
        if 'transcription_result' not in st.session_state:
            st.session_state.transcription_result = None

    def setup_sidebar(self):
        """Configure la barre latérale de l'application."""
        with st.sidebar:
            st.title("⚙️ " + self.get_text('settings'))
            
            # Sélection de la langue
            selected_lang = st.selectbox(
                self.get_text('select_language'),
                ['Français', 'English'],
                index=0 if st.session_state.language == 'fr' else 1
            )
            st.session_state.language = 'fr' if selected_lang == 'Français' else 'en'
            
            # Configuration du modèle
            st.markdown("### " + self.get_text('model_config'))
            st.session_state.model_type = st.selectbox(
                self.get_text('select_model'),
                ["tiny", "base", "small"],
                index=1
            )
            
            # État du système
            st.markdown("### " + self.get_text('system_status'))
            st.info(
                f"{self.get_text('current_model')}: {st.session_state.model_type}\n"
                f"{self.get_text('processing_mode')}: CPU\n"
                f"{self.get_text('last_update')}: {datetime.now().strftime('%H:%M:%S')}"
            )

    def update_progress(self, message: str, progress: float):
        """Met à jour la progression et les logs."""
        st.session_state.progress = progress
        st.session_state.status = message
        logger.info(f"{message} - {progress:.2f}%")
        st.session_state.log_messages.append(
            f"{datetime.now().strftime('%H:%M:%S')} - {message}"
        )

    def display_output_section(self):
        """Gère l'affichage et l'exportation des résultats."""
        output_section = st.container()

        with output_section:
            if st.session_state.transcription_result:
                output_format = st.radio(
                    self.get_text('choose_format'),
                    [self.get_text('display_text'), self.get_text('download_word')],
                    key="output_format"
                )
                
                if output_format == self.get_text('display_text'):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        text_content = st.text_area(
                            self.get_text('transcription_result'),
                            value=st.session_state.transcription_result,
                            height=300,
                            disabled=False
                        )
                    with col2:
                        if st.button("📋 " + self.get_text('copy_clipboard')):
                            st.write(self.get_text('text_copied'))
                else:
                    word_doc = create_word_document(
                        st.session_state.transcription_result,
                        title=f"{self.get_text('transcription')} {datetime.now().strftime('%Y-%m-%d')}"
                    )
                    st.download_button(
                        "⬇️ " + self.get_text('download_word_button'),
                        word_doc,
                        file_name=f"transcription_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key="download_button"
                    )

    def main(self):
        """Logique principale de l'application."""
        st.title("🎙️ " + self.get_text('app_title'))
        st.write(self.get_text('app_description'))

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
                    transcriber = AudioTranscriber(
                        model_name=st.session_state.model_type,
                        progress_callback=self.update_progress,
                        language=st.session_state.language
                    )
                    
                    with st.spinner(self.get_text('processing')):
                        while st.session_state.progress < 100:
                            progress_bar.progress(int(st.session_state.progress))
                            status_text.text(st.session_state.status)
                            
                            if st.session_state.progress == 0:
                                transcription = transcriber.transcribe(audio_file)
                                st.session_state.transcription_result = transcription
                                
                        progress_bar.progress(100)
                        status_text.text(self.get_text('transcription_completed'))
                    
                    st.success(self.get_text('success_message'))
                    self.display_output_section()
                        
                except Exception as e:
                    st.error(f"{self.get_text('error_message')}: {str(e)}")
                    logger.error(f"Transcription error: {str(e)}")

        # Console de débogage
        st.markdown("---")
        with st.expander("🔍 " + self.get_text('debug_console'), expanded=True):
            st.markdown("### " + self.get_text('system_logs'))
            log_container = st.container()
            
            for message in reversed(st.session_state.log_messages[-50:]):
                log_container.text(message)

if __name__ == "__main__":
    app = TranscriptionApp()
    app.main()