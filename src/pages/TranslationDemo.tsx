import { useState } from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Upload, FileText, Globe, Loader2, CheckCircle, AlertCircle } from "lucide-react";
import { OCRResultsDisplay } from "@/components/results/OCRResultsDisplay";
import { TranslationView } from "@/components/results/TranslationView";
import { apiService } from "@/services/api.service";
import { useToast } from "@/hooks/use-toast";

interface OCRResult {
  originalText: string;
  translatedText?: string;
  detectedLanguage: string;
  detectedLanguageCode: string;
  originalLanguage: string;
  isTranslated: boolean;
  confidence?: number;
  documentId?: number;
  ocrResultId?: number;
}

const TranslationDemo = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [ocrResult, setOcrResult] = useState<OCRResult | null>(null);
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      // Validate file type
      const validTypes = ['image/jpeg', 'image/jpg', 'image/png', 'application/pdf'];
      if (!validTypes.includes(file.type)) {
        toast({
          title: "Invalid File Type",
          description: "Please upload a JPG, PNG, or PDF file.",
          variant: "destructive",
        });
        return;
      }

      // Validate file size (max 10MB)
      if (file.size > 10 * 1024 * 1024) {
        toast({
          title: "File Too Large",
          description: "Please upload a file smaller than 10MB.",
          variant: "destructive",
        });
        return;
      }

      setSelectedFile(file);
      setOcrResult(null);
      setError(null);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      toast({
        title: "No File Selected",
        description: "Please select a file to upload.",
        variant: "destructive",
      });
      return;
    }

    setIsProcessing(true);
    setError(null);

    try {
      // Upload and process the file
      const response = await apiService.uploadMultilingualDocument(selectedFile);

      if (response.success && response.data) {
        console.log("[FRONTEND] Response data:", response.data);
        
        // Extract the OCR result data
        const translatedText = response.data.translated_text || (response.data.translated ? response.data.data?.extracted_text : undefined);
        const originalText = response.data.original_text || response.data.data?.extracted_text || "";
        
        const result: OCRResult = {
          originalText: originalText,
          translatedText: translatedText,
          detectedLanguage: response.data.detected_language || "Unknown",
          detectedLanguageCode: response.data.detected_language_code || "",
          originalLanguage: response.data.original_language || response.data.detected_language || "Unknown",
          isTranslated: response.data.translated || false,
          confidence: response.data.confidence,
          documentId: response.data.document_id,
          ocrResultId: response.data.ocr_result_id,
        };

        console.log("[FRONTEND] Parsed result:", result);
        console.log("[FRONTEND] Is Translated:", result.isTranslated);
        console.log("[FRONTEND] Original Text:", result.originalText?.substring(0, 100));
        console.log("[FRONTEND] Translated Text:", result.translatedText?.substring(0, 100));

        setOcrResult(result);

        toast({
          title: "Processing Complete",
          description: `Document processed successfully. Language: ${result.detectedLanguage}`,
        });
      } else {
        throw new Error(response.error || "Failed to process document");
      }
    } catch (err: any) {
      const errorMessage = err.message || "An error occurred while processing the document";
      setError(errorMessage);
      toast({
        title: "Processing Failed",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setOcrResult(null);
    setError(null);
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-b from-background via-accent/10 to-background">
      <Navbar />
      
      <main className="flex-1 container mx-auto px-4 py-8 mt-16">
        {/* Header */}
        <div className="text-center max-w-3xl mx-auto mb-8">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-4">
            <Globe className="w-4 h-4 text-primary" />
            <span className="text-sm font-medium text-primary">Multilingual OCR Translation</span>
          </div>
          
          <h1 className="text-4xl md:text-5xl font-bold mb-4">
            <span className="gradient-text">Extract & Translate</span>
          </h1>
          
          <p className="text-lg text-muted-foreground">
            Upload pharmaceutical labels in any language. Our AI will extract the text and translate it to English automatically.
          </p>
        </div>

        {/* Upload Section */}
        <div className="max-w-4xl mx-auto mb-8">
          <Card className="border-2 border-dashed hover:border-primary/50 transition-colors">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="w-5 h-5" />
                Upload Document
              </CardTitle>
              <CardDescription>
                Supported formats: JPG, PNG, PDF (Max 10MB)
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {/* File Input */}
              <div className="flex flex-col items-center justify-center p-8 border-2 border-dashed rounded-lg bg-muted/30 hover:bg-muted/50 transition-colors">
                <input
                  type="file"
                  id="file-upload"
                  accept="image/jpeg,image/jpg,image/png,application/pdf"
                  onChange={handleFileSelect}
                  className="hidden"
                />
                <label
                  htmlFor="file-upload"
                  className="cursor-pointer flex flex-col items-center gap-2"
                >
                  <div className="w-16 h-16 rounded-full bg-primary/10 flex items-center justify-center">
                    <FileText className="w-8 h-8 text-primary" />
                  </div>
                  <p className="text-sm font-medium">Click to select a file</p>
                  <p className="text-xs text-muted-foreground">or drag and drop</p>
                </label>
              </div>

              {/* Selected File Info */}
              {selectedFile && (
                <Alert className="border-primary/30 bg-primary/5">
                  <CheckCircle className="h-4 w-4 text-primary" />
                  <AlertDescription className="flex items-center justify-between">
                    <span className="font-medium">{selectedFile.name}</span>
                    <span className="text-xs text-muted-foreground">
                      {(selectedFile.size / 1024).toFixed(2)} KB
                    </span>
                  </AlertDescription>
                </Alert>
              )}

              {/* Action Buttons */}
              <div className="flex gap-3">
                <Button
                  onClick={handleUpload}
                  disabled={!selectedFile || isProcessing}
                  className="flex-1"
                  size="lg"
                >
                  {isProcessing ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Processing...
                    </>
                  ) : (
                    <>
                      <Globe className="w-4 h-4" />
                      Process & Translate
                    </>
                  )}
                </Button>
                
                {(selectedFile || ocrResult) && (
                  <Button
                    onClick={handleReset}
                    variant="outline"
                    disabled={isProcessing}
                    size="lg"
                  >
                    Reset
                  </Button>
                )}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Error Display */}
        {error && (
          <div className="max-w-4xl mx-auto mb-8">
            <Alert variant="destructive">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          </div>
        )}

        {/* Results Section */}
        {ocrResult && (
          <div className="max-w-6xl mx-auto animate-fade-in space-y-6">
            {/* Translation View - Prominent Display */}
            {ocrResult.isTranslated && ocrResult.originalText && ocrResult.translatedText && (
              <Card className="border-2 border-primary/20 shadow-xl">
                <CardHeader className="bg-gradient-to-r from-primary/5 to-primary/10">
                  <CardTitle className="flex items-center gap-2 text-2xl">
                    <Globe className="w-6 h-6 text-primary" />
                    Translation Results
                  </CardTitle>
                  <CardDescription className="text-base">
                    Your document has been automatically translated from {ocrResult.detectedLanguage} to English
                  </CardDescription>
                </CardHeader>
                <CardContent className="pt-6">
                  <TranslationView
                    originalText={ocrResult.originalText}
                    translatedText={ocrResult.translatedText}
                    originalLanguage={ocrResult.detectedLanguage}
                    targetLanguage="English"
                  />
                </CardContent>
              </Card>
            )}

            {/* Full OCR Results Display */}
            <OCRResultsDisplay
              originalText={ocrResult.originalText}
              translatedText={ocrResult.translatedText}
              detectedLanguage={ocrResult.detectedLanguage}
              detectedLanguageCode={ocrResult.detectedLanguageCode}
              originalLanguage={ocrResult.originalLanguage}
              isTranslated={ocrResult.isTranslated}
              confidence={ocrResult.confidence}
              isLoading={isProcessing}
            />
          </div>
        )}
      </main>
      
      <Footer />
    </div>
  );
};

export default TranslationDemo;
