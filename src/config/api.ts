/**
 * API Configuration
 * Base URL and endpoints for backend communication
 */

export const API_BASE_URL = 'http://localhost:5000/api';

export const API_ENDPOINTS = {
  // OCR Operations
  OCR_UPLOAD: '/ocr/multilingual/upload',
  OCR_PROCESS: (documentId: number) => `/ocr/multilingual/process/${documentId}`,
  OCR_RESULTS: (resultId: number) => `/ocr/results/${resultId}`,
  OCR_VALIDATE: (resultId: number) => `/ocr/results/${resultId}/validate`,
  OCR_ERRORS: (resultId: number) => `/ocr/results/${resultId}/errors`,
  OCR_DOCUMENTS: '/ocr/documents',
  OCR_DELETE: (documentId: number) => `/ocr/documents/${documentId}`,
  
  // Language Support
  OCR_LANGUAGES: '/ocr/multilingual/languages',
  OCR_DETECT_LANGUAGE: '/ocr/multilingual/detect-language',
  
  // Analytics
  ANALYTICS_DASHBOARD: '/analytics/dashboard',
  ANALYTICS_ACCURACY: '/analytics/accuracy',
  ANALYTICS_TRENDS: '/analytics/compliance-trends',
  ANALYTICS_ERRORS: '/analytics/error-analysis',
  ANALYTICS_CONTROLLED: '/analytics/controlled-substances',
};

export const HEALTH_CHECK_URL = 'http://localhost:5000/health';
