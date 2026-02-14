#!/usr/bin/env python
"""
Property-based tests for LanguageDetectionService using Hypothesis.

This test suite validates the correctness properties of the LanguageDetectionService,
ensuring that the service behaves correctly across a wide range of inputs.

**Validates: Requirements 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 4.7**
"""

import pytest
from hypothesis import given, strategies as st, settings, HealthCheck, assume
from services.language_detection_service import LanguageDetectionService, LANGUAGE_NAMES


class TestLanguageDetectionServiceProperties:
    """Property-based tests for LanguageDetectionService"""

    # ========== Property 8: Language Detection Returns Valid Code ==========
    @given(st.sampled_from([
        "Hello world, this is a test",
        "Bonjour le monde, ceci est un test",
        "Hola mundo, esto es una prueba",
        "Hallo Welt, das ist ein Test",
        "Ciao mondo, questo è un test",
        "Olá mundo, isto é um teste",
        "Привет мир, это тест",
        "Hej världen, det här är ett test",
        "Cześć świecie, to jest test",
        "Merhaba dünya, bu bir testtir",
        "Γεια σας κόσμε, αυτό είναι ένα τεστ",
        "שלום עולם, זה בדיקה",
        "สวัสดีชาวโลก นี่คือการทดสอบ",
        "你好世界，这是一个测试",
        "こんにちは世界、これはテストです",
        "안녕하세요 세계, 이것은 테스트입니다",
        "नमस्ते दुनिया, यह एक परीक्षण है",
        "வணக்கம் உலகம், இது ஒரு சோதனை",
        "హలో ప్రపంచం, ఇది ఒక పరీక్ష",
        "ಹಲೋ ವರ್ಲ್ಡ್, ಇದು ಒಂದು ಪರೀಕ್ಷೆ",
        "നമസ്കാരം ലോകം, ഇത് ഒരു പരീക്ഷയാണ്",
        "Tere maailm, see on test",
    ]))
    @settings(max_examples=20, suppress_health_check=[HealthCheck.too_slow], deadline=None)
    def test_property_8_language_detection_returns_valid_code(self, text):
        """
        **Property 8: Language Detection Returns Valid Code**
        
        For any text in a supported language, the language detection service should 
        return a language_code that exists in the SUPPORTED_LANGUAGES mapping.
        
        **Validates: Requirements 3.1, 3.2, 3.6, 4.7**
        """
        result = LanguageDetectionService.detect_language(text)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "success" in result
        assert "language_code" in result
        assert "language_name" in result
        assert "confidence" in result
        assert "error" in result
        
        # For successful detection
        if result["success"]:
            # Language code should be a string
            assert isinstance(result["language_code"], str)
            assert len(result["language_code"]) > 0
            
            # Language code should be in the LANGUAGE_NAMES mapping
            assert result["language_code"] in LANGUAGE_NAMES, \
                f"Language code '{result['language_code']}' not in LANGUAGE_NAMES mapping"
            
            # Language name should match the code
            assert result["language_name"] == LANGUAGE_NAMES[result["language_code"]]
            
            # Error should be None on success
            assert result["error"] is None

    # ========== Property 9: Language Detection Confidence Range ==========
    @given(st.sampled_from([
        "Hello world, this is a test",
        "Bonjour le monde, ceci est un test",
        "Hola mundo, esto es una prueba",
        "Hallo Welt, das ist ein Test",
        "Ciao mondo, questo è un item",
        "Olá mundo, isto é um teste",
        "Привет мир, это тест",
        "Hej världen, det här är ett test",
        "Cześć świecie, to jest test",
        "Merhaba dünya, bu bir testtir",
        "Γεια σας κόσμε, αυτό είναι ένα τεστ",
        "שלום עולם, זה בדיקה",
        "สวัสดีชาวโลก นี่คือการทดสอบ",
        "你好世界，这是一个测试",
        "こんにちは世界、これはテストです",
        "안녕하세요 세계, 이것은 테스트입니다",
        "नमस्ते दुनिया, यह एक परीक्षण है",
        "வணக்கம் உலகம், இது ஒரு சோதனை",
        "హలో ప్రపంచం, ఇది ఒక పరీక్ష",
        "ಹಲೋ ವರ್ಲ್ಡ್, ಇದು ಒಂದು ಪರೀಕ್ಷೆ",
        "നമസ്കാരം ലോകം, ഇത് ഒരു പരീക്ഷയാണ്",
        "Tere maailm, see on test",
    ]))
    @settings(max_examples=20, suppress_health_check=[HealthCheck.too_slow])
    def test_property_9_language_detection_confidence_range(self, text):
        """
        **Property 9: Language Detection Confidence Range**
        
        For any text, the confidence score returned by language detection should be 
        a number between 0.0 and 1.0 (inclusive).
        
        **Validates: Requirements 3.2**
        """
        result = LanguageDetectionService.detect_language(text)
        
        # Verify response structure
        assert isinstance(result, dict)
        assert "confidence" in result
        
        # Confidence should always be a number
        assert isinstance(result["confidence"], (int, float))
        
        # Confidence should be in valid range [0.0, 1.0]
        assert 0.0 <= result["confidence"] <= 1.0, \
            f"Confidence {result['confidence']} is outside valid range [0.0, 1.0]"

    # ========== Property 10: Multi-Page Language Detection Consistency ==========
    def test_property_10_multi_page_language_detection_consistency(self):
        """
        **Property 10: Multi-Page Language Detection Consistency**
        
        For any multi-page document where all pages are in the same language, 
        the language detection service should return the same language code 
        regardless of which pages are combined.
        
        **Validates: Requirements 3.5**
        """
        # Test with English pages
        english_pages = [
            "Hello world, this is page one",
            "This is page two with more English text",
            "Page three continues with English content",
        ]
        
        # Detect language from all pages
        result_all = LanguageDetectionService.detect_language_from_pages(english_pages)
        
        # Detect language from subset of pages
        result_subset = LanguageDetectionService.detect_language_from_pages(english_pages[:2])
        
        # Both should succeed
        assert result_all["success"] is True
        assert result_subset["success"] is True
        
        # Both should detect the same language
        assert result_all["language_code"] == result_subset["language_code"], \
            "Language detection should be consistent across different page combinations"
        
        # Test with French pages
        french_pages = [
            "Bonjour le monde, ceci est la première page",
            "Ceci est la deuxième page avec plus de texte français",
            "La troisième page continue avec du contenu français",
        ]
        
        result_french_all = LanguageDetectionService.detect_language_from_pages(french_pages)
        result_french_subset = LanguageDetectionService.detect_language_from_pages(french_pages[:2])
        
        assert result_french_all["success"] is True
        assert result_french_subset["success"] is True
        assert result_french_all["language_code"] == result_french_subset["language_code"]

    # ========== Property 19: Language Code Mapping Consistency ==========
    def test_property_19_language_code_mapping_consistency(self):
        """
        **Property 19: Language Code Mapping Consistency**
        
        For any language name in the LANGUAGE_NAMES mapping, the corresponding 
        language code should be a valid ISO 639-1 code that langdetect recognizes.
        
        **Validates: Requirements 4.5, 3.6**
        """
        # Verify all entries in LANGUAGE_NAMES mapping
        assert isinstance(LANGUAGE_NAMES, dict)
        assert len(LANGUAGE_NAMES) > 0
        
        for language_code, language_name in LANGUAGE_NAMES.items():
            # Language code should be a string
            assert isinstance(language_code, str)
            assert len(language_code) > 0
            
            # Language name should be a string
            assert isinstance(language_name, str)
            assert len(language_name) > 0
            
            # Language code should be lowercase (ISO 639-1 convention)
            assert language_code == language_code.lower(), \
                f"Language code '{language_code}' should be lowercase"
            
            # Language code should be 2-5 characters (ISO 639-1 or variants)
            assert 2 <= len(language_code) <= 5, \
                f"Language code '{language_code}' has invalid length"


