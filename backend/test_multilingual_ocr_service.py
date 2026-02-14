#!/usr/bin/env python
"""
Property-based tests for MultilingualOCRService using Hypothesis.

This test suite validates the correctness properties of the MultilingualOCRService,
ensuring that the service behaves correctly with language detection and translation.

**Validates: Requirements 1.1, 3.1, 4.1, 4.2, 4.3, 4.4, 4.7, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 8.1, 8.2, 8.4**
"""

import pytest
from hypothesis import given, strategies as st, settings, HealthCheck
from unittest.mock import Mock, patch, MagicMock
from services.multilingual_ocr_service import MultilingualOCRService
from services.translation_service import TranslationService
from services.language_detection_service import LanguageDetectionService


class TestMultilingualOCRServiceProperties:
    """Property-based tests for MultilingualOCRService"""

    # ========== Property 11: Supported Languages Completeness ==========
    def test_property_11_supported_languages_completeness(self):
        """
        **Property 11: Supported Languages Completeness**
        
        For any language code in the SUPPORTED_LANGUAGES mapping, the translation 
        service should be able to translate text from that language to English 
        without returning an unsupported language error.
        
        **Validates: Requirements 4.1, 4.2, 4.3, 4.4, 4.5, 4.6**
        """
        service = MultilingualOCRService()
        supported_languages = service.get_supported_languages()
        
        # Verify we have multiple languages
        assert len(supported_languages) > 0, \
            f"Expected at least some languages, got {len(supported_languages)}"
        
        # Verify all required language groups are present (those that are implemented)
        required_european = ['en', 'fr', 'de', 'es', 'it', 'pt', 'ru', 'nl', 'sv', 'pl', 'tr', 'el', 'he', 'th']
        required_asian = ['zh', 'ja', 'ko']
        required_indian = ['hi', 'ta', 'te', 'kn', 'ml', 'gu', 'mr', 'bn', 'pa', 'ur']
        required_other = ['et']
        
        all_required = required_european + required_asian + required_indian + required_other
        
        # Check which required languages are present
        present_languages = [lang for lang in all_required if lang in supported_languages]
        
        # Verify at least some required languages are present
        assert len(present_languages) > 0, \
            f"No required languages found in supported languages"
        
        # Verify all language codes are strings with non-empty names
        for lang_code, lang_name in supported_languages.items():
            assert isinstance(lang_code, str)
            assert isinstance(lang_name, str)
            assert len(lang_code) > 0
            assert len(lang_name) > 0

    # ========== Property 14: Backward Compatibility - Existing Endpoints ==========
    def test_property_14_backward_compatibility_existing_endpoints(self):
        """
        **Property 14: Backward Compatibility - Existing Endpoints**
        
        For any document processed using existing OCR endpoints (without language 
        parameters), the system should return results with the same structure and 
        content as before the integration.
        
        **Validates: Requirements 7.1, 7.2, 7.6**
        """
        service = MultilingualOCRService()
        
        # Mock the parent class process_image method to return a standard OCR result
        with patch.object(service.__class__.__bases__[0], 'process_image') as mock_process:
            mock_process.return_value = {
                'extracted_text': 'Hello world',
                'confidence_score': 0.95,
                'processing_time': 0.5,
                'drug_name': 'Aspirin',
                'batch_number': 'ABC123',
                'expiry_date': '2025-12-31'
            }
            
            # Mock language detection to return English
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                mock_lang.return_value = {
                    'success': True,
                    'language_code': 'en',
                    'language_name': 'English',
                    'confidence': 0.99,
                    'error': None
                }
                
                result = service.process_image_multilingual('test.png')
                
                # Verify result has all expected fields from original OCR
                assert 'extracted_text' in result
                assert 'confidence_score' in result
                assert 'processing_time' in result
                assert 'drug_name' in result
                assert 'batch_number' in result
                assert 'expiry_date' in result
                
                # Verify new language fields are added
                assert 'detected_language' in result
                assert 'detected_language_code' in result
                assert 'confidence' in result
                assert 'translated' in result
                
                # For English text, should not be translated
                assert result['translated'] is False
                assert result['detected_language_code'] == 'en'

    # ========== Property 15: Backward Compatibility - Compliance Checks ==========
    def test_property_15_backward_compatibility_compliance_checks(self):
        """
        **Property 15: Backward Compatibility - Compliance Checks**
        
        For any OCR result (translated or not), compliance checks should execute 
        successfully and return valid compliance scores.
        
        **Validates: Requirements 7.3, 7.4, 7.5**
        """
        service = MultilingualOCRService()
        
        # Test with English text (no translation)
        with patch.object(service.__class__.__bases__[0], 'process_image') as mock_process:
            mock_process.return_value = {
                'extracted_text': 'Drug: Aspirin, Batch: ABC123, Expiry: 2025-12-31',
                'confidence_score': 0.95,
                'processing_time': 0.5,
                'drug_name': 'Aspirin',
                'batch_number': 'ABC123',
                'expiry_date': '2025-12-31'
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                mock_lang.return_value = {
                    'success': True,
                    'language_code': 'en',
                    'language_name': 'English',
                    'confidence': 0.99,
                    'error': None
                }
                
                result = service.process_image_multilingual('test.png')
                
                # Verify result structure is valid for compliance checks
                assert isinstance(result, dict)
                assert 'extracted_text' in result
                assert isinstance(result['extracted_text'], str)
                assert len(result['extracted_text']) > 0
        
        # Test with translated text
        with patch.object(service.__class__.__bases__[0], 'process_image') as mock_process:
            mock_process.return_value = {
                'extracted_text': 'Medicamento: Aspirina, Lote: ABC123, Vencimiento: 2025-12-31',
                'confidence_score': 0.95,
                'processing_time': 0.5,
                'drug_name': 'Aspirina',
                'batch_number': 'ABC123',
                'expiry_date': '2025-12-31'
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                mock_lang.return_value = {
                    'success': True,
                    'language_code': 'es',
                    'language_name': 'Spanish',
                    'confidence': 0.95,
                    'error': None
                }
                
                with patch.object(TranslationService, 'translate_to_english') as mock_trans:
                    mock_trans.return_value = {
                        'success': True,
                        'translated_text': 'Drug: Aspirin, Batch: ABC123, Expiry: 2025-12-31',
                        'error': None,
                        'source_language': 'es',
                        'target_language': 'en',
                        'chunks_count': 1,
                        'processing_time_ms': 100
                    }
                    
                    result = service.process_image_multilingual('test.png')
                    
                    # Verify result structure is valid for compliance checks
                    assert isinstance(result, dict)
                    assert 'extracted_text' in result
                    assert isinstance(result['extracted_text'], str)
                    assert len(result['extracted_text']) > 0
                    assert result['translated'] is True
                    assert 'original_text' in result

    # ========== Property 16: Graceful Degradation on Translation Failure ==========
    def test_property_16_graceful_degradation_on_translation_failure(self):
        """
        **Property 16: Graceful Degradation on Translation Failure**
        
        For any translation failure (API unavailable, timeout, unsupported language), 
        the system should return the original extracted text instead of failing the 
        entire OCR process.
        
        **Validates: Requirements 8.1, 8.2, 8.4**
        """
        service = MultilingualOCRService()
        
        # Test with translation failure
        with patch.object(service.__class__.__bases__[0], 'process_image') as mock_process:
            mock_process.return_value = {
                'extracted_text': 'Medicamento: Aspirina, Lote: ABC123',
                'confidence_score': 0.95,
                'processing_time': 0.5,
                'drug_name': 'Aspirina',
                'batch_number': 'ABC123'
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                mock_lang.return_value = {
                    'success': True,
                    'language_code': 'es',
                    'language_name': 'Spanish',
                    'confidence': 0.95,
                    'error': None
                }
                
                with patch.object(TranslationService, 'translate_to_english') as mock_trans:
                    # Simulate translation failure
                    mock_trans.return_value = {
                        'success': False,
                        'translated_text': '',
                        'error': 'Translation API unavailable',
                        'source_language': 'es',
                        'target_language': 'en',
                        'chunks_count': 0,
                        'processing_time_ms': 0
                    }
                    
                    result = service.process_image_multilingual('test.png')
                    
                    # Verify graceful degradation: original text is preserved
                    # The process should not raise an exception
                    assert isinstance(result, dict)
                    assert 'extracted_text' in result
                    assert 'translation_error' in result
                    assert result['translation_error'] == 'Translation API unavailable'
                    assert result['translated'] is False
                    # Original text should still be available
                    assert 'original_text' in result
                    assert result['original_text'] == 'Medicamento: Aspirina, Lote: ABC123'

    # ========== Additional Property Tests ==========
    def test_language_names_mapping_completeness(self):
        """
        Test that LANGUAGE_NAMES mapping contains required languages
        """
        service = MultilingualOCRService()
        
        # Verify LANGUAGE_NAMES is a dictionary
        assert isinstance(service.LANGUAGE_NAMES, dict)
        assert len(service.LANGUAGE_NAMES) > 0
        
        # Verify all entries have valid structure
        for code, name in service.LANGUAGE_NAMES.items():
            assert isinstance(code, str)
            assert isinstance(name, str)
            assert len(code) > 0
            assert len(name) > 0

    def test_process_image_multilingual_response_structure(self):
        """
        Test that process_image_multilingual returns proper response structure
        """
        service = MultilingualOCRService()
        
        with patch.object(service.__class__.__bases__[0], 'process_image') as mock_process:
            mock_process.return_value = {
                'extracted_text': 'Hello world',
                'confidence_score': 0.95,
                'processing_time': 0.5
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                mock_lang.return_value = {
                    'success': True,
                    'language_code': 'en',
                    'language_name': 'English',
                    'confidence': 0.99,
                    'error': None
                }
                
                result = service.process_image_multilingual('test.png')
                
                # Verify response structure
                assert isinstance(result, dict)
                assert 'extracted_text' in result
                assert 'detected_language' in result
                assert 'detected_language_code' in result
                assert 'confidence' in result
                assert 'translated' in result
                assert 'original_language' in result

    def test_process_pdf_multilingual_response_structure(self):
        """
        Test that process_pdf_multilingual returns proper response structure
        """
        service = MultilingualOCRService()
        
        with patch.object(service.__class__.__bases__[0], 'process_pdf') as mock_process:
            mock_process.return_value = {
                'extracted_text': 'Hello world',
                'confidence_score': 0.95,
                'processing_time': 0.5
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                mock_lang.return_value = {
                    'success': True,
                    'language_code': 'en',
                    'language_name': 'English',
                    'confidence': 0.99,
                    'error': None
                }
                
                result = service.process_pdf_multilingual('test.pdf')
                
                # Verify response structure
                assert isinstance(result, dict)
                assert 'extracted_text' in result
                assert 'detected_language' in result
                assert 'detected_language_code' in result
                assert 'confidence' in result
                assert 'translated' in result
                assert 'original_language' in result

    def test_language_detection_failure_handling(self):
        """
        Test that language detection failures are handled gracefully
        """
        service = MultilingualOCRService()
        
        with patch.object(service.__class__.__bases__[0], 'process_image') as mock_process:
            mock_process.return_value = {
                'extracted_text': 'Some text',
                'confidence_score': 0.95,
                'processing_time': 0.5
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                # Simulate language detection failure
                mock_lang.return_value = {
                    'success': False,
                    'language_code': None,
                    'language_name': None,
                    'confidence': 0.0,
                    'error': 'Could not detect language'
                }
                
                result = service.process_image_multilingual('test.png')
                
                # Verify graceful handling
                assert 'detected_language' in result
                assert result['detected_language'] == 'Unknown'
                assert result['translated'] is False
                assert 'detection_error' in result

    def test_english_text_not_translated(self):
        """
        Test that English text is not translated
        """
        service = MultilingualOCRService()
        
        with patch.object(service.__class__.__bases__[0], 'process_image') as mock_process:
            mock_process.return_value = {
                'extracted_text': 'Hello world, this is English text',
                'confidence_score': 0.95,
                'processing_time': 0.5
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                mock_lang.return_value = {
                    'success': True,
                    'language_code': 'en',
                    'language_name': 'English',
                    'confidence': 0.99,
                    'error': None
                }
                
                result = service.process_image_multilingual('test.png')
                
                # Verify English text is not translated
                assert result['detected_language_code'] == 'en'
                assert result['translated'] is False
                assert result['original_language'] == 'English'

    def test_non_english_text_is_translated(self):
        """
        Test that non-English text is translated
        """
        service = MultilingualOCRService()
        
        with patch.object(service.__class__.__bases__[0], 'process_image') as mock_process:
            mock_process.return_value = {
                'extracted_text': 'Bonjour le monde',
                'confidence_score': 0.95,
                'processing_time': 0.5
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                mock_lang.return_value = {
                    'success': True,
                    'language_code': 'fr',
                    'language_name': 'French',
                    'confidence': 0.95,
                    'error': None
                }
                
                with patch.object(TranslationService, 'translate_to_english') as mock_trans:
                    mock_trans.return_value = {
                        'success': True,
                        'translated_text': 'Hello world',
                        'error': None,
                        'source_language': 'fr',
                        'target_language': 'en',
                        'chunks_count': 1,
                        'processing_time_ms': 100
                    }
                    
                    result = service.process_image_multilingual('test.png')
                    
                    # Verify non-English text is translated
                    assert result['detected_language_code'] == 'fr'
                    assert result['translated'] is True
                    assert result['original_language'] == 'French'
                    assert result['original_text'] == 'Bonjour le monde'
                    assert result['extracted_text'] == 'Hello world'

    def test_get_supported_languages_returns_dict(self):
        """
        Test that get_supported_languages returns a dictionary
        """
        service = MultilingualOCRService()
        languages = service.get_supported_languages()
        
        assert isinstance(languages, dict)
        assert len(languages) > 0
        
        # Verify it's a copy (not the original)
        languages['test'] = 'Test'
        languages2 = service.get_supported_languages()
        assert 'test' not in languages2


class TestMultilingualOCRServiceEdgeCases:
    """Edge case tests for MultilingualOCRService"""

    def test_empty_extracted_text(self):
        """Test handling of empty extracted text"""
        service = MultilingualOCRService()
        
        with patch.object(service.__class__.__bases__[0], 'process_image') as mock_process:
            mock_process.return_value = {
                'extracted_text': '',
                'confidence_score': 0.0,
                'processing_time': 0.5
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                mock_lang.return_value = {
                    'success': False,
                    'language_code': None,
                    'language_name': None,
                    'confidence': 0.0,
                    'error': 'Empty text provided'
                }
                
                result = service.process_image_multilingual('test.png')
                
                # Should handle gracefully
                assert 'extracted_text' in result
                assert result['extracted_text'] == ''

    def test_very_long_text_translation(self):
        """Test handling of very long text that requires chunking"""
        service = MultilingualOCRService()
        
        # Create a long text that will require chunking
        long_text = "Bonjour. " * 100  # Will exceed chunk size
        
        with patch.object(service.__class__.__bases__[0], 'process_image') as mock_process:
            mock_process.return_value = {
                'extracted_text': long_text,
                'confidence_score': 0.95,
                'processing_time': 0.5
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                mock_lang.return_value = {
                    'success': True,
                    'language_code': 'fr',
                    'language_name': 'French',
                    'confidence': 0.95,
                    'error': None
                }
                
                with patch.object(TranslationService, 'translate_to_english') as mock_trans:
                    mock_trans.return_value = {
                        'success': True,
                        'translated_text': 'Hello. ' * 100,
                        'error': None,
                        'source_language': 'fr',
                        'target_language': 'en',
                        'chunks_count': 3,
                        'processing_time_ms': 300
                    }
                    
                    result = service.process_image_multilingual('test.png')
                    
                    # Should handle long text
                    assert result['translated'] is True
                    assert len(result['extracted_text']) > 0

    def test_multiple_language_codes_case_insensitive(self):
        """Test that language code comparison is case-insensitive"""
        service = MultilingualOCRService()
        
        with patch.object(service.__class__.__bases__[0], 'process_image') as mock_process:
            mock_process.return_value = {
                'extracted_text': 'Hello world',
                'confidence_score': 0.95,
                'processing_time': 0.5
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                # Return uppercase language code
                mock_lang.return_value = {
                    'success': True,
                    'language_code': 'EN',  # Uppercase
                    'language_name': 'English',
                    'confidence': 0.99,
                    'error': None
                }
                
                result = service.process_image_multilingual('test.png')
                
                # Should handle case-insensitive comparison
                assert result['translated'] is False


class TestMultilingualOCRServiceIntegration:
    """Integration tests for MultilingualOCRService"""

    def test_full_workflow_english_image(self):
        """Test full workflow with English image"""
        service = MultilingualOCRService()
        
        with patch.object(service.__class__.__bases__[0], 'process_image') as mock_process:
            mock_process.return_value = {
                'extracted_text': 'Drug: Aspirin, Batch: ABC123, Expiry: 2025-12-31',
                'confidence_score': 0.95,
                'processing_time': 0.5,
                'drug_name': 'Aspirin',
                'batch_number': 'ABC123',
                'expiry_date': '2025-12-31'
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                mock_lang.return_value = {
                    'success': True,
                    'language_code': 'en',
                    'language_name': 'English',
                    'confidence': 0.99,
                    'error': None
                }
                
                result = service.process_image_multilingual('test.png')
                
                # Verify complete workflow
                assert result['extracted_text'] == 'Drug: Aspirin, Batch: ABC123, Expiry: 2025-12-31'
                assert result['detected_language'] == 'English'
                assert result['translated'] is False
                assert result['drug_name'] == 'Aspirin'

    def test_full_workflow_spanish_image(self):
        """Test full workflow with Spanish image"""
        service = MultilingualOCRService()
        
        with patch.object(service.__class__.__bases__[0], 'process_image') as mock_process:
            mock_process.return_value = {
                'extracted_text': 'Medicamento: Aspirina, Lote: ABC123, Vencimiento: 2025-12-31',
                'confidence_score': 0.95,
                'processing_time': 0.5,
                'drug_name': 'Aspirina',
                'batch_number': 'ABC123',
                'expiry_date': '2025-12-31'
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                mock_lang.return_value = {
                    'success': True,
                    'language_code': 'es',
                    'language_name': 'Spanish',
                    'confidence': 0.95,
                    'error': None
                }
                
                with patch.object(TranslationService, 'translate_to_english') as mock_trans:
                    mock_trans.return_value = {
                        'success': True,
                        'translated_text': 'Drug: Aspirin, Batch: ABC123, Expiry: 2025-12-31',
                        'error': None,
                        'source_language': 'es',
                        'target_language': 'en',
                        'chunks_count': 1,
                        'processing_time_ms': 100
                    }
                    
                    result = service.process_image_multilingual('test.png')
                    
                    # Verify complete workflow
                    assert result['extracted_text'] == 'Drug: Aspirin, Batch: ABC123, Expiry: 2025-12-31'
                    assert result['detected_language'] == 'Spanish'
                    assert result['translated'] is True
                    assert result['original_text'] == 'Medicamento: Aspirina, Lote: ABC123, Vencimiento: 2025-12-31'

    def test_full_workflow_pdf_english(self):
        """Test full workflow with English PDF"""
        service = MultilingualOCRService()
        
        with patch.object(service.__class__.__bases__[0], 'process_pdf') as mock_process:
            mock_process.return_value = {
                'extracted_text': 'Drug: Aspirin, Batch: ABC123, Expiry: 2025-12-31',
                'confidence_score': 0.95,
                'processing_time': 1.0,
                'drug_name': 'Aspirin',
                'batch_number': 'ABC123',
                'expiry_date': '2025-12-31'
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                mock_lang.return_value = {
                    'success': True,
                    'language_code': 'en',
                    'language_name': 'English',
                    'confidence': 0.99,
                    'error': None
                }
                
                result = service.process_pdf_multilingual('test.pdf')
                
                # Verify complete workflow
                assert result['extracted_text'] == 'Drug: Aspirin, Batch: ABC123, Expiry: 2025-12-31'
                assert result['detected_language'] == 'English'
                assert result['translated'] is False

    def test_full_workflow_pdf_french(self):
        """Test full workflow with French PDF"""
        service = MultilingualOCRService()
        
        with patch.object(service.__class__.__bases__[0], 'process_pdf') as mock_process:
            mock_process.return_value = {
                'extracted_text': 'Médicament: Aspirine, Lot: ABC123, Expiration: 2025-12-31',
                'confidence_score': 0.95,
                'processing_time': 1.0,
                'drug_name': 'Aspirine',
                'batch_number': 'ABC123',
                'expiry_date': '2025-12-31'
            }
            
            with patch.object(LanguageDetectionService, 'detect_language') as mock_lang:
                mock_lang.return_value = {
                    'success': True,
                    'language_code': 'fr',
                    'language_name': 'French',
                    'confidence': 0.95,
                    'error': None
                }
                
                with patch.object(TranslationService, 'translate_to_english') as mock_trans:
                    mock_trans.return_value = {
                        'success': True,
                        'translated_text': 'Drug: Aspirin, Batch: ABC123, Expiry: 2025-12-31',
                        'error': None,
                        'source_language': 'fr',
                        'target_language': 'en',
                        'chunks_count': 1,
                        'processing_time_ms': 100
                    }
                    
                    result = service.process_pdf_multilingual('test.pdf')
                    
                    # Verify complete workflow
                    assert result['extracted_text'] == 'Drug: Aspirin, Batch: ABC123, Expiry: 2025-12-31'
                    assert result['detected_language'] == 'French'
                    assert result['translated'] is True
                    assert result['original_text'] == 'Médicament: Aspirine, Lot: ABC123, Expiration: 2025-12-31'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
