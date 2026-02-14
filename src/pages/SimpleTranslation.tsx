import { useState } from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { Upload, Loader2, CheckCircle, AlertCircle } from "lucide-react";
import { apiService } from "@/services/api.service";
import { useToast } from "@/hooks/use-toast";

const SimpleTranslation = () => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [originalText, setOriginalText] = useState<string>("");
  const [translatedText, setTranslatedText] = useState<string>("");
  const [language, setLanguage] = useState<string>("");
  const [error, setError] = useState<string | null>(null);
  const { toast } = useToast();

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
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
    setOriginalText("");
    setTranslatedText("");

    try {
      const response = await apiService.uploadMultilingualDocument(selectedFile);

      console.log("[SIMPLE] Full response:", response);

      if (response.success) {
        const data = response.data;
        console.log("[SIMPLE] Data:", data);
        console.log("[SIMPLE] original_text:", data.original_text);
        console.log("[SIMPLE] translated_text:", data.translated_text);
        console.log("[SIMPLE] extracted_text:", data.data?.extracted_text);
        console.log("[SIMPLE] translated flag:", data.translated);

        // Get the texts
        const original = data.original_text || data.data?.extracted_text || "";
        const translated = data.translated_text || data.data?.extracted_text || "";
        const lang = data.detected_language || "Unknown";

        console.log("[SIMPLE] Setting original:", original.substring(0, 50));
        console.log("[SIMPLE] Setting translated:", translated.substring(0, 50));

        setOriginalText(original);
        setTranslatedText(translated);
        setLanguage(lang);

        toast({
          title: "Success!",
          description: `Document processed. Language: ${lang}`,
        });
      } else {
        throw new Error(response.error || "Failed to process");
      }
    } catch (err: any) {
      const errorMessage = err.message || "An error occurred";
      setError(errorMessage);
      console.error("[SIMPLE] Error:", errorMessage);
      toast({
        title: "Error",
        description: errorMessage,
        variant: "destructive",
      });
    } finally {
      setIsProcessing(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1 container mx-auto px-4 py-8 mt-16">
        <div className="max-w-6xl mx-auto">
          <h1 className="text-4xl font-bold mb-8 text-center">
            <span className="gradient-text">Translation Viewer</span>
          </h1>

          {/* Upload Section */}
          <Card className="mb-8 border-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Upload className="w-5 h-5" />
                Upload Document
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <input
                type="file"
                onChange={handleFileSelect}
                accept="image/*,application/pdf"
                className="block w-full"
              />
              <Button
                onClick={handleUpload}
                disabled={!selectedFile || isProcessing}
                className="w-full"
                size="lg"
              >
                {isProcessing ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin mr-2" />
                    Processing...
                  </>
                ) : (
                  "Process & Translate"
                )}
              </Button>
            </CardContent>
          </Card>

          {/* Error Display */}
          {error && (
            <Alert variant="destructive" className="mb-8">
              <AlertCircle className="h-4 w-4" />
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}

          {/* Results */}
          {(originalText || translatedText) && (
            <div className="space-y-6">
              <div className="text-center">
                <h2 className="text-2xl font-bold mb-2">
                  ✅ Translation Complete
                </h2>
                <p className="text-lg text-muted-foreground">
                  Language Detected: <span className="font-bold">{language}</span>
                </p>
              </div>

              {/* Side by Side */}
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Original */}
                <Card className="border-2 border-amber-300 bg-amber-50">
                  <CardHeader className="bg-amber-100">
                    <CardTitle className="text-amber-900">
                      Original ({language})
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <div className="bg-white p-4 rounded border-2 border-amber-200 max-h-96 overflow-y-auto whitespace-pre-wrap font-mono text-sm">
                      {originalText || "No original text"}
                    </div>
                  </CardContent>
                </Card>

                {/* Translated */}
                <Card className="border-2 border-green-300 bg-green-50">
                  <CardHeader className="bg-green-100">
                    <CardTitle className="text-green-900 flex items-center gap-2">
                      <CheckCircle className="w-5 h-5" />
                      English Translation
                    </CardTitle>
                  </CardHeader>
                  <CardContent className="pt-6">
                    <div className="bg-white p-4 rounded border-2 border-green-200 max-h-96 overflow-y-auto whitespace-pre-wrap font-mono text-sm">
                      {translatedText || "No translation"}
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          )}
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default SimpleTranslation;
