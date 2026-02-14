import { useState } from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { FileUploadWithAPI } from "@/components/upload/FileUploadWithAPI";
import { DashboardStats } from "@/components/dashboard/DashboardStats";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import { 
  ScanText, 
  AlertCircle,
  CheckCircle2
} from "lucide-react";
import { useHealthCheck } from "@/hooks/use-api";
import type { OCRResult } from "@/types/api";
import heroBg from "@/assets/hero-bg.jpg";

const IndexIntegrated = () => {
  const [showUpload, setShowUpload] = useState(false);
  const [uploadResult, setUploadResult] = useState<OCRResult | null>(null);
  const { healthy, checking } = useHealthCheck();

  const handleUploadSuccess = (result: OCRResult) => {
    setUploadResult(result);
    setShowUpload(false);
    // Scroll to results
    setTimeout(() => {
      document.getElementById('results')?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      {/* Backend Status Banner */}
      {!checking && (
        <div className={healthy ? "bg-green-50 border-b border-green-200" : "bg-red-50 border-b border-red-200"}>
          <div className="container mx-auto px-4 py-2">
            <div className="flex items-center justify-center gap-2">
              {healthy ? (
                <>
                  <CheckCircle2 className="h-4 w-4 text-green-600" />
                  <p className="text-sm text-green-800">Backend connected (http://localhost:5000)</p>
                </>
              ) : (
                <>
                  <AlertCircle className="h-4 w-4 text-red-600" />
                  <p className="text-sm text-red-800">
                    Backend server not responding. Please start: cd backend && python app.py
                  </p>
                </>
              )}
            </div>
          </div>
        </div>
      )}
      
      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative pt-24 pb-16 md:pt-32 md:pb-24 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-to-b from-background via-accent/20 to-background" />
          <div 
            className="absolute inset-0 opacity-10"
            style={{
              backgroundImage: `url(${heroBg})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
            }}
          />
          
          <div className="container relative mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-4xl mx-auto mb-12">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent/50 border border-border mb-6">
                <span className={`w-2 h-2 rounded-full ${healthy ? 'bg-success animate-pulse' : 'bg-destructive'}`} />
                <span className="text-sm text-muted-foreground">
                  {healthy ? 'System Online' : 'System Offline'}
                </span>
              </div>
              
              <h1 className="font-display text-4xl md:text-5xl lg:text-6xl font-bold mb-6">
                <span className="gradient-text">OCR-Powered</span>
                <br />
                <span className="text-foreground">Pharmaceutical Compliance</span>
              </h1>
              
              <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-8">
                Automated pharmaceutical document processing with intelligent compliance checking.
                Upload labels, extract text with AI, and validate compliance instantly.
              </p>
              
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
                <Button 
                  variant="hero" 
                  size="xl"
                  onClick={() => setShowUpload(!showUpload)}
                  disabled={!healthy}
                >
                  <ScanText className="w-5 h-5" />
                  {showUpload ? 'Hide Upload' : 'Upload Document'}
                </Button>
                <Button variant="outline" size="lg" onClick={() => {
                  document.getElementById('dashboard')?.scrollIntoView({ behavior: 'smooth' });
                }}>
                  View Dashboard
                </Button>
              </div>
            </div>
            
            {/* Upload Section */}
            {showUpload && healthy && (
              <div className="max-w-3xl mx-auto animate-scale-in">
                <Card>
                  <CardHeader>
                    <CardTitle>Upload Pharmaceutical Document</CardTitle>
                    <CardDescription>
                      Upload an image or PDF of a pharmaceutical label for OCR processing
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <FileUploadWithAPI onUploadSuccess={handleUploadSuccess} />
                  </CardContent>
                </Card>
              </div>
            )}
          </div>
        </section>

        {/* Upload Result */}
        {uploadResult && (
          <section id="results" className="py-12 bg-muted/30">
            <div className="container mx-auto px-4">
              <h2 className="text-3xl font-bold mb-6 text-center">Processing Results</h2>
              <div className="max-w-4xl mx-auto">
                <Card>
                  <CardHeader>
                    <CardTitle>OCR Extraction Complete</CardTitle>
                    <CardDescription>
                      Document ID: {uploadResult.document_id} | Result ID: {uploadResult.id}
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-muted-foreground">Confidence Score</p>
                        <p className="text-2xl font-bold">{(uploadResult.confidence_score * 100).toFixed(1)}%</p>
                      </div>
                      <div>
                        <p className="text-sm text-muted-foreground">Processing Time</p>
                        <p className="text-2xl font-bold">{uploadResult.processing_time.toFixed(2)}s</p>
                      </div>
                    </div>

                    {uploadResult.drug_name && (
                      <div>
                        <p className="text-sm text-muted-foreground">Drug Name</p>
                        <p className="font-medium">{uploadResult.drug_name}</p>
                      </div>
                    )}

                    {uploadResult.batch_number && (
                      <div>
                        <p className="text-sm text-muted-foreground">Batch Number</p>
                        <p className="font-medium">{uploadResult.batch_number}</p>
                      </div>
                    )}

                    {uploadResult.expiry_date && (
                      <div>
                        <p className="text-sm text-muted-foreground">Expiry Date</p>
                        <p className="font-medium">{uploadResult.expiry_date}</p>
                      </div>
                    )}

                    {uploadResult.manufacturer && (
                      <div>
                        <p className="text-sm text-muted-foreground">Manufacturer</p>
                        <p className="font-medium">{uploadResult.manufacturer}</p>
                      </div>
                    )}

                    {uploadResult.controlled_substance && (
                      <Alert className="border-orange-200 bg-orange-50">
                        <AlertCircle className="h-4 w-4 text-orange-600" />
                        <AlertDescription className="text-orange-800">
                          Controlled Substance Detected
                        </AlertDescription>
                      </Alert>
                    )}

                    <div>
                      <p className="text-sm text-muted-foreground mb-2">Extracted Text</p>
                      <div className="bg-muted p-4 rounded-lg max-h-64 overflow-y-auto">
                        <pre className="text-sm whitespace-pre-wrap">{uploadResult.extracted_text}</pre>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </div>
            </div>
          </section>
        )}
        
        {/* Dashboard Section */}
        {healthy && (
          <section id="dashboard" className="py-16 md:py-24">
            <div className="container mx-auto px-4">
              <h2 className="text-3xl font-bold mb-8 text-center">System Dashboard</h2>
              <DashboardStats />
            </div>
          </section>
        )}
      </main>
      
      <Footer />
    </div>
  );
};

export default IndexIntegrated;
