/**
 * API Service
 * Handles all HTTP requests to the backend
 */

import { API_BASE_URL, API_ENDPOINTS, HEALTH_CHECK_URL } from '@/config/api';
import type {
  ApiResponse,
  UploadResponse,
  OCRResult,
  ValidationResponse,
  ErrorDetectionResponse,
  Document,
  DashboardStats,
  AccuracyMetrics,
  ComplianceTrends,
  ErrorAnalysis,
  ControlledSubstancesStats,
} from '@/types/api';

class ApiService {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  /**
   * Generic fetch wrapper with error handling
   */
  private async fetchApi<T>(
    endpoint: string,
    options?: RequestInit
  ): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          ...options?.headers,
        },
      });

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.error || `HTTP error! status: ${response.status}`,
        };
      }

      return data;
    } catch (error) {
      console.error('API Error:', error);
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
      };
    }
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string; message: string }> {
    try {
      const response = await fetch(HEALTH_CHECK_URL);
      return await response.json();
    } catch (error) {
      throw new Error('Backend server is not responding');
    }
  }

  // ==================== OCR Operations ====================

  /**
   * Upload and process a document
   */
  async uploadDocument(file: File): Promise<UploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(`${this.baseUrl}${API_ENDPOINTS.OCR_UPLOAD}`, {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Upload failed');
      }

      return data;
    } catch (error) {
      throw new Error(error instanceof Error ? error.message : 'Upload failed');
    }
  }

  /**
   * Reprocess an existing document
   */
  async processDocument(documentId: number): Promise<ApiResponse<OCRResult>> {
    return this.fetchApi<OCRResult>(API_ENDPOINTS.OCR_PROCESS(documentId), {
      method: 'POST',
    });
  }

  /**
   * Get OCR result by ID
   */
  async getOCRResult(resultId: number): Promise<ApiResponse<OCRResult>> {
    return this.fetchApi<OCRResult>(API_ENDPOINTS.OCR_RESULTS(resultId));
  }

  /**
   * Validate OCR result for compliance
   */
  async validateResult(resultId: number): Promise<ValidationResponse> {
    try {
      const response = await fetch(
        `${this.baseUrl}${API_ENDPOINTS.OCR_VALIDATE(resultId)}`,
        { method: 'POST' }
      );
      return await response.json();
    } catch (error) {
      throw new Error('Validation failed');
    }
  }

  /**
   * Detect errors in OCR result
   */
  async detectErrors(resultId: number): Promise<ErrorDetectionResponse> {
    try {
      const response = await fetch(
        `${this.baseUrl}${API_ENDPOINTS.OCR_ERRORS(resultId)}`
      );
      return await response.json();
    } catch (error) {
      throw new Error('Error detection failed');
    }
  }

  /**
   * List all documents
   */
  async listDocuments(): Promise<ApiResponse<Document[]>> {
    return this.fetchApi<Document[]>(API_ENDPOINTS.OCR_DOCUMENTS);
  }

  /**
   * Delete a document
   */
  async deleteDocument(documentId: number): Promise<ApiResponse<{ message: string }>> {
    return this.fetchApi<{ message: string }>(
      API_ENDPOINTS.OCR_DELETE(documentId),
      { method: 'DELETE' }
    );
  }

  // ==================== Analytics ====================

  /**
   * Get dashboard statistics
   */
  async getDashboardStats(): Promise<ApiResponse<DashboardStats>> {
    return this.fetchApi<DashboardStats>(API_ENDPOINTS.ANALYTICS_DASHBOARD);
  }

  /**
   * Get accuracy metrics
   */
  async getAccuracyMetrics(): Promise<ApiResponse<AccuracyMetrics>> {
    return this.fetchApi<AccuracyMetrics>(API_ENDPOINTS.ANALYTICS_ACCURACY);
  }

  /**
   * Get compliance trends
   */
  async getComplianceTrends(): Promise<ApiResponse<ComplianceTrends>> {
    return this.fetchApi<ComplianceTrends>(API_ENDPOINTS.ANALYTICS_TRENDS);
  }

  /**
   * Get error analysis
   */
  async getErrorAnalysis(): Promise<ApiResponse<ErrorAnalysis>> {
    return this.fetchApi<ErrorAnalysis>(API_ENDPOINTS.ANALYTICS_ERRORS);
  }

  /**
   * Get controlled substances statistics
   */
  async getControlledSubstancesStats(): Promise<
    ApiResponse<ControlledSubstancesStats>
  > {
    return this.fetchApi<ControlledSubstancesStats>(
      API_ENDPOINTS.ANALYTICS_CONTROLLED
    );
  }

  // ==================== Language Support ====================

  /**
   * Get supported languages
   */
  async getSupportedLanguages(): Promise<
    ApiResponse<Record<string, string>>
  > {
    return this.fetchApi<Record<string, string>>(
      API_ENDPOINTS.OCR_LANGUAGES
    );
  }

  /**
   * Upload and process a multilingual document
   */
  async uploadMultilingualDocument(file: File): Promise<ApiResponse<any>> {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(
        `${this.baseUrl}${API_ENDPOINTS.OCR_UPLOAD}`,
        {
          method: 'POST',
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.error || 'Upload failed',
        };
      }

      return {
        success: true,
        data: data,
      };
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Upload failed',
      };
    }
  }

  /**
   * Detect language from file
   */
  async detectLanguage(file: File): Promise<
    ApiResponse<{ language_code: string; language_name: string; confidence: number }>
  > {
    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch(
        `${this.baseUrl}${API_ENDPOINTS.OCR_DETECT_LANGUAGE}`,
        {
          method: 'POST',
          body: formData,
        }
      );

      const data = await response.json();

      if (!response.ok) {
        return {
          success: false,
          error: data.error || 'Language detection failed',
        };
      }

      return data;
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Language detection failed',
      };
    }
  }
}

// Export singleton instance
export const apiService = new ApiService();
export default apiService;
