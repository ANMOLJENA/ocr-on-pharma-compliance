#!/usr/bin/env python
"""
Language Detection Accuracy Tests

This test suite validates language detection accuracy across various scenarios:
- Single-language documents
- Mixed-language documents
- Short text
- Long text
- Confidence score validation
- Supported language set validation

**Validates: Requirements 3.1, 3.2, 3.5, 3.6, 4.7**
"""

import pytest
from services.language_detection_service import LanguageDetectionService, LANGUAGE_NAMES


class TestSingleLanguageDocuments:
    """Test language detection with single-language documents"""

    def test_english_single_language(self):
        """Test detection of English single-language document"""
        text = """
        The pharmaceutical industry is highly regulated to ensure patient safety.
        All medications must undergo rigorous testing before approval.
        Quality control is essential in manufacturing processes.
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "en"
        assert result["language_name"] == "English"
        assert result["confidence"] > 0.9, "High confidence expected for clear English text"

    def test_french_single_language(self):
        """Test detection of French single-language document"""
        text = """
        L'industrie pharmaceutique est hautement réglementée pour assurer la sécurité des patients.
        Tous les médicaments doivent subir des tests rigoureux avant l'approbation.
        Le contrôle de qualité est essentiel dans les processus de fabrication.
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "fr"
        assert result["language_name"] == "French"
        assert result["confidence"] > 0.9

    def test_spanish_single_language(self):
        """Test detection of Spanish single-language document"""
        text = """
        La industria farmacéutica está altamente regulada para garantizar la seguridad del paciente.
        Todos los medicamentos deben someterse a pruebas rigurosas antes de su aprobación.
        El control de calidad es esencial en los procesos de fabricación.
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "es"
        assert result["language_name"] == "Spanish"
        assert result["confidence"] > 0.9

    def test_german_single_language(self):
        """Test detection of German single-language document"""
        text = """
        Die pharmazeutische Industrie ist stark reguliert, um die Patientensicherheit zu gewährleisten.
        Alle Medikamente müssen vor der Zulassung strengen Tests unterzogen werden.
        Qualitätskontrolle ist in Herstellungsprozessen unerlässlich.
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "de"
        assert result["language_name"] == "German"
        assert result["confidence"] > 0.9

    def test_hindi_single_language(self):
        """Test detection of Hindi single-language document"""
        text = """
        फार्मास्युटिकल उद्योग रोगी सुरक्षा सुनिश्चित करने के लिए अत्यधिक विनियमित है।
        सभी दवाओं को अनुमोदन से पहले कठोर परीक्षण से गुजरना होगा।
        विनिर्माण प्रक्रियाओं में गुणवत्ता नियंत्रण आवश्यक है।
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "hi"
        assert result["language_name"] == "Hindi"
        assert result["confidence"] > 0.9

    def test_tamil_single_language(self):
        """Test detection of Tamil single-language document"""
        text = """
        மருந்துத் தொழில் நோயாளி பாதுகாப்பை உறுதி செய்ய மிகவும் ஒழுங்குபடுத்தப்பட்டுள்ளது।
        அனைத்து மருந்துகளும் ஒப்புதலுக்கு முன் கடுமையான சோதனைக்கு உட்படுத்தப்பட வேண்டும்।
        உற்பத்தி செயல்முறைகளில் தர கட்டுப்பாடு அவசியம்.
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "ta"
        assert result["language_name"] == "Tamil"
        assert result["confidence"] > 0.9

    def test_chinese_single_language(self):
        """Test detection of Chinese single-language document"""
        text = """
        制药行业受到严格监管以确保患者安全。
        所有药物在获得批准之前必须经过严格的测试。
        质量控制在制造过程中至关重要。
        这是一个关于药品安全和质量的重要文档。
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        # Chinese can be detected as zh-cn, zh-tw, or zh
        assert result["language_code"] in ["zh-cn", "zh-tw", "zh"]
        # Chinese detection may have slightly lower confidence due to character complexity
        assert result["confidence"] > 0.8

    def test_japanese_single_language(self):
        """Test detection of Japanese single-language document"""
        text = """
        製薬業界は患者の安全を確保するために厳しく規制されています。
        すべての医薬品は承認前に厳格な試験を受けなければなりません。
        製造プロセスにおいて品質管理は不可欠です。
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "ja"
        assert result["language_name"] == "Japanese"
        assert result["confidence"] > 0.9

    def test_korean_single_language(self):
        """Test detection of Korean single-language document"""
        text = """
        제약 산업은 환자 안전을 보장하기 위해 엄격하게 규제됩니다.
        모든 의약품은 승인 전에 엄격한 테스트를 거쳐야 합니다.
        제조 공정에서 품질 관리는 필수적입니다.
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "ko"
        assert result["language_name"] == "Korean"
        assert result["confidence"] > 0.9

    def test_estonian_single_language(self):
        """Test detection of Estonian single-language document"""
        text = """
        Farmaatsiatööstus on patsiendi ohutuse tagamiseks rangelt reguleeritud.
        Kõik ravimid peavad enne heakskiitmist läbima range testimise.
        Kvaliteedikontroll on tootmisprotsessides hädavajalik.
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "et"
        assert result["language_name"] == "Estonian"
        assert result["confidence"] > 0.8  # Estonian might have slightly lower confidence


