import logging
from docx import Document
from io import BytesIO
from typing import Union
from datetime import datetime

def load_translations():
    return {
        'fr': {
            'app_title': "Transcription Audio Multilingue",
            'info_title': "Informations importantes",
            'app_info': """
                Cette application utilise l'Intelligence Artificielle pour transcrire vos fichiers audio.
                
                Temps de traitement estimé :
                - Fichiers courts (<1 min) : environ 30 secondes
                - Fichiers moyens (1-5 min) : 1-2 minutes
                - Fichiers longs (>5 min) : 2-5 minutes
                
                Pour de meilleurs résultats, utilisez des enregistrements clairs avec peu de bruit de fond.
            """,
            'settings': "Paramètres",
            'select_language': "Langue de l'interface",
            'model_config': "Configuration",
            'select_model': "Taille du modèle",
            'processing': "Traitement en cours...",
            'choose_file': "Sélectionner un fichier audio",
            'supported_formats': "Formats supportés : MP3, WAV, M4A",
            'start_transcription': "Démarrer la transcription",
            'success_message': "Transcription terminée avec succès ! 🎉",
            'error_message': "Une erreur s'est produite",
            'transcription_result': "Résultat de la transcription",
            'copy_clipboard': "Copier",
            'text_copied': "Texte copié !",
            'download_word': "Télécharger en Word"
        },
        'en': {
            'app_title': "Multilingual Audio Transcription",
            'info_title': "Important Information",
            'app_info': """
                This application uses Artificial Intelligence to transcribe your audio files.
                
                Estimated processing time:
                - Short files (<1 min): about 30 seconds
                - Medium files (1-5 min): 1-2 minutes
                - Long files (>5 min): 2-5 minutes
                
                For best results, use clear recordings with minimal background noise.
            """,
            'settings': "Settings",
            'select_language': "Interface Language",
            'model_config': "Configuration",
            'select_model': "Model Size",
            'processing': "Processing...",
            'choose_file': "Select an audio file",
            'supported_formats': "Supported formats: MP3, WAV, M4A",
            'start_transcription': "Start Transcription",
            'success_message': "Transcription completed successfully! 🎉",
            'error_message': "An error occurred",
            'transcription_result': "Transcription Result",
            'copy_clipboard': "Copy",
            'text_copied': "Text copied!",
            'download_word': "Download as Word"
        }
    }

def setup_logging() -> logging.Logger:
    """Configure logging for the application."""
    logger = logging.getLogger("WhisperApp")
    logger.setLevel(logging.INFO)
    
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    return logger

def create_word_document(text: str, title: str = "Transcription") -> BytesIO:
    """Create a Word document from the transcribed text."""
    doc = Document()
    
    # Add metadata
    doc.core_properties.author = "Whisper Transcription App"
    doc.core_properties.created = datetime.now()
    
    # Add content
    doc.add_heading(title, level=1)
    doc.add_paragraph(text)
    
    # Add footer with timestamp
    section = doc.sections[0]
    footer = section.footer
    footer.paragraphs[0].text = f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    
    buffer = BytesIO()
    doc.save(buffer)
    buffer.seek(0)
    return buffer
