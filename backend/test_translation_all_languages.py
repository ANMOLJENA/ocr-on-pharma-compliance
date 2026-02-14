#!/usr/bin/env python
"""
Comprehensive tests for TranslationService with all 40+ supported languages.

This test suite validates that the TranslationService can successfully translate
text from all supported languages to English. Tests are organized by language group:
- European languages (14)
- Asian languages (3)
- Indian languages (10)
- Additional languages (1)

**Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5, 4.6**
"""

import pytest
from services.translation_service import TranslationService


class TestTranslationEuropeanLanguages:
    """Test translation for European languages"""

    def test_translate_english(self):
        """Test English text (should pass through without translation)"""
        text = "Hello world, this is a test"
        result = TranslationService.translate_to_english(text, "en")
        
        assert result["success"] is True
        assert result["translated_text"] == text
        assert result["error"] is None

    def test_translate_french(self):
        """Test French to English translation"""
        text = "Bonjour le monde, ceci est un test"
        result = TranslationService.translate_to_english(text, "fr")
        
        assert result["success"] is True
        assert len(result["translated_text"]) > 0
        assert result["error"] is None
        # Verify it's translated (should contain English words)
        assert "hello" in result["translated_text"].lower() or "world" in result["translated_text"].lower()

    def test_translate_german(self):
        """Test German to English translation"""
        text = "Hallo Welt, das ist ein Test"
        result = TranslationService.translate_to_english(text, "de")
        
        assert result["success"] is True
        assert len(result["translated_text"]) > 0
        assert result["error"] is None

    def test_translate_spanish(self):
        """Test Spanish to English translation"""
        text = "Hola mundo, esto es una prueba"
        result = TranslationService.translate_to_english(text, "es")
        
        assert result["success"] is True
        assert len(result["translated_text"]) > 0
        assert result["error"] is None

    def test_translate_italian(self):
        """Test Italian to English translation"""
        text = "Ciao mondo, questo è un test"
        result = TranslationService.translate_to_english(text, "it")
        
        assert result["success"] is True
        assert len(result["translated_text"]) > 0
        assert result["error"] is None

    def test_translate_portuguese(self):
        """Test Portuguese to English translation"""
        text = "Olá mundo, isto é um teste"
        result = TranslationService.translate_to_english(text, "pt")
        
        assert result["success"] is True
        assert len(result["translated_text"]) > 0
        assert result["error"] is None

    def test_translate_russian(self):
        """Test Russian to English translation"""
        text = "Привет мир, это тест"
        result = TranslationService.translate_to_english(text, "ru")
        
        assert result["success"] is True
        assert len(result["translated_text"]) > 0
        assert result["error"] is None

    def test_translate_dutch(self):
        """Test Dutch to English translation"""
        text = "Hallo wereld, dit is een test"
        result = TranslationService.translate_to_english(text, "nl")
        
        assert result["success"] is True
        assert len(result["translated_text"]) > 0
        assert result["error"] is None

    def test_translate_swedish(self):
        """Test Swedish to English translation"""
        text = "Hej världen, det här är ett test"
        result = TranslationService.translate_to_english(text, "sv")
        
        assert result["success"] is True
        assert len(result["translated_text"]) > 0
        assert result["error"] is None

    def test_translate_polish(self):
        """Test Polish to English translation"""
        text = "Cześć świecie, to jest test"
        result = TranslationService.translate_to_english(text, "pl")
        
        assert result["success"] is True
        assert len(result["translated_text"]) > 0
        assert result["error"] is None

    def test_translate_turkish(self):
        """Test Turkish to English translation"""
        text = "Merhaba dünya, bu bir test"
        result = TranslationService.translate_to_english(text, "tr")
        
        assert result["success"] is True
        assert len(result["translated_text"]) > 0
        assert result["error"] is None