class TestMixedLanguageDocuments:
    """Test language detection with mixed-language documents"""

    def test_english_french_mixed(self):
        """Test detection with English and French mixed text"""
        # Predominantly English with some French
        text = """
        The pharmaceutical industry is highly regulated to ensure patient safety.
        All medications must undergo rigorous testing before approval.
        L'industrie pharmaceutique est réglementée.
        Quality control is essential in manufacturing processes.
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        # Should detect the dominant language (English in this case)
        assert result["language_code"] == "en"
        assert 0.0 <= result["confidence"] <= 1.0

    def test_spanish_english_mixed(self):
        """Test detection with Spanish and English mixed text"""
        # Predominantly Spanish with some English
        text = """
        La industria farmacéutica está altamente regulada para garantizar la seguridad del paciente.
        Todos los medicamentos deben someterse a pruebas rigurosas.
        Quality control is essential.
        El control de calidad es esencial en los procesos de fabricación.
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        # Should detect the dominant language (Spanish in this case)
        assert result["language_code"] == "es"
        assert 0.0 <= result["confidence"] <= 1.0

    def test_hindi_english_mixed(self):
        """Test detection with Hindi and English mixed text"""
        # Predominantly Hindi with some English
        text = """
        फार्मास्युटिकल उद्योग रोगी सुरक्षा सुनिश्चित करने के लिए अत्यधिक विनियमित है।
        सभी दवाओं को अनुमोदन से पहले कठोर परीक्षण से गुजरना होगा।
        Quality control is important.
        विनिर्माण प्रक्रियाओं में गुणवत्ता नियंत्रण आवश्यक है।
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        # Should detect the dominant language (Hindi in this case)
        assert result["language_code"] == "hi"
        assert 0.0 <= result["confidence"] <= 1.0


class TestShortTextDetection:
    """Test language detection with short text"""

    def test_short_english_text(self):
        """Test detection with short English text"""
        text = "Pharmaceutical safety"
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "en"
        assert 0.0 <= result["confidence"] <= 1.0

    def test_short_french_text(self):
        """Test detection with short French text"""
        text = "Sécurité pharmaceutique"
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "fr"
        assert 0.0 <= result["confidence"] <= 1.0

    def test_short_spanish_text(self):
        """Test detection with short Spanish text"""
        text = "Seguridad farmacéutica"
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "es"
        assert 0.0 <= result["confidence"] <= 1.0

    def test_short_hindi_text(self):
        """Test detection with short Hindi text"""
        text = "फार्मास्युटिकल सुरक्षा"
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        # Short Hindi text may be misdetected as Nepali (ne) due to similar Devanagari script
        # This is a known limitation of language detection with very short text
        assert result["language_code"] in ["hi", "ne", "mr"], "Should detect Hindi or similar Devanagari script language"
        assert 0.0 <= result["confidence"] <= 1.0

    def test_very_short_text(self):
        """Test detection with very short text (single word)"""
        text = "Hello"
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        # Should still return a valid language code
        assert result["language_code"] in LANGUAGE_NAMES
        assert 0.0 <= result["confidence"] <= 1.0


class TestLongTextDetection:
    """Test language detection with long text"""

    def test_long_english_text(self):
        """Test detection with long English text"""
        text = """
        The pharmaceutical industry plays a crucial role in healthcare by developing, producing, and marketing medications.
        This industry is highly regulated to ensure patient safety and drug efficacy.
        All medications must undergo rigorous testing through clinical trials before receiving approval from regulatory agencies.
        Quality control is essential throughout the manufacturing process to maintain product consistency and safety.
        Pharmaceutical companies must comply with Good Manufacturing Practices (GMP) and other regulatory standards.
        The industry faces challenges including drug development costs, patent expirations, and increasing regulatory requirements.
        Innovation in pharmaceutical research continues to drive the development of new treatments for various diseases.
        Biotechnology and personalized medicine are emerging trends that are transforming the pharmaceutical landscape.
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "en"
        assert result["language_name"] == "English"
        assert result["confidence"] > 0.95, "Very high confidence expected for long clear text"

    def test_long_french_text(self):
        """Test detection with long French text"""
        text = """
        L'industrie pharmaceutique joue un rôle crucial dans les soins de santé en développant, produisant et commercialisant des médicaments.
        Cette industrie est hautement réglementée pour assurer la sécurité des patients et l'efficacité des médicaments.
        Tous les médicaments doivent subir des tests rigoureux par le biais d'essais cliniques avant de recevoir l'approbation des agences de réglementation.
        Le contrôle de qualité est essentiel tout au long du processus de fabrication pour maintenir la cohérence et la sécurité des produits.
        Les entreprises pharmaceutiques doivent se conformer aux bonnes pratiques de fabrication (BPF) et à d'autres normes réglementaires.
        L'industrie fait face à des défis notamment les coûts de développement de médicaments, les expirations de brevets et les exigences réglementaires croissantes.
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "fr"
        assert result["language_name"] == "French"
        assert result["confidence"] > 0.95

    def test_long_hindi_text(self):
        """Test detection with long Hindi text"""
        text = """
        फार्मास्युटिकल उद्योग दवाओं को विकसित, उत्पादन और विपणन करके स्वास्थ्य सेवा में महत्वपूर्ण भूमिका निभाता है।
        यह उद्योग रोगी सुरक्षा और दवा प्रभावकारिता सुनिश्चित करने के लिए अत्यधिक विनियमित है।
        सभी दवाओं को नियामक एजेंसियों से अनुमोदन प्राप्त करने से पहले नैदानिक परीक्षणों के माध्यम से कठोर परीक्षण से गुजरना होगा।
        उत्पाद की स्थिरता और सुरक्षा बनाए रखने के लिए विनिर्माण प्रक्रिया के दौरान गुणवत्ता नियंत्रण आवश्यक है।
        फार्मास्युटिकल कंपनियों को अच्छी विनिर्माण प्रथाओं और अन्य नियामक मानकों का पालन करना चाहिए।
        उद्योग को दवा विकास लागत, पेटेंट समाप्ति और बढ़ती नियामक आवश्यकताओं सहित चुनौतियों का सामना करना पड़ता है।
        """
        result = LanguageDetectionService.detect_language(text)
        
        assert result["success"] is True
        assert result["language_code"] == "hi"
        assert result["language_name"] == "Hindi"
        assert result["confidence"] > 0.95


class TestConfidenceScoreValidation:
    """Test confidence score validation"""

    def test_confidence_score_range(self):
        """Test that confidence scores are always in valid range (0.0-1.0)"""
        test_texts = [
            "The pharmaceutical industry is highly regulated.",
            "L'industrie pharmaceutique est réglementée.",
            "La industria farmacéutica está regulada.",
            "फार्मास्युटिकल उद्योग विनियमित है।",
            "制药行业受到监管。",
            "Hello",  # Very short text
            "A",  # Single character
        ]
        
        for text in test_texts:
            result = LanguageDetectionService.detect_language(text)
            if result["success"]:
                assert 0.0 <= result["confidence"] <= 1.0, f"Confidence score {result['confidence']} out of range for text: {text}"

    def test_high_confidence_for_clear_text(self):
        """Test that clear, unambiguous text has high confidence"""
        clear_texts = {
            "en": "The pharmaceutical industry is highly regulated to ensure patient safety and drug efficacy.",
            "fr": "L'industrie pharmaceutique est hautement réglementée pour assurer la sécurité des patients.",
            "es": "La industria farmacéutica está altamente regulada para garantizar la seguridad del paciente.",
            "de": "Die pharmazeutische Industrie ist stark reguliert, um die Patientensicherheit zu gewährleisten.",
        }
        
        for expected_lang, text in clear_texts.items():
            result = LanguageDetectionService.detect_language(text)
            assert result["success"] is True
            assert result["confidence"] > 0.9, f"Expected high confidence for {expected_lang}, got {result['confidence']}"

    def test_lower_confidence_for_ambiguous_text(self):
        """Test that ambiguous or short text may have lower confidence"""
        ambiguous_texts = [
            "OK",  # Could be multiple languages
            "Test",  # Common word in many languages
            "Hello world",  # Very short
        ]
        
        for text in ambiguous_texts:
            result = LanguageDetectionService.detect_language(text)
            if result["success"]:
                # Just verify it's in valid range, don't enforce high confidence
                assert 0.0 <= result["confidence"] <= 1.0


class TestSupportedLanguageSetValidation:
    """Test that detected languages are in supported set"""

    def test_detected_language_in_supported_set(self):
        """Test that all detected languages are in the supported language set"""
        test_texts = [
            "The pharmaceutical industry is regulated.",
            "L'industrie pharmaceutique est réglementée.",
            "La industria farmacéutica está regulada.",
            "Die pharmazeutische Industrie ist reguliert.",
            "फार्मास्युटिकल उद्योग विनियमित है।",
            "மருந்துத் தொழில் ஒழுங்குபடுத்தப்பட்டுள்ளது।",
            "制药行业受到监管。",
            "製薬業界は規制されています。",
            "제약 산업은 규제됩니다.",
            "Farmaatsiatööstus on reguleeritud.",
        ]
        
        for text in test_texts:
            result = LanguageDetectionService.detect_language(text)
            if result["success"]:
                # Verify language code is in supported set
                assert result["language_code"] in LANGUAGE_NAMES, \
                    f"Detected language '{result['language_code']}' not in supported set"
                # Verify language name matches the code
                assert result["language_name"] == LANGUAGE_NAMES.get(result["language_code"], result["language_code"]), \
                    f"Language name mismatch for code '{result['language_code']}'"

    def test_all_supported_languages_have_names(self):
        """Test that all supported language codes have corresponding names"""
        # This test verifies the LANGUAGE_NAMES mapping is complete
        from services.translation_service import TranslationService
        
        for lang_code in TranslationService.LANGUAGE_CODES.values():
            # Some codes might be variants (like zh-cn), so we check the base code
            base_code = lang_code.split('-')[0]
            assert base_code in LANGUAGE_NAMES or lang_code in LANGUAGE_NAMES, \
                f"Language code '{lang_code}' missing from LANGUAGE_NAMES mapping"

    def test_language_name_consistency(self):
        """Test that language names are consistent across detections"""
        # Test the same language multiple times to ensure consistency
        english_texts = [
            "The pharmaceutical industry is regulated.",
            "Quality control is essential in manufacturing.",
            "All medications must undergo rigorous testing.",
        ]
        
        detected_names = []
        for text in english_texts:
            result = LanguageDetectionService.detect_language(text)
            if result["success"] and result["language_code"] == "en":
                detected_names.append(result["language_name"])
        
        # All English texts should have the same language name
        assert len(set(detected_names)) == 1, "Inconsistent language names for English"
        assert detected_names[0] == "English"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
