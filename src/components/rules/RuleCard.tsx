import { Globe, Languages, ToggleLeft, ToggleRight, Edit, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface RuleCardProps {
  id: string;
  text: string;
  country: string;
  language: string;
  category: string;
  mandatory: boolean;
  isActive: boolean;
  onToggle?: () => void;
  onEdit?: () => void;
  onDelete?: () => void;
}

export function RuleCard({
  text,
  country,
  language,
  category,
  mandatory,
  isActive,
  onToggle,
  onEdit,
  onDelete,
}: RuleCardProps) {
  return (
    <div className={cn(
      "p-4 rounded-xl border transition-all duration-300",
      isActive 
        ? "bg-card border-border hover:border-primary/30" 
        : "bg-muted/50 border-muted"
    )}>
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap mb-2">
            <Badge variant="outline" className="gap-1">
              <Globe className="w-3 h-3" />
              {country}
            </Badge>
            <Badge variant="outline" className="gap-1">
              <Languages className="w-3 h-3" />
              {language}
            </Badge>
            <Badge variant="secondary">{category}</Badge>
            {mandatory && (
              <Badge className="bg-destructive/10 text-destructive border-destructive/20">
                Mandatory
              </Badge>
            )}
          </div>
          
          <p className={cn(
            "font-medium",
            !isActive && "text-muted-foreground"
          )}>
            -
          </p>
          
          <p className="text-xs text-muted-foreground mt-2">
            Coming soon
          </p>
        </div>
        
        <div className="flex items-center gap-1">
          <Button
            variant="ghost"
            size="icon"
            onClick={onToggle}
            className={cn(
              "transition-colors",
              isActive ? "text-primary" : "text-muted-foreground"
            )}
          >
            {isActive ? (
              <ToggleRight className="w-5 h-5" />
            ) : (
              <ToggleLeft className="w-5 h-5" />
            )}
          </Button>
          <Button variant="ghost" size="icon" onClick={onEdit}>
            <Edit className="w-4 h-4" />
          </Button>
          <Button variant="ghost" size="icon" onClick={onDelete}>
            <Trash2 className="w-4 h-4 text-destructive" />
          </Button>
        </div>
      </div>
    </div>
  );
}
