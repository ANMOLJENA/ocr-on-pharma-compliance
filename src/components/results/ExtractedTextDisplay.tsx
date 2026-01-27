import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Copy, Download, Globe } from "lucide-react";
import { toast } from "sonner";

interface ExtractedTextDisplayProps {
  originalText?: string;
  translatedText?: string;
  detectedLanguage?: string;
  originalLanguage?: string;
  isTranslated?: boolean;
  confidence?: number;
}

export function ExtractedTextDisplay({
  originalText,
  translatedText,
  detectedLanguage,
  originalLanguage,
  isTranslated,
  confidence,
}: ExtractedTextDisplayProps) {
  const [activeTab, setActiveTab] = useState<"english" | "side-by-side" | "original" | "translated">(
    isTranslated ? "english" : "original"
  );

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    toast.success(`${label} copied to clipboard`);
  };

  const downloadText = (text: string, filename: string) => {
    const element = document.createElement("a");
    element.setAttribute("href", "data:text/plain;charset=utf-8," + encodeURIComponent(text));
    element.setAttribute("download", filename);
    element.style.display = "none";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    toast.success(`${filename} downloaded`);
  };

  return (
    <div className="space-y-4">
      {/* Language Info */}
      {isTranslated && (
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-blue-900">
                🌍 Language Detection & Conversion
              </p>
              <p className="text-sm text-blue-700">
                Detected: <span className="font-semibold">{detectedLanguage}</span> → Converted to{" "}
                <span className="font-semibold">English</span>
              </p>
            </div>
            {confidence && (
              <div className="text-right">
                <p className="text-sm font-medium text-blue-900">Confidence</p>
                <p className="text-lg font-bold text-blue-700">{(confidence * 100).toFixed(1)}%</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Tabs */}
      {isTranslated && (
        <div className="flex gap-2 border-b overflow-x-auto">
          <button
            onClick={() => setActiveTab("english")}
            className={`px-4 py-2 font-medium text-sm border-b-2 transition-colors whitespace-nowrap ${
              activeTab === "english"
                ? "border-green-500 text-green-600"
                : "border-transparent text-gray-600 hover:text-gray-900"
            }`}
          >
            <Globe className="w-4 h-4 inline mr-2" />
            English (Converted)
          </button>
          <button
            onClick={() => setActiveTab("side-by-side")}
            className={`px-4 py-2 font-medium text-sm border-b-2 transition-colors whitespace-nowrap ${
              activeTab === "side-by-side"
                ? "border-blue-500 text-blue-600"
                : "border-transparent text-gray-600 hover:text-gray-900"
            }`}
          >
            Side by Side
          </button>
          <button
            onClick={() => setActiveTab("original")}
            className={`px-4 py-2 font-medium text-sm border-b-2 transition-colors whitespace-nowrap ${
              activeTab === "original"
                ? "border-blue-500 text-blue-600"
                : "border-transparent text-gray-600 hover:text-gray-900"
            }`}
          >
            Original ({originalLanguage})
          </button>
          <button
            onClick={() => setActiveTab("translated")}
            className={`px-4 py-2 font-medium text-sm border-b-2 transition-colors whitespace-nowrap ${
              activeTab === "translated"
                ? "border-blue-500 text-blue-600"
                : "border-transparent text-gray-600 hover:text-gray-900"
            }`}
          >
            Translation
          </button>
        </div>
      )}

      {/* English Tab - Main Display */}
      {activeTab === "english" && isTranslated && translatedText && (
        <Card className="p-4 bg-green-50 border-green-200">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-2">
              <Globe className="w-5 h-5 text-green-700" />
              <h3 className="font-semibold text-green-900">
                Extracted Text (English - Converted)
              </h3>
              {detectedLanguage && detectedLanguage !== "English" && (
                <span className="text-xs bg-green-200 text-green-800 px-2 py-1 rounded">
                  Converted from {detectedLanguage}
                </span>
              )}
            </div>
            <div className="flex gap-2">
              <button
                onClick={() => copyToClipboard(translatedText, "English text")}
                className="p-1 hover:bg-green-100 rounded transition-colors"
                title="Copy English text"
              >
                <Copy className="w-4 h-4 text-green-700" />
              </button>
              <button
                onClick={() => downloadText(translatedText, "extracted_text_english.txt")}
                className="p-1 hover:bg-green-100 rounded transition-colors"
                title="Download English text"
              >
                <Download className="w-4 h-4 text-green-700" />
              </button>
            </div>
          </div>
          <div className="bg-white rounded p-4 max-h-96 overflow-y-auto text-sm text-gray-700 whitespace-pre-wrap font-mono border border-green-100">
            {translatedText}
          </div>
        </Card>
      )}

      {/* Side by Side Tab */}
      {activeTab === "side-by-side" && isTranslated && originalText && translatedText && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {/* Original Text */}
          <Card className="p-4 bg-amber-50 border-amber-200">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold text-amber-900">
                Original ({originalLanguage})
              </h3>
              <div className="flex gap-2">
                <button
                  onClick={() => copyToClipboard(originalText, "Original text")}
                  className="p-1 hover:bg-amber-100 rounded transition-colors"
                  title="Copy original text"
                >
                  <Copy className="w-4 h-4 text-amber-700" />
                </button>
                <button
                  onClick={() => downloadText(originalText, "original_text.txt")}
                  className="p-1 hover:bg-amber-100 rounded transition-colors"
                  title="Download original text"
                >
                  <Download className="w-4 h-4 text-amber-700" />
                </button>
              </div>
            </div>
            <div className="bg-white rounded p-3 max-h-96 overflow-y-auto text-sm text-gray-700 whitespace-pre-wrap font-mono">
              {originalText}
            </div>
          </Card>

          {/* Translated Text */}
          <Card className="p-4 bg-green-50 border-green-200">
            <div className="flex items-center justify-between mb-3">
              <h3 className="font-semibold text-green-900">English Translation</h3>
              <div className="flex gap-2">
                <button
                  onClick={() => copyToClipboard(translatedText, "Translated text")}
                  className="p-1 hover:bg-green-100 rounded transition-colors"
                  title="Copy translated text"
                >
                  <Copy className="w-4 h-4 text-green-700" />
                </button>
                <button
                  onClick={() => downloadText(translatedText, "translated_text.txt")}
                  className="p-1 hover:bg-green-100 rounded transition-colors"
                  title="Download translated text"
                >
                  <Download className="w-4 h-4 text-green-700" />
                </button>
              </div>
            </div>
            <div className="bg-white rounded p-3 max-h-96 overflow-y-auto text-sm text-gray-700 whitespace-pre-wrap font-mono">
              {translatedText}
            </div>
          </Card>
        </div>
      )}

      {/* Original Only Tab */}
      {activeTab === "original" && originalText && (
        <Card className="p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold">Original Text ({originalLanguage})</h3>
            <div className="flex gap-2">
              <button
                onClick={() => copyToClipboard(originalText, "Original text")}
                className="p-1 hover:bg-gray-100 rounded transition-colors"
                title="Copy original text"
              >
                <Copy className="w-4 h-4" />
              </button>
              <button
                onClick={() => downloadText(originalText, "original_text.txt")}
                className="p-1 hover:bg-gray-100 rounded transition-colors"
                title="Download original text"
              >
                <Download className="w-4 h-4" />
              </button>
            </div>
          </div>
          <div className="bg-gray-50 rounded p-3 max-h-96 overflow-y-auto text-sm text-gray-700 whitespace-pre-wrap font-mono">
            {originalText}
          </div>
        </Card>
      )}

      {/* Translated Only Tab */}
      {activeTab === "translated" && translatedText && (
        <Card className="p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold">English Translation</h3>
            <div className="flex gap-2">
              <button
                onClick={() => copyToClipboard(translatedText, "Translated text")}
                className="p-1 hover:bg-gray-100 rounded transition-colors"
                title="Copy translated text"
              >
                <Copy className="w-4 h-4" />
              </button>
              <button
                onClick={() => downloadText(translatedText, "translated_text.txt")}
                className="p-1 hover:bg-gray-100 rounded transition-colors"
                title="Download translated text"
              >
                <Download className="w-4 h-4" />
              </button>
            </div>
          </div>
          <div className="bg-gray-50 rounded p-3 max-h-96 overflow-y-auto text-sm text-gray-700 whitespace-pre-wrap font-mono">
            {translatedText}
          </div>
        </Card>
      )}

      {/* Fallback for non-translated */}
      {!isTranslated && originalText && (
        <Card className="p-4">
          <div className="flex items-center justify-between mb-3">
            <h3 className="font-semibold">Extracted Text</h3>
            <div className="flex gap-2">
              <button
                onClick={() => copyToClipboard(originalText, "Extracted text")}
                className="p-1 hover:bg-gray-100 rounded transition-colors"
                title="Copy text"
              >
                <Copy className="w-4 h-4" />
              </button>
              <button
                onClick={() => downloadText(originalText, "extracted_text.txt")}
                className="p-1 hover:bg-gray-100 rounded transition-colors"
                title="Download text"
              >
                <Download className="w-4 h-4" />
              </button>
            </div>
          </div>
          <div className="bg-gray-50 rounded p-3 max-h-96 overflow-y-auto text-sm text-gray-700 whitespace-pre-wrap font-mono">
            {originalText}
          </div>
        </Card>
      )}
    </div>
  );
}
