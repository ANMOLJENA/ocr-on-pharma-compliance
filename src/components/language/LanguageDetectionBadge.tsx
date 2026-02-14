import { AlertCircle, CheckCircle2, Globe, AlertTriangle } from "lucide-react";
import { cn } from "@/lib/utils";

interface LanguageDetectionBadgeProps {
  detectedLanguage?: string;
  languageCode?: string;
  confidence?: number;
  error?: string | null;
  isLoading?: boolean;
  className?: string;
  size?: "sm" | "md" | "lg";
}

export function LanguageDetectionBadge({
  detectedLanguage,
  languageCode,
  confidence,
  error,
  isLoading = false,
  className,
  size = "md",
}: LanguageDetectionBadgeProps) {
  // Determine confidence level for styling
  const getConfidenceLevel = (conf: number) => {
    if (conf >= 0.9) return "high";
    if (conf >= 0.7) return "medium";
    return "low";
  };

  const confidenceLevel =
    confidence !== undefined ? getConfidenceLevel(confidence) : null;

  // Size classes
  const sizeClasses = {
    sm: "px-2 py-1 text-xs",
    md: "px-3 py-2 text-sm",
    lg: "px-4 py-3 text-base",
  };

  const iconSizes = {
    sm: "w-3 h-3",
    md: "w-4 h-4",
    lg: "w-5 h-5",
  };

  // Error state
  if (error) {
    return (
      <div
        className={cn(
          "flex items-center gap-2 rounded-lg border",
          "bg-destructive/10 border-destructive/30",
          sizeClasses[size],
          className
        )}
      >
        <AlertCircle className={cn("text-destructive flex-shrink-0", iconSizes[size])} />
        <div className="flex-1">
          <p className="font-medium text-destructive">Detection Failed</p>
          <p className="text-xs text-destructive/80">{error}</p>
        </div>
      </div>
    );
  }

  // Loading state
  if (isLoading) {
    return (
      <div
        className={cn(
          "flex items-center gap-2 rounded-lg border",
          "bg-muted border-border",
          sizeClasses[size],
          className
        )}
      >
        <div className={cn("animate-spin text-muted-foreground", iconSizes[size])}>
          <Globe className="w-full h-full" />
        </div>
        <p className="font-medium text-muted-foreground">Detecting language...</p>
      </div>
    );
  }

  // No detection result
  if (!detectedLanguage) {
    return (
      <div
        className={cn(
          "flex items-center gap-2 rounded-lg border",
          "bg-muted border-border",
          sizeClasses[size],
          className
        )}
      >
        <Globe className={cn("text-muted-foreground flex-shrink-0", iconSizes[size])} />
        <p className="font-medium text-muted-foreground">No language detected</p>
      </div>
    );
  }

  // Success state with detected language
  const bgColorMap = {
    high: "bg-success/10 border-success/30",
    medium: "bg-warning/10 border-warning/30",
    low: "bg-amber-100/50 border-amber-300/50",
  };

  const textColorMap = {
    high: "text-success",
    medium: "text-warning",
    low: "text-amber-700",
  };

  const bgColor = confidenceLevel ? bgColorMap[confidenceLevel] : "bg-blue-50 border-blue-200";
  const textColor = confidenceLevel ? textColorMap[confidenceLevel] : "text-blue-700";

  return (
    <div
      className={cn(
        "flex items-center gap-2 rounded-lg border",
        bgColor,
        sizeClasses[size],
        className
      )}
    >
      <CheckCircle2 className={cn("flex-shrink-0", textColor, iconSizes[size])} />
      <div className="flex-1">
        <div className="flex items-center gap-2">
          <p className={cn("font-medium", textColor)}>{detectedLanguage}</p>
          {languageCode && (
            <span className={cn("text-xs font-mono opacity-70", textColor)}>
              ({languageCode})
            </span>
          )}
        </div>
        {confidence !== undefined && (
          <div className="flex items-center gap-2 mt-1">
            <div className="flex-1 h-1.5 bg-black/10 rounded-full overflow-hidden">
              <div
                className={cn(
                  "h-full rounded-full transition-all",
                  confidenceLevel === "high"
                    ? "bg-success"
                    : confidenceLevel === "medium"
                      ? "bg-warning"
                      : "bg-amber-500"
                )}
                style={{ width: `${confidence * 100}%` }}
              />
            </div>
            <span className={cn("text-xs font-medium", textColor)}>
              {(confidence * 100).toFixed(1)}%
            </span>
          </div>
        )}
      </div>
      {confidence !== undefined && confidence < 0.7 && (
        <AlertTriangle className={cn("flex-shrink-0", textColor, iconSizes[size])} />
      )}
    </div>
  );
}
