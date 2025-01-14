import whisper
import numpy as np
import soundfile as sf
from io import BytesIO
from typing import Union, Tuple, Callable
import logging
import time
from datetime import datetime

class AudioTranscriber:
    def __init__(self, model_name: str = "tiny", progress_callback: Callable = None, language: str = 'fr'):
        self.model_name = model_name
        self.progress_callback = progress_callback
        self.language = language
        self.logger = self.setup_logging()
        self._model = None  # Cache pour le modèle

    def setup_logging(self) -> logging.Logger:
        logger = logging.getLogger("WhisperTranscriber")
        if not logger.handlers:
            logger.setLevel(logging.INFO)
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger

    def get_model(self):
        if self._model is None:
            self._model = whisper.load_model(self.model_name)
        return self._model

    def process_audio(self, audio_file: BytesIO) -> Tuple[np.ndarray, int]:
        try:
            self.update_progress("Lecture du fichier audio", 10)
            audio_bytes = audio_file.read()
            audio_array, sample_rate = sf.read(BytesIO(audio_bytes))
            
            if len(audio_array.shape) > 1:
                self.update_progress("Conversion en mono", 15)
                audio_array = audio_array.mean(axis=1)
            
            self.update_progress("Normalisation audio", 20)
            audio_array = audio_array.astype(np.float32)
            
            # Normalisation du volume
            if np.abs(audio_array).max() > 0:
                audio_array = audio_array / np.abs(audio_array).max()
            
            return audio_array, sample_rate
            
        except Exception as e:
            self.logger.error(f"Erreur de traitement audio: {str(e)}")
            raise RuntimeError(f"Erreur lors du traitement audio: {str(e)}")

    def update_progress(self, message: str, progress: float):
        if self.progress_callback:
            self.progress_callback(message, progress)
        self.logger.info(f"{message} - {progress:.2f}%")

    def transcribe(self, audio_file: BytesIO) -> str:
        try:
            self.update_progress("Initialisation du modèle", 0)
            model = self.get_model()
            
            self.update_progress("Préparation de l'audio", 20)
            audio_array, _ = self.process_audio(audio_file)
            
            self.update_progress("Configuration de la transcription", 30)
            language_code = "fr" if self.language == "fr" else "en"
            
            self.update_progress("Transcription en cours...", 40)
            start_time = time.time()
            
            result = model.transcribe(
                audio_array,
                task="transcribe",
                language=language_code,
                fp16=False,
                condition_on_previous_text=False,
                initial_prompt="Transcription audio en français." if language_code == "fr" else "Audio transcription in English."
            )
            
            duration = time.time() - start_time
            self.update_progress(f"Transcription terminée en {duration:.1f} secondes", 100)
            
            return result["text"]
            
        except Exception as e:
            error_message = f"Erreur de transcription: {str(e)}"
            self.logger.error(error_message)
            raise RuntimeError(error_message)