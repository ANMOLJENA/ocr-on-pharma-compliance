/**
 * OCR Service Tests
 * Tests for language response parsing and error handling
 */

import { describe, it, expect } from 'vitest';
import { ocrService } from './ocr.service';
import type { UploadResponse, OCRResult } from '@/types/api';

describe('OCRService', () => {
  const mockOCRResult: OCRResult = {
    id: 1,
    document_id: 1,
    extracted_text: 'Sample extracted text',
    confidence_score: 0.95,
    processing_time: 2.5,
    processed_date: '2024-01-29',
    drug_name: 'Aspirin',
    batch_number: 'BATCH123',
    expiry_date: '2025-12-31',
    manufacturer: 'Pharma Corp',
    controlled_substance: false,
  };

  describe('parseLanguageResponse', () => {
    it('should parse successful response with translation', () => {
      const response: UploadResponse = {
        success: true,
        document_id: 1,
        ocr_result_id: 1,
        data: mockOCRResult,
        detected_language: 'Hindi',
        original_language: 'Hindi',
        translated: true,
        original_text: 'Original Hindi text',
        translated_text: 'Translated English text',
      };

      const result = ocrService.parseLanguageResponse(response);

      expect(result.success).toBe(true);
      expect(result.languageInfo.detectedLanguage).toBe('Hindi');
      expect(result.languageInfo.originalLanguage).toBe('Hindi');
      expect(result.languageInfo.isTranslated).toBe(true);
      expect(result.languageInfo.originalText).toBe('Original Hindi text');
      expect(result.languageInfo.translatedText).toBe('Translated English text');
    });

    it('should parse response without translation', () => {
      const response: UploadResponse = {
        success: true,
        document_id: 1,
        ocr_result_id: 1,
        data: mockOCRResult,
        detected_language: 'English',
        original_language: 'English',
        translated: false,
      };

      const result = ocrService.parseLanguageResponse(response);

      expect(result.success).toBe(true);
      expect(result.languageInfo.detectedLanguage).toBe('English');
      expect(result.languageInfo.originalLanguage).toBe('English');
      expect(result.languageInfo.isTranslated).toBe(false);
      expect(result.languageInfo.originalText).toBe('Sample extracted text');
      expect(result.languageInfo.translatedText).toBeUndefined();
    });

    it('should handle response with missing language fields', () => {
      const response: UploadResponse = {
        success: true,
        document_id: 1,
        ocr_result_id: 1,
        data: mockOCRResult,
      };

      const result = ocrService.parseLanguageResponse(response);

      expect(result.success).toBe(true);
      expect(result.languageInfo.detectedLanguage).toBe('English');
      expect(result.languageInfo.originalLanguage).toBe('English');
      expect(result.languageInfo.isTranslated).toBe(false);
    });

    it('should handle failed response', () => {
      const response: UploadResponse = {
        success: false,
        document_id: 0,
        ocr_result_id: 0,
        data: mockOCRResult,
      };

      const result = ocrService.parseLanguageResponse(response);

      expect(result.success).toBe(false);
      expect(result.error).toBe('Upload response was not successful');
    });

    it('should handle response with missing data', () => {
      const response: UploadResponse = {
        success: true,
        document_id: 1,
        ocr_result_id: 1,
        data: undefined as any,
      };

      const result = ocrService.parseLanguageResponse(response);

      expect(result.success).toBe(false);
      expect(result.error).toBe('No OCR data in response');
    });
  });

  describe('handleLanguageDetectionError', () => {
    it('should return fallback language info on error', () => {
      const result = ocrService.handleLanguageDetectionError(
        mockOCRResult,
        'Language detection service unavailable'
      );

      expect(result.success).toBe(true);
      expect(result.languageInfo.detectedLanguage).toBe('Unknown');
      expect(result.languageInfo.originalLanguage).toBe('Unknown');
      expect(result.languageInfo.isTranslated).toBe(false);
      expect(result.languageInfo.originalText).toBe('Sample extracted text');
      expect(result.error).toContain('Language detection failed');
    });
  });

  describe('extractLanguageMetadata', () => {
    it('should extract language metadata from OCR result with metadata', () => {
      const ocrResultWithMetadata = {
        ...mockOCRResult,
        metadata: {
          detected_language: 'Tamil',
          original_language: 'Tamil',
          translated: true,
          original_text: 'Original Tamil text',
          translated_text: 'Translated English text',
        },
      } as any;

      const result = ocrService.extractLanguageMetadata(ocrResultWithMetadata);

      expect(result.detectedLanguage).toBe('Tamil');
      expect(result.originalLanguage).toBe('Tamil');
      expect(result.isTranslated).toBe(true);
      expect(result.originalText).toBe('Original Tamil text');
      expect(result.translatedText).toBe('Translated English text');
    });

    it('should return default language info when metadata is missing', () => {
      const result = ocrService.extractLanguageMetadata(mockOCRResult);

      expect(result.detectedLanguage).toBe('English');
      expect(result.originalLanguage).toBe('English');
      expect(result.isTranslated).toBe(false);
      expect(result.originalText).toBe('Sample extracted text');
      expect(result.translatedText).toBeUndefined();
    });
  });

  describe('validateLanguageResponse', () => {
    it('should validate successful response with translation', () => {
      const response: UploadResponse = {
        success: true,
        document_id: 1,
        ocr_result_id: 1,
        data: mockOCRResult,
        detected_language: 'Hindi',
        original_language: 'Hindi',
        translated: true,
        original_text: 'Original text',
        translated_text: 'Translated text',
      };

      const validation = ocrService.validateLanguageResponse(response);

      expect(validation.valid).toBe(true);
      expect(validation.errors).toHaveLength(0);
    });

    it('should detect missing original_text when translated', () => {
      const response: UploadResponse = {
        success: true,
        document_id: 1,
        ocr_result_id: 1,
        data: mockOCRResult,
        detected_language: 'Hindi',
        original_language: 'Hindi',
        translated: true,
        translated_text: 'Translated text',
      };

      const validation = ocrService.validateLanguageResponse(response);

      expect(validation.valid).toBe(false);
      expect(validation.errors).toContain(
        'Translation indicated but original_text is missing'
      );
    });

    it('should detect missing translated_text when translated', () => {
      const response: UploadResponse = {
        success: true,
        document_id: 1,
        ocr_result_id: 1,
        data: mockOCRResult,
        detected_language: 'Hindi',
        original_language: 'Hindi',
        translated: true,
        original_text: 'Original text',
      };

      const validation = ocrService.validateLanguageResponse(response);

      expect(validation.valid).toBe(false);
      expect(validation.errors).toContain(
        'Translation indicated but translated_text is missing'
      );
    });

    it('should detect missing detected_language', () => {
      const response: UploadResponse = {
        success: true,
        document_id: 1,
        ocr_result_id: 1,
        data: mockOCRResult,
        original_language: 'Hindi',
        translated: false,
      };

      const validation = ocrService.validateLanguageResponse(response);

      expect(validation.valid).toBe(false);
      expect(validation.errors).toContain('detected_language is missing');
    });

    it('should detect missing original_language', () => {
      const response: UploadResponse = {
        success: true,
        document_id: 1,
        ocr_result_id: 1,
        data: mockOCRResult,
        detected_language: 'Hindi',
        translated: false,
      };

      const validation = ocrService.validateLanguageResponse(response);

      expect(validation.valid).toBe(false);
      expect(validation.errors).toContain('original_language is missing');
    });

    it('should detect failed response', () => {
      const response: UploadResponse = {
        success: false,
        document_id: 0,
        ocr_result_id: 0,
        data: mockOCRResult,
      };

      const validation = ocrService.validateLanguageResponse(response);

      expect(validation.valid).toBe(false);
      expect(validation.errors).toContain('Response success flag is false');
    });

    it('should detect missing data', () => {
      const response: UploadResponse = {
        success: true,
        document_id: 1,
        ocr_result_id: 1,
        data: undefined as any,
      };

      const validation = ocrService.validateLanguageResponse(response);

      expect(validation.valid).toBe(false);
      expect(validation.errors).toContain('No OCR data in response');
    });
  });
});
