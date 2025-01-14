import unittest
import numpy as np
from io import BytesIO
import soundfile as sf
from src.transcriber import AudioTranscriber
from src.utils import create_word_document

class TestAudioTranscriber(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests."""
        cls.transcriber = AudioTranscriber(model_name="base")
        
        # Create a simple test audio file
        sample_rate = 16000
        duration = 1  # seconds
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio_data = np.sin(2 * np.pi * 440 * t)  # 440 Hz sine wave
        cls.test_audio = BytesIO()
        sf.write(cls.test_audio, audio_data, sample_rate, format='WAV')
        cls.test_audio.seek(0)

    def test_process_audio(self):
        """Test audio processing functionality."""
        # Reset buffer position
        self.test_audio.seek(0)
        
        # Process audio
        audio_array, sample_rate = self.transcriber.process_audio(self.test_audio)
        
        # Assertions
        self.assertIsInstance(audio_array, np.ndarray)
        self.assertEqual(audio_array.dtype, np.float32)
        self.assertEqual(len(audio_array.shape), 1)  # Should be mono
        self.assertGreater(len(audio_array), 0)  # Should contain data

    def test_transcribe_invalid_audio(self):
        """Test transcription with invalid audio data."""
        invalid_audio = BytesIO(b"invalid audio data")
        
        with self.assertRaises(Exception):
            self.transcriber.transcribe(invalid_audio)

    def test_create_word_document(self):
        """Test Word document creation."""
        test_text = "This is a test transcription."
        doc_buffer = create_word_document(test_text)
        
        self.assertIsInstance(doc_buffer, BytesIO)
        self.assertGreater(doc_buffer.getbuffer().nbytes, 0)

def run_tests():
    unittest.main()

if __name__ == '__main__':
    run_tests()