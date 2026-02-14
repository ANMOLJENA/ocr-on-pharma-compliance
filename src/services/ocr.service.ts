/**
 * OCR Service
 * Handles OCR-specific operations including language response parsing
 */

import type { UploadResponse, OCRResult } from '@/types/api';

export interface LanguageInfo {
  detectedLanguage: string;
  originalLanguage: string;
  isTranslated: boolean;
  originalText: string;
  translatedText?: string;
}

export interface ParsedOCRResponse {
  success: boolean;
  ocrResult: OCRResult;
  languageInfo: LanguageInfo;
  error?: string;
}

class OCRService {
  /**
   * Parse language information from upload response
   * Extracts detected_language, original_language, translated status, and text variants
   */
  parseLanguageResponse(response: UploadResponse): ParsedOCRResponse {
    if (!response.success) {
      return {
        success: false,
        ocrResult: response.data,
        languageInfo: {
          detectedLanguage: 'Unknown',
          originalLanguage: 'Unknown',
          isTranslated: false,
          originalText: '',
        },
        error: 'Upload response was not successful',
      };
    }

    if (!response.data) {
      return {
        success: false,
        ocrResult: {} as OCRResult,
        languageInfo: {
          detectedLanguage: 'Unknown',
          originalLanguage: 'Unknown',
          isTranslated: false,
          originalText: '',
        },
        error: 'No OCR data in response',
      };
    }

    // Extract language information from response
    const detectedLanguage = response.detected_language || 'English';
    const originalLanguage = response.original_language || 'English';
    const isTranslated = response.translated || false;

    // Determine which text to use as original
    let originalText = '';
    let translatedText: string | undefined;

    if (isTranslated && response.original_text) {
      // If translation occurred, use the provided original text
      originalText = response.original_text;
      translatedText = response.translated_text;
    } else {
      // If no translation, use the extracted text as original
      originalText = response.data.extracted_text || '';
    }

    const languageInfo: LanguageInfo = {
      detectedLanguage,
      originalLanguage,
      isTranslated,
      originalText,
      translatedText,
    };

    return {
      success: true,
      ocrResult: response.data,
      languageInfo,
    };
  }

  /**
   * Handle language detection errors gracefully
   * Returns a default language info structure when detection fails
   */
  handleLanguageDetectionError(
    ocrResult: OCRResult,
    error: string
  ): ParsedOCRResponse {
    return {
      success: true,
      ocrResult,
      languageInfo: {
        detectedLanguage: 'Unknown',
        originalLanguage: 'Unknown',
        isTranslated: false,
        originalText: ocrResult.extracted_text || '',
      },
      error: `Language detection failed: ${error}`,
    };
  }

  /**
   * Extract language metadata from OCR result
   * Useful for retrieving language info from stored results
   */
  extractLanguageMetadata(
    ocrResult: OCRResult
  ): LanguageInfo {
    // Check if metadata contains language information
    const metadata = (ocrResult as any).metadata;

    if (metadata && typeof metadata === 'object') {
      return {
        detectedLanguage: metadata.detected_language || 'English',
        originalLanguage: metadata.original_language || 'English',
        isTranslated: metadata.translated || false,
        originalText: metadata.original_text || ocrResult.extracted_text || '',
        translatedText: metadata.translated_text,
      };
    }

    // Fallback to default if no metadata
    return {
      detectedLanguage: 'English',
      originalLanguage: 'English',
      isTranslated: false,
      originalText: ocrResult.extracted_text || '',
    };
  }

  /**
   * Validate language response structure
   * Ensures all required fields are present
   */
  validateLanguageResponse(response: UploadResponse): {
    valid: boolean;
    errors: string[];
  } {
    const errors: string[] = [];

    if (!response.success) {
      errors.push('Response success flag is false');
    }

    if (!response.data) {
      errors.push('No OCR data in response');
    }

    if (response.translated && !response.original_text) {
      errors.push('Translation indicated but original_text is missing');
    }

    if (response.translated && !response.translated_text) {
      errors.push('Translation indicated but translated_text is missing');
    }

    if (!response.detected_language) {
      errors.push('detected_language is missing');
    }

    if (!response.original_language) {
      errors.push('original_language is missing');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }
}

// Export singleton instance
export const ocrService = new OCRService();
export default ocrService;
