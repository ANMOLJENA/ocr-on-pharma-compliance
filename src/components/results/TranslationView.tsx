import { Card } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { ArrowRight, Languages } from "lucide-react";
import { cn } from "@/lib/utils";

interface TranslationViewProps {
  originalText: string;
  translatedText: string;
  originalLanguage: string;
  targetLanguage?: string;
  className?: string;
}

/**
 * TranslationView Component
 * 
 * Displays original and translated text side-by-side with clear visual separation
 */
export function TranslationView({
  originalText,
  translatedText,
  originalLanguage,
  targetLanguage = "English",
  className,
}: TranslationViewProps) {
  return (
    <div className={cn("space-y-4", className)}>
      {/* Header with Translation Indicator */}
      <div className="flex items-center justify-center gap-3 py-4">
        <Badge variant="outline" className="text-base px-4 py-2 bg-amber-50 border-amber-300 text-amber-900">
          <Languages className="w-4 h-4 mr-2" />
          {originalLanguage}
        </Badge>
        <ArrowRight className="w-6 h-6 text-primary animate-pulse" />
        <Badge variant="outline" className="text-base px-4 py-2 bg-green-50 border-green-300 text-green-900">
          <Languages className="w-4 h-4 mr-2" />
          {targetLanguage}
        </Badge>
      </div>

      {/* Side-by-Side Text Display */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Original Text */}
        <Card className="p-6 bg-gradient-to-br from-amber-50 to-orange-50 border-2 border-amber-300 shadow-lg">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-amber-900 flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-amber-500 animate-pulse" />
                Original Text
              </h3>
              <Badge className="bg-amber-600 text-white">
                {originalLanguage}
              </Badge>
            </div>
            <div className="bg-white rounded-lg p-4 border-2 border-amber-200 shadow-inner max-h-[500px] overflow-y-auto">
              <pre className="text-sm text-gray-800 whitespace-pre-wrap font-mono leading-relaxed">
                {originalText}
              </pre>
            </div>
          </div>
        </Card>

        {/* Translated Text */}
        <Card className="p-6 bg-gradient-to-br from-green-50 to-emerald-50 border-2 border-green-300 shadow-lg">
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <h3 className="text-lg font-bold text-green-900 flex items-center gap-2">
                <div className="w-3 h-3 rounded-full bg-green-500 animate-pulse" />
                English Translation
              </h3>
              <Badge className="bg-green-600 text-white">
                {targetLanguage}
              </Badge>
            </div>
            <div className="bg-white rounded-lg p-4 border-2 border-green-200 shadow-inner max-h-[500px] overflow-y-auto">
              <pre className="text-sm text-gray-800 whitespace-pre-wrap font-mono leading-relaxed">
                {translatedText}
              </pre>
            </div>
          </div>
        </Card>
      </div>

      {/* Translation Info */}
      <div className="bg-blue-50 border-2 border-blue-200 rounded-lg p-4">
        <div className="flex items-start gap-3">
          <div className="w-8 h-8 rounded-full bg-blue-500 flex items-center justify-center flex-shrink-0">
            <Languages className="w-4 h-4 text-white" />
          </div>
          <div>
            <p className="font-semibold text-blue-900">Automatic Translation</p>
            <p className="text-sm text-blue-700 mt-1">
              This document was automatically translated from <span className="font-bold">{originalLanguage}</span> to{" "}
              <span className="font-bold">{targetLanguage}</span> using AI-powered translation.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
