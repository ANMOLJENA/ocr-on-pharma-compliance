import { CheckCircle2, XCircle, AlertTriangle, Eye, MoreVertical } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

export type ComplianceStatus = "pass" | "fail" | "warning";

interface ComplianceResultCardProps {
  id: string;
  imageName: string;
  imageUrl: string;
  status: ComplianceStatus;
  extractedText: string;
  matchedRules: number;
  totalRules: number;
  timestamp: string;
  onView?: () => void;
}

const statusConfig = {
  pass: {
    icon: CheckCircle2,
    label: "Compliant",
    className: "bg-success/10 text-success border-success/20",
    iconColor: "text-success",
  },
  fail: {
    icon: XCircle,
    label: "Non-Compliant",
    className: "bg-destructive/10 text-destructive border-destructive/20",
    iconColor: "text-destructive",
  },
  warning: {
    icon: AlertTriangle,
    label: "Review Required",
    className: "bg-warning/10 text-warning border-warning/20",
    iconColor: "text-warning",
  },
};

export function ComplianceResultCard({
  imageName,
  imageUrl,
  status,
  extractedText,
  matchedRules,
  totalRules,
  timestamp,
  onView,
}: ComplianceResultCardProps) {
  const config = statusConfig[status];
  const StatusIcon = config.icon;

  return (
    <div className="group p-4 rounded-xl bg-card border border-border hover:border-primary/30 transition-all duration-300 hover:shadow-lg hover:shadow-primary/5">
      <div className="flex gap-4">
        {/* Image thumbnail */}
        <div className="w-20 h-20 rounded-lg bg-muted overflow-hidden flex-shrink-0">
          <img 
            src={imageUrl} 
            alt={imageName}
            className="w-full h-full object-cover"
          />
        </div>
        
        {/* Content */}
        <div className="flex-1 min-w-0">
          <div className="flex items-start justify-between gap-2">
            <div>
              <h4 className="font-medium truncate">{imageName}</h4>
              <p className="text-xs text-muted-foreground mt-0.5">{timestamp}</p>
            </div>
            <Badge className={cn("flex-shrink-0", config.className)}>
              <StatusIcon className={cn("w-3 h-3 mr-1", config.iconColor)} />
              {config.label}
            </Badge>
          </div>
          
          <p className="text-sm text-muted-foreground mt-2 line-clamp-2">
            {extractedText}
          </p>
          
          <div className="flex items-center justify-between mt-3">
            <div className="flex items-center gap-2">
              <span className="text-xs text-muted-foreground">
                Rules matched:
              </span>
              <span className={cn(
                "text-xs font-medium",
                matchedRules === totalRules ? "text-success" : "text-warning"
              )}>
                {matchedRules}/{totalRules}
              </span>
            </div>
            
            <div className="flex gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
              <Button variant="ghost" size="sm" onClick={onView}>
                <Eye className="w-4 h-4 mr-1" />
                View
              </Button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
