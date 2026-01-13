import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { UploadZone } from "@/components/upload/UploadZone";
import { FeatureCard } from "@/components/features/FeatureCard";
import { StatsCard } from "@/components/stats/StatsCard";
import { Button } from "@/components/ui/button";
import { 
  ScanText, 
  Languages, 
  Shield, 
  FileCheck, 
  Zap, 
  Database,
  FileText,
  CheckCircle,
  Clock,
  TrendingUp
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import heroBg from "@/assets/hero-bg.jpg";

const features = [
  {
    icon: ScanText,
    title: "Advanced OCR Engine",
    description: "Powered by Tesseract with support for 100+ languages including Hindi, Urdu, Bengali, and Tamil.",
  },
  {
    icon: Languages,
    title: "Multi-Language Support",
    description: "Process labels in English, Hindi, Nepali, Bengali, Tamil, Marathi, Urdu and more.",
  },
  {
    icon: Shield,
    title: "Compliance Validation",
    description: "Automated checking against country-specific regulatory requirements and mandatory warnings.",
  },
  {
    icon: FileCheck,
    title: "Rule Management",
    description: "Flexible rule engine with version control, regex support, and category-based organization.",
  },
  {
    icon: Zap,
    title: "Fast Processing",
    description: "GPU-accelerated image processing with OpenCV for optimal OCR accuracy.",
  },
  {
    icon: Database,
    title: "Audit Trail",
    description: "Complete audit logging of all processing, decisions, and rule changes for compliance.",
  },
];

const Index = () => {
  const navigate = useNavigate();

  const handleFilesUploaded = (files: File[]) => {
    // Navigate to results page after processing
    navigate("/results");
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative pt-24 pb-16 md:pt-32 md:pb-24 overflow-hidden">
          {/* Background decoration */}
          <div className="absolute inset-0 bg-gradient-to-b from-background via-accent/20 to-background" />
          <div 
            className="absolute inset-0 opacity-10"
            style={{
              backgroundImage: `url(${heroBg})`,
              backgroundSize: 'cover',
              backgroundPosition: 'center',
            }}
          />
          <div className="absolute top-1/4 right-1/4 w-96 h-96 bg-primary/20 rounded-full blur-3xl animate-pulse-slow" />
          <div className="absolute bottom-1/4 left-1/4 w-64 h-64 bg-primary/10 rounded-full blur-3xl animate-pulse-slow" style={{ animationDelay: '2s' }} />
          
          <div className="container relative mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-4xl mx-auto mb-12 md:mb-16">
              <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-accent/50 border border-border mb-6 animate-fade-in">
                <span className="w-2 h-2 rounded-full bg-success animate-pulse" />
                <span className="text-sm text-muted-foreground">Compliance Verification System</span>
              </div>
              
              <h1 className="font-display text-4xl md:text-5xl lg:text-6xl font-bold mb-6 animate-slide-up">
                <span className="gradient-text">OCR-Powered</span>
                <br />
                <span className="text-foreground">Text Compliance System</span>
              </h1>
              
              <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto mb-8 animate-slide-up" style={{ animationDelay: '100ms' }}>
                Automated verification of regulatory labels and packaging text. 
                Upload images, extract text with AI, and validate compliance instantly.
              </p>
              
              <div className="flex flex-col sm:flex-row items-center justify-center gap-4 animate-slide-up" style={{ animationDelay: '200ms' }}>
                <Button variant="hero" size="xl">
                  <ScanText className="w-5 h-5" />
                  Start Scanning
                </Button>
                <Button variant="outline" size="lg">
                  View Documentation
                </Button>
              </div>
            </div>
            
            {/* Stats Row */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 max-w-4xl mx-auto mb-16 animate-slide-up" style={{ animationDelay: '300ms' }}>
              <StatsCard 
                icon={FileText} 
                label="Images Processed" 
                value="12,847"
                trend={{ value: 12, isPositive: true }}
              />
              <StatsCard 
                icon={CheckCircle} 
                label="Compliance Rate" 
                value="98.2%"
                trend={{ value: 3, isPositive: true }}
              />
              <StatsCard 
                icon={Clock} 
                label="Avg. Process Time" 
                value="1.2s"
              />
              <StatsCard 
                icon={TrendingUp} 
                label="Active Rules" 
                value="156"
              />
            </div>
            
            {/* Upload Section */}
            <div className="animate-scale-in" style={{ animationDelay: '400ms' }}>
              <UploadZone onFilesUploaded={handleFilesUploaded} />
            </div>
          </div>
        </section>
        
        {/* Features Section */}
        <section className="py-16 md:py-24 bg-muted/30">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-12">
              <h2 className="font-display text-3xl md:text-4xl font-bold mb-4">
                Powerful Compliance Features
              </h2>
              <p className="text-muted-foreground">
                Everything you need to ensure regulatory compliance for product labels and packaging.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {features.map((feature, index) => (
                <FeatureCard 
                  key={feature.title}
                  icon={feature.icon}
                  title={feature.title}
                  description={feature.description}
                  delay={index * 100}
                />
              ))}
            </div>
          </div>
        </section>
        
        {/* How It Works Section */}
        <section className="py-16 md:py-24">
          <div className="container mx-auto px-4 sm:px-6 lg:px-8">
            <div className="text-center max-w-2xl mx-auto mb-12">
              <h2 className="font-display text-3xl md:text-4xl font-bold mb-4">
                How It Works
              </h2>
              <p className="text-muted-foreground">
                Simple 3-step process to verify compliance of your product labels.
              </p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
              {[
                {
                  step: "01",
                  title: "Upload Images",
                  description: "Upload JPG or PNG images of your product packaging labels.",
                },
                {
                  step: "02",
                  title: "OCR Processing",
                  description: "Our AI extracts text from images with high accuracy across languages.",
                },
                {
                  step: "03",
                  title: "Compliance Check",
                  description: "Automated validation against regulatory rules with instant results.",
                },
              ].map((item, index) => (
                <div key={item.step} className="relative group">
                  <div className="text-7xl font-display font-bold text-primary/10 group-hover:text-primary/20 transition-colors">
                    {item.step}
                  </div>
                  <div className="mt-4">
                    <h3 className="font-display text-xl font-semibold mb-2">{item.title}</h3>
                    <p className="text-muted-foreground">{item.description}</p>
                  </div>
                  {index < 2 && (
                    <div className="hidden md:block absolute top-1/4 -right-4 text-border">
                      →
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        </section>
      </main>
      
      <Footer />
    </div>
  );
};

export default Index;
