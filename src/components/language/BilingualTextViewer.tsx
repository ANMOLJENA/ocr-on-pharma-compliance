import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Copy, Download, Globe, ArrowRight } from "lucide-react";
import { cn } from "@/lib/utils";
import { toast } from "sonner";

interface BilingualTextViewerProps {
  originalText: string;
  translatedText: string;
  originalLanguage: string;
  translatedLanguage?: string;
  translationStatus?: "success" | "pending" | "failed";
  confidence?: number;
  className?: string;
}

export function BilingualTextViewer({
  originalText,
  translatedText,
  originalLanguage,
  translatedLanguage = "English",
  translationStatus = "success",
  confidence,
  className,
}: BilingualTextViewerProps) {
  const [activeTab, setActiveTab] = useState<"side-by-side" | "original" | "translated">(
    "side-by-side"
  );

  const copyToClipboard = (text: string, label: string) => {
    navigator.clipboard.writeText(text);
    toast.success(`${label} copied to clipboard`);
  };

  const downloadText = (text: string, filename: string) => {
    const element = document.createElement("a");
    element.setAttribute(
      "href",
      "data:text/plain;charset=utf-8," + encodeURIComponent(text)
    );
    element.setAttribute("download", filename);
    element.style.display = "none";
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
    toast.success(`${filename} downloaded`);
  };

  const getStatusColor = () => {
    switch (translationStatus) {
      case "success":
        return "bg-success/10 border-success/30 text-success";
      case "pending":
        return "bg-warning/10 border-warning/30 text-warning";
      case "failed":
        return "bg-destructive/10 border-destructive/30 text-destructive";
      default:
        return "bg-muted border-border text-muted-foreground";
    }
  };

  const getStatusIcon = () => {
    switch (translationStatus) {
      case "success":
        return "✓";
      case "pending":
        return "⏳";
      case "failed":
        return "✕";
      default:
        return "•";
    }
  };

  return (
    <div className={cn("space-y-4", className)}>
      {/* Translation Status Header */}
      <div className={cn("flex items-center justify-between p-4 rounded-lg border", getStatusColor())}>
        <div className="flex items-center gap-3">
          <span className="text-lg font-bold">{getStatusIcon()}</span>
          <div>
            <p className="font-medium">
              {originalLanguage}
              <ArrowRight className="w-4 h-4 inline mx-2" />
              {translatedLanguage}
            </p>
            <p className="text-xs opacity-75">
              {translationStatus === "success"
                ? "Translation completed successfully"
                : translationStatus === "pending"
                  ? "Translation in progress..."
                  : "Translation failed - showing original text"}
            </p>
          </div>
        </div>
        {confidence !== undefined && translationStatus === "success" && (
          <div className="text-right">
            <p className="text-xs opacity-75">Confidence</p>
            <p className="text-lg font-bold">{(confidence * 100).toFixed(1)}%</p>
          </div>
        )}
      </div>

      {/* Tabs */}
      <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as any)}>
        <TabsList className="grid w-full grid-cols-3">
          <TabsTrigger value="side-by-side" className="flex items-center gap-2">
            <Globe className="w-4 h-4" />
            <span className="hidden sm:inline">Side by Side</span>
            <span className="sm:hidden">Both</span>
          </TabsTrigger>
          <TabsTrigger value="original" className="flex items-center gap-2">
            <span className="text-xs">{originalLanguage}</span>
          </TabsTrigger>
          <TabsTrigger value="translated" className="flex items-center gap-2">
            <span className="text-xs">{translatedLanguage}</span>
          </TabsTrigger>
        </TabsList>

        {/* Side by Side View */}
        <TabsContent value="side-by-side" className="space-y-4">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
            {/* Original Text */}
            <Card className="flex flex-col bg-card border-border hover:border-primary/30 transition-colors">
              <div className="flex items-center justify-between p-4 border-b border-border">
                <h3 className="font-semibold text-sm flex items-center gap-2">
                  <Globe className="w-4 h-4 text-muted-foreground" />
                  Original ({originalLanguage})
                </h3>
                <div className="flex gap-1">
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8"
                    onClick={() => copyToClipboard(originalText, "Original text")}
                    title="Copy original text"
                  >
                    <Copy className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8"
                    onClick={() => downloadText(originalText, `original_${originalLanguage.toLowerCase()}.txt`)}
                    title="Download original text"
                  >
                    <Download className="w-4 h-4" />
                  </Button>
                </div>
              </div>
              <div className="flex-1 p-4 overflow-auto">
                <div className="bg-muted/30 rounded p-3 text-sm text-foreground whitespace-pre-wrap font-mono leading-relaxed max-h-96 overflow-y-auto">
                  {originalText}
                </div>
              </div>
            </Card>

            {/* Translated Text */}
            <Card className="flex flex-col bg-card border-border hover:border-primary/30 transition-colors">
              <div className="flex items-center justify-between p-4 border-b border-border">
                <h3 className="font-semibold text-sm flex items-center gap-2">
                  <Globe className="w-4 h-4 text-success" />
                  {translatedLanguage} Translation
                </h3>
                <div className="flex gap-1">
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8"
                    onClick={() => copyToClipboard(translatedText, "Translated text")}
                    title="Copy translated text"
                  >
                    <Copy className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    className="h-8 w-8"
                    onClick={() => downloadText(translatedText, `translated_${translatedLanguage.toLowerCase()}.txt`)}
                    title="Download translated text"
                  >
                    <Download className="w-4 h-4" />
                  </Button>
                </div>
              </div>
              <div className="flex-1 p-4 overflow-auto">
                <div className="bg-success/5 rounded p-3 text-sm text-foreground whitespace-pre-wrap font-mono leading-relaxed max-h-96 overflow-y-auto">
                  {translatedText}
                </div>
              </div>
            </Card>
          </div>
        </TabsContent>

        {/* Original Text Only */}
        <TabsContent value="original">
          <Card className="flex flex-col bg-card border-border">
            <div className="flex items-center justify-between p-4 border-b border-border">
              <h3 className="font-semibold flex items-center gap-2">
                <Globe className="w-4 h-4 text-muted-foreground" />
                Original Text ({originalLanguage})
              </h3>
              <div className="flex gap-1">
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => copyToClipboard(originalText, "Original text")}
                  title="Copy original text"
                >
                  <Copy className="w-4 h-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => downloadText(originalText, `original_${originalLanguage.toLowerCase()}.txt`)}
                  title="Download original text"
                >
                  <Download className="w-4 h-4" />
                </Button>
              </div>
            </div>
            <div className="p-4 overflow-auto">
              <div className="bg-muted/30 rounded p-4 text-sm text-foreground whitespace-pre-wrap font-mono leading-relaxed max-h-96 overflow-y-auto">
                {originalText}
              </div>
            </div>
          </Card>
        </TabsContent>

        {/* Translated Text Only */}
        <TabsContent value="translated">
          <Card className="flex flex-col bg-card border-border">
            <div className="flex items-center justify-between p-4 border-b border-border">
              <h3 className="font-semibold flex items-center gap-2">
                <Globe className="w-4 h-4 text-success" />
                {translatedLanguage} Translation
              </h3>
              <div className="flex gap-1">
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => copyToClipboard(translatedText, "Translated text")}
                  title="Copy translated text"
                >
                  <Copy className="w-4 h-4" />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  onClick={() => downloadText(translatedText, `translated_${translatedLanguage.toLowerCase()}.txt`)}
                  title="Download translated text"
                >
                  <Download className="w-4 h-4" />
                </Button>
              </div>
            </div>
            <div className="p-4 overflow-auto">
              <div className="bg-success/5 rounded p-4 text-sm text-foreground whitespace-pre-wrap font-mono leading-relaxed max-h-96 overflow-y-auto">
                {translatedText}
              </div>
            </div>
          </Card>
        </TabsContent>
      </Tabs>

      {/* Info Footer */}
      <div className="text-xs text-muted-foreground p-3 rounded-lg bg-muted/30 border border-border">
        <p>
          💡 Use the tabs above to view the original text, translation, or both side-by-side.
          Copy or download any text using the buttons in each section.
        </p>
      </div>
    </div>
  );
}
