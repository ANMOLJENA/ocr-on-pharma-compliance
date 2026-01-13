import { useState } from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
// import { ComplianceStatus } from "@/components/results/ComplianceResultCard"; // removed to avoid type mismatch
import { StatsCard } from "@/components/stats/StatsCard";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import {
  Search,
  Download,
  CheckCircle,
  XCircle,
  AlertTriangle,
  FileText,
} from "lucide-react";

type FilterStatus = "all" | "pass" | "fail" | "warning";

const Results = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [filterStatus, setFilterStatus] = useState<FilterStatus>("all");

  const STATUSES: FilterStatus[] = ["all", "pass", "fail", "warning"];

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1 pt-24 pb-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="mb-8">
            <h1 className="font-display text-3xl md:text-4xl font-bold mb-2">
              Compliance Results
            </h1>
            <p className="text-muted-foreground">
              Review and manage OCR processing results and compliance status.
            </p>
          </div>

          {/* Stats – show "-" since no data yet */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <StatsCard icon={FileText} label="Total Processed" value="-" />
            <StatsCard
              icon={CheckCircle}
              label="Compliant"
              value="-"
              className="border-success/30"
            />
            <StatsCard
              icon={XCircle}
              label="Non-Compliant"
              value="-"
              className="border-destructive/30"
            />
            <StatsCard
              icon={AlertTriangle}
              label="Review Required"
              value="-"
              className="border-warning/30"
            />
          </div>

          {/* Filters – UI only for now */}
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search by filename or text..."
                value={searchQuery}
                onChange={(e) => setSearchQuery((e.target as HTMLInputElement).value)}
                className="pl-10"
              />
            </div>

            <div className="flex gap-2">
              {STATUSES.map((status) => (
                <Button
                  key={status}
                  variant={filterStatus === status ? "default" : "outline"}
                  size="sm"
                  onClick={() => setFilterStatus(status)}
                >
                  {status === "all"
                    ? "All"
                    : status === "pass"
                    ? "Compliant"
                    : status === "fail"
                    ? "Failed"
                    : "Warning"}
                </Button>
              ))}
            </div>

            <Button variant="outline" className="ml-auto">
              <Download className="w-4 h-4 mr-2" />
              Export
            </Button>
          </div>

          {/* Empty results area */}
          <div className="border rounded-lg p-8 flex items-center justify-center text-muted-foreground">
            <p>Results will appear here.</p>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Results;
