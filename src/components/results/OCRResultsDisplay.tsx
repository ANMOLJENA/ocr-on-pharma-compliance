import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Badge } from "@/components/ui/badge";
import { AlertCircle, Globe, FileText, CheckCircle } from "lucide-react";
import { cn } from "@/lib/utils";
import {
  LanguageDetectionBadge,
  BilingualTextViewer,
} from "@/components/language";

interface OCRResultsDisplayProps {
  /** Original extracted text (in detected language) */
  originalText?: string;
  /** Translated text (usually to English) */
  translatedText?: string;
  /** Detected language name (e.g., "Hindi", "Spanish") */
  detectedLanguage?: string;
  /** Detected language code (e.g., "hi", "es") */
  detectedLanguageCode?: string;
  /** Original language name (same as detected if not translated) */
  originalLanguage?: string;
  /** Whether translation occurred */
  isTranslated?: boolean;
  /** Confidence score for language detection (0.0 to 1.0) */
  confidence?: number;
  /** Error message if language detection or translation failed */
  error?: string | null;
  /** Loading state */
  isLoading?: boolean;
  /** Additional CSS classes */
  className?: string;
  /** Show compliance information */
  complianceStatus?: "pass" | "fail" | "warning" | null;
  /** Compliance message */
  complianceMessage?: string;
}

/**
 * OCRResultsDisplay Component
 *
 * Displays OCR extraction results with integrated language detection and translation information.
 * Supports multilingual documents with side-by-side original/translated text viewing.
 *
 * **Validates: Requirements 6.2, 6.3, 6.4, 6.5**
 *
 * Features:
 * - Language detection badge with confidence score
 * - Bilingual text viewer for translated documents
 * - Error state handling
 * - Loading state
 * - Compliance status display
 * - Responsive design
 */