class TestLanguageDetectionServiceEdgeCases:
    """Edge case tests for LanguageDetectionService"""

    def test_empty_text_handling(self):
        """Test language detection with empty text"""
        result = LanguageDetectionService.detect_language("")
        
        assert result["success"] is False
        assert result["language_code"] is None
        assert result["language_name"] is None
        assert result["confidence"] == 0.0
        assert "error" in result
        assert len(result["error"]) > 0

    def test_whitespace_only_text_handling(self):
        """Test language detection with whitespace-only text"""
        result = LanguageDetectionService.detect_language("   \n\t  ")
        
        assert result["success"] is False
        assert result["language_code"] is None
        assert result["language_name"] is None
        assert result["confidence"] == 0.0
        assert "error" in result

    def test_single_word_detection(self):
        """Test language detection with single word"""
        result = LanguageDetectionService.detect_language("Hello")
        
        # Should attempt detection even with single word
        assert isinstance(result, dict)
        assert "success" in result
        assert "language_code" in result
        assert "confidence" in result

    def test_mixed_language_text(self):
        """Test language detection with mixed language text"""
        # Text with multiple languages
        mixed_text = "Hello world Bonjour le monde"
        result = LanguageDetectionService.detect_language(mixed_text)
        
        # Should return a result (may detect one or the other)
        assert isinstance(result, dict)
        assert "success" in result
        assert "language_code" in result
        
        if result["success"]:
            # Should return a valid language code
            assert result["language_code"] in LANGUAGE_NAMES

    def test_multi_page_empty_list(self):
        """Test multi-page detection with empty list"""
        result = LanguageDetectionService.detect_language_from_pages([])
        
        assert result["success"] is False
        assert result["language_code"] is None
        assert result["language_name"] is None
        assert result["confidence"] == 0.0
        assert "error" in result

    def test_multi_page_all_empty_strings(self):
        """Test multi-page detection with all empty strings"""
        result = LanguageDetectionService.detect_language_from_pages(["", "  ", "\n"])
        
        assert result["success"] is False
        assert result["language_code"] is None
        assert result["language_name"] is None
        assert result["confidence"] == 0.0
        assert "error" in result

    def test_multi_page_mixed_empty_and_valid(self):
        """Test multi-page detection with mix of empty and valid text"""
        pages = ["", "Hello world", "  ", "This is a test"]
        result = LanguageDetectionService.detect_language_from_pages(pages)
        
        # Should succeed by combining valid text
        assert result["success"] is True
        assert result["language_code"] is not None
        assert result["language_name"] is not None
        assert result["confidence"] > 0.0

    def test_response_structure_on_error(self):
        """Test that error responses have consistent structure"""
        result = LanguageDetectionService.detect_language("")
        
        # Verify all expected keys are present
        assert "success" in result
        assert "language_code" in result
        assert "language_name" in result
        assert "confidence" in result
        assert "error" in result
        
        # Verify types on error
        assert result["success"] is False
        assert result["language_code"] is None
        assert result["language_name"] is None
        assert isinstance(result["confidence"], (int, float))
        assert isinstance(result["error"], str)

    def test_supported_languages_count(self):
        """Test that we have sufficient language support"""
        # Should have at least 40 languages as per requirements
        assert len(LANGUAGE_NAMES) >= 40, \
            f"Expected at least 40 languages, got {len(LANGUAGE_NAMES)}"

    def test_required_languages_present(self):
        """Test that all required language groups are present"""
        required_languages = {
            # European languages
            'en': 'English',
            'fr': 'French',
            'de': 'German',
            'es': 'Spanish',
            'it': 'Italian',
            'pt': 'Portuguese',
            'ru': 'Russian',
            'nl': 'Dutch',
            'sv': 'Swedish',
            'pl': 'Polish',
            'tr': 'Turkish',
            'el': 'Greek',
            'he': 'Hebrew',
            'th': 'Thai',
            # Asian languages
            'zh-cn': 'Chinese (Simplified)',
            'ja': 'Japanese',
            'ko': 'Korean',
            # Indian languages
            'hi': 'Hindi',
            'ta': 'Tamil',
            'te': 'Telugu',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'gu': 'Gujarati',
            'mr': 'Marathi',
            'bn': 'Bengali',
            'pa': 'Punjabi',
            'ur': 'Urdu',
            # Additional
            'et': 'Estonian',
        }
        
        for lang_code in required_languages.keys():
            assert lang_code in LANGUAGE_NAMES, \
                f"Required language '{lang_code}' not found in LANGUAGE_NAMES"

    def test_language_name_non_empty(self):
        """Test that all language names are non-empty"""
        for language_code, language_name in LANGUAGE_NAMES.items():
            assert len(language_name.strip()) > 0, \
                f"Language name for code '{language_code}' is empty"

    def test_detect_language_from_pages_combines_text(self):
        """Test that multi-page detection properly combines text"""
        # Create pages with different amounts of text
        pages = [
            "Hello",
            "world",
            "this",
            "is",
            "a",
            "test",
        ]
        
        result = LanguageDetectionService.detect_language_from_pages(pages)
        
        # Should succeed by combining all pages
        assert result["success"] is True
        assert result["language_code"] is not None


