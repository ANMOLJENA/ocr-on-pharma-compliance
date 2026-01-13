import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { StatsCard } from "@/components/stats/StatsCard";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { FileText, CheckCircle, Clock, TrendingUp, Activity } from "lucide-react";
import React, { useState } from "react";

const PARAMETERS = [
  { value: "timestamp", label: "Timestamp" },
  { value: "confidence", label: "Confidence" },
  { value: "textLength", label: "Text length" },
  { value: "ruleMatches", label: "Rule matches" },
];

const Analytics = () => {
  const [xParam, setXParam] = useState(PARAMETERS[0].value);
  const [yParam, setYParam] = useState(PARAMETERS[1].value);

  const handleApply = () => {
    localStorage.setItem("analyticsMapping", JSON.stringify({ x: xParam, y: yParam }));
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />

      <main className="flex-1 pt-24 pb-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h1 className="font-display text-3xl md:text-4xl font-bold mb-2">
              Analytics — Parameter mapping
            </h1>
            <p className="text-muted-foreground">Select parameters for X and Y axes.</p>
          </div>

          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
            <StatsCard icon={FileText} label="Total Processed" value="-" />
            <StatsCard icon={CheckCircle} label="Compliance Rate" value="-" />
            <StatsCard icon={Clock} label="Avg. Process Time" value="-" />
            <StatsCard icon={TrendingUp} label="Active Rules" value="-" />
          </div>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="w-5 h-5 text-primary" />
                Parameter Mapping
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 max-w-md">
                <label>
                  <div className="mb-1">X axis</div>
                  <select value={xParam} onChange={(e) => setXParam(e.target.value)} className="w-full">
                    {PARAMETERS.map((p) => (
                      <option key={p.value} value={p.value}>
                        {p.label}
                      </option>
                    ))}
                  </select>
                </label>

                <label>
                  <div className="mb-1">Y axis</div>
                  <select value={yParam} onChange={(e) => setYParam(e.target.value)} className="w-full">
                    {PARAMETERS.map((p) => (
                      <option key={p.value} value={p.value}>
                        {p.label}
                      </option>
                    ))}
                  </select>
                </label>
              </div>

              <div className="mt-4">
                <button onClick={handleApply} className="btn">
                  Apply
                </button>
              </div>

              <div className="mt-6">
                <strong>Selected mapping:</strong>
                <div>X: {xParam}</div>
                <div>Y: {yParam}</div>
              </div>
            </CardContent>
          </Card>
        </div>
      </main>

      <Footer />
    </div>
  );
};

export default Analytics;
