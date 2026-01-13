import { useState, useCallback } from "react";
import { useDropzone } from "react-dropzone";
import { Upload, Image, X, FileCheck, Loader2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";
import { toast } from "@/hooks/use-toast";

interface UploadZoneProps {
  onFilesUploaded: (files: File[]) => void;
}

export function UploadZone({ onFilesUploaded }: UploadZoneProps) {
  const [files, setFiles] = useState<File[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const imageFiles = acceptedFiles.filter(file => 
      file.type.startsWith('image/')
    );
    
    if (imageFiles.length !== acceptedFiles.length) {
      toast({
        title: "Invalid file type",
        description: "Only image files (JPG, PNG) are accepted.",
        variant: "destructive",
      });
    }
    
    setFiles(prev => [...prev, ...imageFiles]);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/jpeg': ['.jpg', '.jpeg'],
      'image/png': ['.png'],
    },
    maxSize: 10 * 1024 * 1024, // 10MB
  });

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  const handleProcess = async () => {
    if (files.length === 0) return;
    
    setIsProcessing(true);
    
    // Simulate processing
    await new Promise(resolve => setTimeout(resolve, 2000));
    
    onFilesUploaded(files);
    
    toast({
      title: "Processing Complete",
      description: `${files.length} image(s) processed successfully.`,
    });
    
    setIsProcessing(false);
    setFiles([]);
  };

  return (
    <div className="w-full max-w-3xl mx-auto">
      {/* Drop Zone */}
      <div
        {...getRootProps()}
        className={cn(
          "relative group cursor-pointer rounded-2xl border-2 border-dashed transition-all duration-300 p-8 md:p-12",
          isDragActive 
            ? "border-primary bg-accent/50 scale-[1.02]" 
            : "border-border hover:border-primary/50 hover:bg-accent/20",
          "focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2"
        )}
      >
        <input {...getInputProps()} />
        
        {/* Background decoration */}
        <div className="absolute inset-0 bg-gradient-to-br from-primary/5 to-transparent rounded-2xl opacity-0 group-hover:opacity-100 transition-opacity duration-300" />
        
        <div className="relative flex flex-col items-center text-center">
          <div className={cn(
            "w-16 h-16 rounded-2xl flex items-center justify-center mb-6 transition-all duration-300",
            isDragActive 
              ? "bg-primary text-primary-foreground scale-110" 
              : "bg-accent text-accent-foreground group-hover:bg-primary/10"
          )}>
            <Upload className="w-8 h-8" />
          </div>
          
          <h3 className="font-display text-xl font-semibold mb-2">
            {isDragActive ? "Drop your images here" : "Upload Label Images"}
          </h3>
          
          <p className="text-muted-foreground max-w-sm mb-6">
            Drag and drop your packaging label images, or click to browse. 
            Supports JPG, PNG up to 10MB.
          </p>
          
          <Button variant="outline" className="pointer-events-none">
            <Image className="w-4 h-4 mr-2" />
            Select Images
          </Button>
        </div>
      </div>

      {/* File Preview */}
      {files.length > 0 && (
        <div className="mt-6 space-y-3 animate-slide-up">
          <div className="flex items-center justify-between">
            <h4 className="font-display font-medium">
              Selected Files ({files.length})
            </h4>
            <Button 
              variant="ghost" 
              size="sm"
              onClick={() => setFiles([])}
            >
              Clear All
            </Button>
          </div>
          
          <div className="grid gap-3">
            {files.map((file, index) => (
              <div 
                key={`${file.name}-${index}`}
                className="flex items-center gap-3 p-3 rounded-lg bg-card border border-border group hover:border-primary/30 transition-colors"
              >
                <div className="w-12 h-12 rounded-lg bg-accent flex items-center justify-center overflow-hidden flex-shrink-0">
                  <img 
                    src={URL.createObjectURL(file)} 
                    alt={file.name}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="font-medium truncate">{file.name}</p>
                  <p className="text-sm text-muted-foreground">
                    {(file.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
                <Button 
                  variant="ghost" 
                  size="icon"
                  className="opacity-0 group-hover:opacity-100 transition-opacity"
                  onClick={() => removeFile(index)}
                >
                  <X className="w-4 h-4" />
                </Button>
              </div>
            ))}
          </div>
          
          <Button 
            variant="hero" 
            size="lg" 
            className="w-full mt-4"
            onClick={handleProcess}
            disabled={isProcessing}
          >
            {isProcessing ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <FileCheck className="w-5 h-5" />
                Process {files.length} Image{files.length > 1 ? 's' : ''}
              </>
            )}
          </Button>
        </div>
      )}
    </div>
  );
}
