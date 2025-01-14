# src/transcriber.py
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
        self.logger = self.setup_logging()
        
    def setup_logging(self) -> logging.Logger:
        """
        Configure le système de logging pour le transcripteur.
        
        Returns:
            logging.Logger: Logger configuré pour le transcripteur
        """
        logger = logging.getLogger("WhisperTranscriber")
        
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger

    def process_audio(self, audio_file: BytesIO) -> Tuple[np.ndarray, int]:
        """
        Traite le fichier audio pour la transcription.
        
        Args:
            audio_file (BytesIO): Fichier audio à traiter
            
        Returns:
            Tuple[np.ndarray, int]: Tableau audio traité et taux d'échantillonnage
        """
        try:
            self.update_progress("Lecture du fichier audio", 10)
            audio_bytes = audio_file.read()
            audio_array, sample_rate = sf.read(BytesIO(audio_bytes))
            
            self.update_progress("Traitement du format audio", 20)
            if len(audio_array.shape) > 1:
                audio_array = audio_array.mean(axis=1)
            
            audio_array = audio_array.astype(np.float32)
            self.update_progress("Prétraitement audio terminé", 30)
            
            return audio_array, sample_rate
            
        except Exception as e:
            self.logger.error(f"Erreur de traitement audio: {str(e)}")
            raise RuntimeError(f"Erreur lors du traitement du fichier audio: {str(e)}")

    def update_progress(self, message: str, progress: float):
        """
        Met à jour la progression via le callback et le logging.
        
        Args:
            message (str): Message de progression
            progress (float): Pourcentage de progression
        """
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
            language_code = "fr" if self.language == "fr" else "en"
            
            result = model.transcribe(
                audio_array,
                task="transcribe",
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
            error_message = f"Erreur lors de la transcription: {str(e)}"
            self.logger.error(error_message)
            raise RuntimeError(error_message)