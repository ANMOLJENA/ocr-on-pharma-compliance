/**
 * API Type Definitions
 */

// Document Types
export interface Document {
  id: number;
  filename: string;
  file_type: string;
  file_size: number;
  upload_date: string;
  status: 'pending' | 'processing' | 'completed' | 'failed';
}

// OCR Result Types
export interface OCRResult {
  id: number;
  document_id: number;
  extracted_text: string;
  confidence_score: number;
  processing_time: number;
  processed_date: string;
  drug_name: string | null;
  batch_number: string | null;
  expiry_date: string | null;
  manufacturer: string | null;
  controlled_substance: boolean;
}

// Compliance Check Types
export interface ComplianceCheck {
  id: number;
  ocr_result_id: number;
  rule_id: number | null;
  check_type: string;
  status: 'passed' | 'failed' | 'warning';
  message: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  checked_date: string;
}

// Error Detection Types
export interface ErrorDetection {
  id: number;
  ocr_result_id: number;
  error_type: string;
  field_name: string;
  expected_value: string | null;
  actual_value: string;
  confidence: number;
  suggestion: string;
  detected_date: string;
}

// Analytics Types
export interface DashboardStats {
  total_documents: number;
  status_breakdown: Record<string, number>;
  average_confidence: number;
  compliance: {
    total_checks: number;
    passed: number;
    failed: number;
    pass_rate: number;
  };
  total_errors: number;
  recent_activity: number;
}

export interface AccuracyMetrics {
  confidence_distribution: Array<{
    range: string;
    count: number;
  }>;
  average_processing_time: number;
}

export interface ComplianceTrends {
  [date: string]: {
    passed: number;
    failed: number;
    warning: number;
  };
}

export interface ErrorAnalysis {
  error_types: Array<{
    type: string;
    count: number;
  }>;
  common_fields: Array<{
    field: string;
    count: number;
  }>;
}

export interface ControlledSubstancesStats {
  total_controlled: number;
  total_documents: number;
  percentage: number;
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

export interface UploadResponse {
  success: boolean;
  document_id: number;
  ocr_result_id: number;
  data: OCRResult;
  detected_language?: string;
  original_language?: string;
  translated?: boolean;
  original_text?: string;
  translated_text?: string;
}

export interface ValidationResponse {
  success: boolean;
  compliance_score: number;
  checks: ComplianceCheck[];
}

export interface ErrorDetectionResponse {
  success: boolean;
  errors: ErrorDetection[];
  suggestions: {
    total_errors: number;
    critical_errors: number;
    corrections: Array<{
      field: string;
      current: string;
      suggested: string | null;
      reason: string;
    }>;
  };
}
