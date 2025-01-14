"""
Audio Transcription Package

This package provides functionality for transcribing audio files to text
using the OpenAI Whisper model, with support for various audio formats
and Word document export capabilities.

Modules:
    - transcriber: Contains the main AudioTranscriber class
    - utils: Utility functions for document creation and file handling
"""

from .transcriber import AudioTranscriber
from .utils import create_word_document

__version__ = "1.0.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"

# Export main classes and functions
__all__ = ['AudioTranscriber', 'create_word_document']