export function OCRResultsDisplay({
  originalText,
  translatedText,
  detectedLanguage,
  detectedLanguageCode,
  originalLanguage,
  isTranslated = false,
  confidence,
  error,
  isLoading = false,
  className,
  complianceStatus,
  complianceMessage,
}: OCRResultsDisplayProps) {
  const [activeTab, setActiveTab] = useState<"overview" | "text" | "details">(
    "overview"
  );

  // Determine if we have valid data to display
  const hasData = originalText || translatedText;
  const displayLanguage = originalLanguage || detectedLanguage || "Unknown";

  // Get compliance status styling
  const getComplianceStyles = () => {
    switch (complianceStatus) {
      case "pass":
        return {
          bg: "bg-success/10",
          border: "border-success/30",
          text: "text-success",
          icon: "✓",
        };
      case "fail":
        return {
          bg: "bg-destructive/10",
          border: "border-destructive/30",
          text: "text-destructive",
          icon: "✕",
        };
      case "warning":
        return {
          bg: "bg-warning/10",
          border: "border-warning/30",
          text: "text-warning",
          icon: "⚠",
        };
      default:
        return null;
    }
  };

  const complianceStyles = getComplianceStyles();

  // Error state
  if (error) {
    return (
      <Card className={cn("border-destructive/30 bg-destructive/5", className)}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-destructive">
            <AlertCircle className="w-5 h-5" />
            OCR Processing Error
          </CardTitle>
        </CardHeader>
        <CardContent>
          <Alert className="border-destructive/30 bg-destructive/10">
            <AlertCircle className="h-4 w-4 text-destructive" />
            <AlertDescription className="text-destructive">{error}</AlertDescription>
          </Alert>
        </CardContent>
      </Card>
    );
  }

  // Loading state
  if (isLoading) {
    return (
      <Card className={className}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <div className="animate-spin">
              <Globe className="w-5 h-5" />
            </div>
            Processing Document...
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-3">
            <div className="h-4 bg-muted rounded animate-pulse" />
            <div className="h-4 bg-muted rounded animate-pulse w-5/6" />
            <div className="h-32 bg-muted rounded animate-pulse" />
          </div>
        </CardContent>
      </Card>
    );
  }

  // No data state
  if (!hasData) {
    return (
      <Card className={cn("border-dashed", className)}>
        <CardHeader>
          <CardTitle className="flex items-center gap-2 text-muted-foreground">
            <FileText className="w-5 h-5" />
            No OCR Results
          </CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-sm text-muted-foreground">
            Upload a document to see OCR results with language detection and
            translation information.
          </p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card className={className}>
      <CardHeader className="space-y-4">
        <div className="flex items-start justify-between gap-4">
          <CardTitle className="flex items-center gap-2">
            <Globe className="w-5 h-5" />
            OCR Results
          </CardTitle>
          {complianceStatus && complianceStyles && (
            <div
              className={cn(
                "px-3 py-1 rounded-lg border text-sm font-medium flex items-center gap-2",
                complianceStyles.bg,
                complianceStyles.border,
                complianceStyles.text
              )}
            >
              <span>{complianceStyles.icon}</span>
              <span>
                {complianceStatus === "pass"
                  ? "Compliant"
                  : complianceStatus === "fail"
                    ? "Non-Compliant"
                    : "Review Required"}
              </span>
            </div>
          )}
        </div>

        {/* Language Detection Badge */}
        <div className="space-y-2">
          <p className="text-sm font-medium text-muted-foreground">
            Language Detection
          </p>
          <LanguageDetectionBadge
            detectedLanguage={detectedLanguage}
            languageCode={detectedLanguageCode}
            confidence={confidence}
            error={error}
            isLoading={isLoading}
            size="md"
          />
        </div>

        {/* Translation Status */}
        {isTranslated && (
          <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
            <p className="text-sm font-medium text-blue-900">
              🔄 Translation Status
            </p>
            <p className="text-sm text-blue-700 mt-1">
              Document translated from <span className="font-semibold">{displayLanguage}</span> to{" "}
              <span className="font-semibold">English</span>
            </p>
          </div>
        )}

        {/* Compliance Message */}
        {complianceMessage && (
          <Alert className="border-blue-200 bg-blue-50">
            <AlertCircle className="h-4 w-4 text-blue-600" />
            <AlertDescription className="text-blue-700">
              {complianceMessage}
            </AlertDescription>
          </Alert>
        )}
      </CardHeader>

      <CardContent>
        <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as any)}>
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="overview">Overview</TabsTrigger>
            <TabsTrigger value="text">Text</TabsTrigger>
            <TabsTrigger value="details">Details</TabsTrigger>
          </TabsList>

          {/* Overview Tab */}
          <TabsContent value="overview" className="space-y-4">
            {isTranslated && originalText && translatedText ? (
              <div className="space-y-4">
                {/* English Translation - Primary Display */}
                <Card className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-400 shadow-lg">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-xl font-bold text-green-900 flex items-center gap-2">
                      <CheckCircle className="w-6 h-6 text-green-600" />
                      English Translation
                    </h3>
                    <Badge className="bg-green-600 text-white text-base px-4 py-2">
                      ✓ Converted to English
                    </Badge>
                  </div>
                  <div className="bg-white rounded-lg p-5 border-2 border-green-300 shadow-inner max-h-96 overflow-y-auto">
                    <pre className="text-base text-gray-900 whitespace-pre-wrap font-sans leading-relaxed">
                      {translatedText}
                    </pre>
                  </div>
                </Card>

                {/* Original Text - Secondary Display */}
                <details className="group">
                  <summary className="cursor-pointer list-none">
                    <Card className="p-4 bg-amber-50 border-amber-200 hover:border-amber-300 transition-colors">
                      <div className="flex items-center justify-between">
                        <h3 className="font-semibold text-amber-900 flex items-center gap-2">
                          <Globe className="w-5 h-5" />
                          View Original Text ({displayLanguage})
                        </h3>
                        <span className="text-amber-600 group-open:rotate-180 transition-transform">
                          ▼
                        </span>
                      </div>
                    </Card>
                  </summary>
                  <Card className="p-4 bg-amber-50 border-amber-200 mt-2">
                    <div className="bg-white rounded p-4 max-h-96 overflow-y-auto text-sm text-foreground whitespace-pre-wrap font-mono border border-amber-100">
                      {originalText}
                    </div>
                  </Card>
                </details>
              </div>
            ) : (
              <Card className="p-4 bg-muted/30">
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-semibold text-sm">Extracted Text</h3>
                </div>
                <div className="bg-background rounded p-3 max-h-96 overflow-y-auto text-sm text-foreground whitespace-pre-wrap font-mono">
                  {originalText}
                </div>
              </Card>
            )}
          </TabsContent>

          {/* Text Tab */}
          <TabsContent value="text" className="space-y-4">
            {isTranslated && originalText && translatedText ? (
              <div className="space-y-6">
                {/* English Translation - Show First and Prominently */}
                <Card className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-400 shadow-lg">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <h3 className="text-xl font-bold text-green-900 flex items-center gap-2">
                        <CheckCircle className="w-5 h-5 text-green-600" />
                        ✅ English Translation (Converted)
                      </h3>
                      <Badge className="bg-green-600 text-white text-sm px-3 py-1">
                        Translated to English
                      </Badge>
                    </div>
                    <div className="bg-white rounded-lg p-5 border-2 border-green-300 shadow-inner max-h-[400px] overflow-y-auto">
                      <pre className="text-base text-gray-900 whitespace-pre-wrap font-sans leading-relaxed">
                        {translatedText}
                      </pre>
                    </div>
                  </div>
                </Card>

                {/* Original Text - Show Below */}
                <Card className="p-6 bg-gradient-to-br from-amber-50 to-orange-50 border-2 border-amber-300 shadow-lg">
                  <div className="space-y-3">
                    <div className="flex items-center justify-between">
                      <h3 className="text-lg font-bold text-amber-900 flex items-center gap-2">
                        <Globe className="w-5 h-5 text-amber-600" />
                        Original Text ({displayLanguage})
                      </h3>
                      <Badge className="bg-amber-600 text-white">
                        {displayLanguage}
                      </Badge>
                    </div>
                    <div className="bg-white rounded-lg p-5 border-2 border-amber-200 shadow-inner max-h-[400px] overflow-y-auto">
                      <pre className="text-sm text-gray-800 whitespace-pre-wrap font-mono leading-relaxed">
                        {originalText}
                      </pre>
                    </div>
                  </div>
                </Card>
              </div>
            ) : (
              <Card className="p-6 bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-300">
                <div className="space-y-3">
                  <h3 className="text-lg font-bold text-blue-900 flex items-center gap-2">
                    <FileText className="w-5 h-5" />
                    Extracted Text
                  </h3>
                  <div className="bg-white rounded-lg p-5 border-2 border-blue-200 max-h-[400px] overflow-y-auto">
                    <pre className="text-base text-gray-900 whitespace-pre-wrap font-sans leading-relaxed">
                      {originalText}
                    </pre>
                  </div>
                </div>
              </Card>
            )}
          </TabsContent>

          {/* Details Tab */}
          <TabsContent value="details" className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Language Information */}
              <Card className="p-4">
                <h3 className="font-semibold text-sm mb-3 flex items-center gap-2">
                  <Globe className="w-4 h-4" />
                  Language Information
                </h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Detected Language:</span>
                    <span className="font-medium">{detectedLanguage || "Unknown"}</span>
                  </div>
                  {detectedLanguageCode && (
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Language Code:</span>
                      <span className="font-mono text-xs bg-muted px-2 py-1 rounded">
                        {detectedLanguageCode}
                      </span>
                    </div>
                  )}
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Original Language:</span>
                    <span className="font-medium">{displayLanguage}</span>
                  </div>
                  {confidence !== undefined && (
                    <div className="flex justify-between">
                      <span className="text-muted-foreground">Confidence:</span>
                      <span className="font-medium">
                        {(confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                  )}
                </div>
              </Card>

              {/* Translation Information */}
              <Card className="p-4">
                <h3 className="font-semibold text-sm mb-3 flex items-center gap-2">
                  <FileText className="w-4 h-4" />
                  Translation Information
                </h3>
                <div className="space-y-2 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Translation Status:</span>
                    <span className={cn(
                      "font-medium px-2 py-1 rounded text-xs",
                      isTranslated
                        ? "bg-success/10 text-success"
                        : "bg-muted text-muted-foreground"
                    )}>
                      {isTranslated ? "Translated" : "Not Translated"}
                    </span>
                  </div>
                  {isTranslated && (
                    <>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Source Language:</span>
                        <span className="font-medium">{displayLanguage}</span>
                      </div>
                      <div className="flex justify-between">
                        <span className="text-muted-foreground">Target Language:</span>
                        <span className="font-medium">English</span>
                      </div>
                    </>
                  )}
                </div>
              </Card>
            </div>

            {/* Text Statistics */}
            {(originalText || translatedText) && (
              <Card className="p-4">
                <h3 className="font-semibold text-sm mb-3">Text Statistics</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                  <div>
                    <p className="text-muted-foreground text-xs">Original Length</p>
                    <p className="font-semibold text-lg">
                      {originalText?.length || 0}
                    </p>
                  </div>
                  {translatedText && (
                    <div>
                      <p className="text-muted-foreground text-xs">Translated Length</p>
                      <p className="font-semibold text-lg">
                        {translatedText.length}
                      </p>
                    </div>
                  )}
                  <div>
                    <p className="text-muted-foreground text-xs">Word Count</p>
                    <p className="font-semibold text-lg">
                      {(originalText || "").split(/\s+/).filter(w => w.length > 0).length}
                    </p>
                  </div>
                  <div>
                    <p className="text-muted-foreground text-xs">Line Count</p>
                    <p className="font-semibold text-lg">
                      {(originalText || "").split("\n").length}
                    </p>
                  </div>
                </div>
              </Card>
            )}
          </TabsContent>
        </Tabs>
      </CardContent>
    </Card>
  );
}