class TestLanguageDetectionServiceIntegration:
    """Integration tests for LanguageDetectionService"""

    def test_detect_language_english(self):
        """Test English language detection"""
        result = LanguageDetectionService.detect_language(
            "The quick brown fox jumps over the lazy dog"
        )
        
        assert result["success"] is True
        assert result["language_code"] == "en"
        assert result["language_name"] == "English"
        assert result["confidence"] > 0.5

    def test_detect_language_french(self):
        """Test French language detection"""
        result = LanguageDetectionService.detect_language(
            "Le renard brun rapide saute par-dessus le chien paresseux"
        )
        
        assert result["success"] is True
        assert result["language_code"] == "fr"
        assert result["language_name"] == "French"
        assert result["confidence"] > 0.5

    def test_detect_language_spanish(self):
        """Test Spanish language detection"""
        result = LanguageDetectionService.detect_language(
            "El rápido zorro marrón salta sobre el perro perezoso"
        )
        
        assert result["success"] is True
        assert result["language_code"] == "es"
        assert result["language_name"] == "Spanish"
        assert result["confidence"] > 0.5

    def test_detect_language_german(self):
        """Test German language detection"""
        result = LanguageDetectionService.detect_language(
            "Der schnelle braune Fuchs springt über den faulen Hund"
        )
        
        assert result["success"] is True
        assert result["language_code"] == "de"
        assert result["language_name"] == "German"
        assert result["confidence"] > 0.5

    def test_detect_language_hindi(self):
        """Test Hindi language detection"""
        result = LanguageDetectionService.detect_language(
            "तेज भूरी लोमड़ी आलसी कुत्ते के ऊपर कूदती है"
        )
        
        assert result["success"] is True
        assert result["language_code"] == "hi"
        assert result["language_name"] == "Hindi"
        assert result["confidence"] > 0.5

    def test_detect_language_tamil(self):
        """Test Tamil language detection"""
        result = LanguageDetectionService.detect_language(
            "வேகமான பழுப்பு நரி சோம்பேறி நாயின் மீது குதிக்கிறது"
        )
        
        assert result["success"] is True
        assert result["language_code"] == "ta"
        assert result["language_name"] == "Tamil"
        assert result["confidence"] > 0.5

    def test_detect_language_chinese(self):
        """Test Chinese language detection"""
        result = LanguageDetectionService.detect_language(
            "敏捷的棕色狐狸跳过懒狗。这是一个更长的中文文本，以确保正确检测语言。"
        )
        
        assert result["success"] is True
        # Chinese can be detected as zh-cn or zh-tw or zh
        assert result["language_code"] in ["zh-cn", "zh-tw", "zh"], \
            f"Expected Chinese language code, got {result['language_code']}"
        assert result["confidence"] > 0.5

    def test_detect_language_japanese(self):
        """Test Japanese language detection"""
        result = LanguageDetectionService.detect_language(
            "素早い茶色のキツネが怠け者の犬を飛び越えます"
        )
        
        assert result["success"] is True
        assert result["language_code"] == "ja"
        assert result["language_name"] == "Japanese"
        assert result["confidence"] > 0.5

    def test_detect_language_korean(self):
        """Test Korean language detection"""
        result = LanguageDetectionService.detect_language(
            "빠른 갈색 여우가 게으른 개를 뛰어넘습니다"
        )
        
        assert result["success"] is True
        assert result["language_code"] == "ko"
        assert result["language_name"] == "Korean"
        assert result["confidence"] > 0.5

    def test_detect_language_estonian(self):
        """Test Estonian language detection"""
        result = LanguageDetectionService.detect_language(
            "Kiire pruun rebane hüppab laisa koera üle"
        )
        
        assert result["success"] is True
        assert result["language_code"] == "et"
        assert result["language_name"] == "Estonian"
        assert result["confidence"] > 0.5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
