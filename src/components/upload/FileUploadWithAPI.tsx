/**
 * File Upload Component with Backend Integration
 */

import { useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, FileText, CheckCircle, XCircle, Loader2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Progress } from '@/components/ui/progress';
import { Card, CardContent } from '@/components/ui/card';
import { ExtractedTextDisplay } from '@/components/results/ExtractedTextDisplay';
import { useFileUpload } from '@/hooks/use-api';
import { useToast } from '@/hooks/use-toast';
import type { OCRResult } from '@/types/api';

interface FileUploadWithAPIProps {
  onUploadSuccess?: (result: OCRResult) => void;
  onUploadError?: (error: string) => void;
}

export function FileUploadWithAPI({
  onUploadSuccess,
  onUploadError,
}: FileUploadWithAPIProps) {
  const { uploadFile, uploading, progress, result, languageInfo, error, reset } = useFileUpload();
  const { toast } = useToast();
  const [selectedFile, setSelectedFile] = useState<File | null>(null);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'image/*': ['.png', '.jpg', '.jpeg', '.tiff', '.bmp'],
      'application/pdf': ['.pdf'],
    },
    maxFiles: 1,
    maxSize: 16 * 1024 * 1024, // 16MB
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        setSelectedFile(acceptedFiles[0]);
        reset();
      }
    },
    onDropRejected: (fileRejections) => {
      const error = fileRejections[0]?.errors[0]?.message || 'File rejected';
      toast({
        title: 'Upload Error',
        description: error,
        variant: 'destructive',
      });
    },
  });

  const handleUpload = async () => {
    if (!selectedFile) return;

    try {
      const response = await uploadFile(selectedFile);

      toast({
        title: 'Upload Successful',
        description: `Document processed with ${(response.data.confidence_score * 100).toFixed(1)}% confidence`,
      });

      if (onUploadSuccess && response.data) {
        onUploadSuccess(response.data);
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Upload failed';
      toast({
        title: 'Upload Failed',
        description: errorMessage,
        variant: 'destructive',
      });

      if (onUploadError) {
        onUploadError(errorMessage);
      }
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    reset();
  };

  return (
    <div className="space-y-4">
      {/* Dropzone */}
      {!selectedFile && !result && (
        <Card>
          <CardContent className="pt-6">
            <div
              {...getRootProps()}
              className={`
                border-2 border-dashed rounded-lg p-12 text-center cursor-pointer
                transition-colors duration-200
                ${
                  isDragActive
                    ? 'border-primary bg-primary/5'
                    : 'border-gray-300 hover:border-primary/50'
                }
              `}
            >
              <input {...getInputProps()} />
              <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
              <p className="text-lg font-medium mb-2">
                {isDragActive
                  ? 'Drop the file here'
                  : 'Drag & drop a pharmaceutical document'}
              </p>
              <p className="text-sm text-gray-500 mb-4">
                or click to select a file
              </p>
              <p className="text-xs text-gray-400">
                Supported: PNG, JPG, TIFF, PDF (Max 16MB)
              </p>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Selected File */}
      {selectedFile && !uploading && !result && (
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <FileText className="h-8 w-8 text-primary" />
                <div>
                  <p className="font-medium">{selectedFile.name}</p>
                  <p className="text-sm text-gray-500">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
              <div className="flex space-x-2">
                <Button variant="outline" onClick={handleReset}>
                  Cancel
                </Button>
                <Button onClick={handleUpload}>
                  <Upload className="mr-2 h-4 w-4" />
                  Upload & Process
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Uploading Progress */}
      {uploading && (
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Loader2 className="h-6 w-6 animate-spin text-primary" />
                  <div>
                    <p className="font-medium">Processing document...</p>
                    <p className="text-sm text-gray-500">
                      Extracting text and analyzing compliance
                    </p>
                  </div>
                </div>
                <span className="text-sm font-medium">{progress}%</span>
              </div>
              <Progress value={progress} className="w-full" />
            </div>
          </CardContent>
        </Card>
      )}

      {/* Success Result */}
      {result && !error && (
        <div className="space-y-4">
          <Card className="border-green-200 bg-green-50">
            <CardContent className="pt-6">
              <div className="space-y-4">
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-3">
                    <CheckCircle className="h-6 w-6 text-green-600 mt-1" />
                    <div className="space-y-2">
                      <p className="font-medium text-green-900">
                        Document Processed Successfully
                      </p>
                      <div className="text-sm text-green-700 space-y-1">
                        <p>
                          <span className="font-medium">Confidence:</span>{' '}
                          {(result.confidence_score * 100).toFixed(1)}%
                        </p>
                        <p>
                          <span className="font-medium">Processing Time:</span>{' '}
                          {result.processing_time.toFixed(2)}s
                        </p>
                        {result.drug_name && (
                          <p>
                            <span className="font-medium">Drug:</span> {result.drug_name}
                          </p>
                        )}
                        {result.batch_number && (
                          <p>
                            <span className="font-medium">Batch:</span>{' '}
                            {result.batch_number}
                          </p>
                        )}
                        {result.controlled_substance && (
                          <p className="text-orange-600 font-medium">
                            ⚠️ Controlled Substance Detected
                          </p>
                        )}
                      </div>
                    </div>
                  </div>
                  <Button variant="outline" size="sm" onClick={handleReset}>
                    Upload Another
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>

          {/* Extracted Text Display with Multilingual Support */}
          {languageInfo && (
            <Card>
              <CardContent className="pt-6">
                <h3 className="text-lg font-semibold mb-4">Extracted Text</h3>
                <ExtractedTextDisplay
                  originalText={languageInfo.originalText}
                  translatedText={languageInfo.translatedText}
                  detectedLanguage={languageInfo.detectedLanguage}
                  originalLanguage={languageInfo.originalLanguage}
                  isTranslated={languageInfo.isTranslated}
                  confidence={result.confidence_score}
                />
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Error */}
      {error && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="pt-6">
            <div className="flex items-start space-x-3">
              <XCircle className="h-6 w-6 text-red-600 mt-1" />
              <div className="flex-1">
                <p className="font-medium text-red-900">Upload Failed</p>
                <p className="text-sm text-red-700 mt-1">{error}</p>
                <Button
                  variant="outline"
                  size="sm"
                  onClick={handleReset}
                  className="mt-3"
                >
                  Try Again
                </Button>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
