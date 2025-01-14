import whisper
import numpy as np
import soundfile as sf
from io import BytesIO
from typing import Union, Tuple, Callable
import logging
import time
from datetime import datetime

class AudioTranscriber:
    def __init__(self, model_name: str = "base", progress_callback: Callable = None, language: str = 'fr'):
        """
        Initialise le transcripteur avec le modèle spécifié et la langue.
        
        Args:
            model_name (str): Nom du modèle Whisper à utiliser
            progress_callback (Callable): Fonction de callback pour la progression
            language (str): Code de langue ('fr' ou 'en')
        """
        self.model_name = model_name
        self.progress_callback = progress_callback
        self.language = language
        self.setup_logging()
        
    def update_progress(self, message: str, progress: float):
        """Met à jour la progression via le callback et le logging."""
        if self.progress_callback:
            self.progress_callback(message, progress)
        self.logger.info(f"{message} - {progress:.2f}%")

    def transcribe(self, audio_file: BytesIO) -> str:
        """
        Transcrit le fichier audio en texte avec suivi de la progression.
        
        Args:
            audio_file (BytesIO): Fichier audio à transcrire
            
        Returns:
            str: Texte transcrit
        """
        try:
            self.update_progress("Chargement du modèle Whisper", 0)
            model = whisper.load_model(self.model_name)
            
            audio_array, _ = self.process_audio(audio_file)
            
            self.update_progress("Démarrage de la transcription", 40)
            start_time = time.time()
            
            # Configuration spécifique à la langue
            task = "transcribe"
            language_code = "fr" if self.language == "fr" else "en"
            
            result = model.transcribe(
                audio_array,
                task=task,
                language=language_code,
                fp16=False
            )
            
            end_time = time.time()
            duration = end_time - start_time
            
            self.update_progress(
                f"Transcription terminée en {duration:.2f} secondes",
                100
            )
            return result["text"]
            
        except Exception as e:
            self.logger.error(f"Erreur de transcription: {str(e)}")
            raise