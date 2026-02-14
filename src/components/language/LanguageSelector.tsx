import { useState, useEffect } from "react";
import { Globe, AlertCircle } from "lucide-react";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { apiService } from "@/services/api.service";

interface LanguageSelectorProps {
  onLanguageSelect?: (languageCode: string, languageName: string) => void;
  showLabel?: boolean;
}

export function LanguageSelector({
  onLanguageSelect,
  showLabel = true,
}: LanguageSelectorProps) {
  const [languages, setLanguages] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedLanguage, setSelectedLanguage] = useState<string>("");

  useEffect(() => {
    const fetchLanguages = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const response = await apiService.getSupportedLanguages();

        if (response.success && response.data) {
          setLanguages(response.data);
          // Set default to English
          setSelectedLanguage("en");
        } else {
          setError(response.error || "Failed to load languages");
        }
      } catch (err) {
        setError(
          err instanceof Error ? err.message : "Failed to load languages"
        );
      } finally {
        setIsLoading(false);
      }
    };

    fetchLanguages();
  }, []);

  const handleLanguageChange = (value: string) => {
    setSelectedLanguage(value);
    if (onLanguageSelect) {
      onLanguageSelect(value, languages[value] || value);
    }
  };

  if (error) {
    return (
      <Alert variant="destructive">
        <AlertCircle className="h-4 w-4" />
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  return (
    <div className="space-y-2">
      {showLabel && (
        <label className="text-sm font-medium flex items-center gap-2">
          <Globe className="w-4 h-4" />
          Document Language
        </label>
      )}
      <Select value={selectedLanguage} onValueChange={handleLanguageChange} disabled={isLoading}>
        <SelectTrigger className="w-full">
          <SelectValue placeholder="Select language..." />
        </SelectTrigger>
        <SelectContent>
          {Object.entries(languages).map(([code, name]) => (
            <SelectItem key={code} value={code}>
              {name}
            </SelectItem>
          ))}
        </SelectContent>
      </Select>
      {!isLoading && Object.keys(languages).length > 0 && (
        <p className="text-xs text-muted-foreground">
          {Object.keys(languages).length} languages supported
        </p>
      )}
    </div>
  );
}
