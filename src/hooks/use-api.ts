/**
 * Custom hooks for API operations
 */

import { useState, useEffect } from 'react';
import { apiService } from '@/services/api.service';
import type {
  DashboardStats,
  Document,
  ComplianceRule,
  OCRResult,
} from '@/types/api';

/**
 * Hook for dashboard statistics
 */
export function useDashboardStats() {
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchStats = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiService.getDashboardStats();
      if (response.success && response.data) {
        setStats(response.data);
      } else {
        setError(response.error || 'Failed to fetch stats');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  return { stats, loading, error, refetch: fetchStats };
}

/**
 * Hook for documents list
 */
export function useDocuments() {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchDocuments = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiService.listDocuments();
      if (response.success && response.data) {
        setDocuments(response.data);
      } else {
        setError(response.error || 'Failed to fetch documents');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, []);

  const deleteDocument = async (id: number) => {
    try {
      const response = await apiService.deleteDocument(id);
      if (response.success) {
        setDocuments(documents.filter((doc) => doc.id !== id));
        return true;
      }
      return false;
    } catch (err) {
      console.error('Delete failed:', err);
      return false;
    }
  };

  return { documents, loading, error, refetch: fetchDocuments, deleteDocument };
}

/**
 * Hook for compliance rules
 */
export function useComplianceRules() {
  const [rules, setRules] = useState<ComplianceRule[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchRules = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await apiService.listRules();
      if (response.success && response.data) {
        setRules(response.data);
      } else {
        setError(response.error || 'Failed to fetch rules');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRules();
  }, []);

  const toggleRule = async (id: number) => {
    try {
      const response = await apiService.toggleRule(id);
      if (response.success && response.data) {
        setRules(
          rules.map((rule) => (rule.id === id ? response.data! : rule))
        );
        return true;
      }
      return false;
    } catch (err) {
      console.error('Toggle failed:', err);
      return false;
    }
  };

  const deleteRule = async (id: number) => {
    try {
      const response = await apiService.deleteRule(id);
      if (response.success) {
        setRules(rules.filter((rule) => rule.id !== id));
        return true;
      }
      return false;
    } catch (err) {
      console.error('Delete failed:', err);
      return false;
    }
  };

  return { rules, loading, error, refetch: fetchRules, toggleRule, deleteRule };
}

/**
 * Hook for file upload
 */
export function useFileUpload() {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);
  const [result, setResult] = useState<OCRResult | null>(null);
  const [error, setError] = useState<string | null>(null);

  const uploadFile = async (file: File) => {
    setUploading(true);
    setProgress(0);
    setError(null);
    setResult(null);

    try {
      // Simulate progress
      const progressInterval = setInterval(() => {
        setProgress((prev) => Math.min(prev + 10, 90));
      }, 200);

      const response = await apiService.uploadDocument(file);

      clearInterval(progressInterval);
      setProgress(100);

      if (response.success && response.data) {
        setResult(response.data);
        return response;
      } else {
        throw new Error('Upload failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Upload failed');
      throw err;
    } finally {
      setUploading(false);
    }
  };

  const reset = () => {
    setUploading(false);
    setProgress(0);
    setResult(null);
    setError(null);
  };

  return { uploadFile, uploading, progress, result, error, reset };
}

/**
 * Hook for backend health check
 */
export function useHealthCheck() {
  const [healthy, setHealthy] = useState<boolean | null>(null);
  const [checking, setChecking] = useState(true);

  const checkHealth = async () => {
    setChecking(true);
    try {
      const response = await apiService.healthCheck();
      setHealthy(response.status === 'healthy');
    } catch (err) {
      setHealthy(false);
    } finally {
      setChecking(false);
    }
  };

  useEffect(() => {
    checkHealth();
    // Check every 30 seconds
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return { healthy, checking, checkHealth };
}
