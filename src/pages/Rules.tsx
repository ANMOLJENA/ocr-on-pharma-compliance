import { useState } from "react";
import { Navbar } from "@/components/layout/Navbar";
import { Footer } from "@/components/layout/Footer";
import { RuleCard } from "@/components/rules/RuleCard";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { 
  Search, 
  Plus, 
  Filter,
  BookOpen
} from "lucide-react";

// Mock data
const mockRules = [
  {
    id: "1",
    text: "SCHEDULE H DRUG - TO BE SOLD BY RETAIL ON THE PRESCRIPTION OF A REGISTERED MEDICAL PRACTITIONER ONLY",
    country: "India",
    language: "English",
    category: "Warning",
    mandatory: true,
    caseSensitive: false,
    isActive: true,
  },
  {
    id: "2",
    text: "यह दवा केवल चिकित्सक के परामर्श से लें",
    country: "India",
    language: "Hindi",
    category: "Warning",
    mandatory: true,
    caseSensitive: false,
    isActive: true,
  },
  {
    id: "3",
    text: "Store in a cool and dry place away from direct sunlight",
    country: "Global",
    language: "English",
    category: "Storage",
    mandatory: false,
    caseSensitive: false,
    isActive: true,
  },
  {
    id: "4",
    text: "Keep out of reach of children",
    country: "Global",
    language: "English",
    category: "Safety",
    mandatory: true,
    caseSensitive: false,
    isActive: true,
  },
  {
    id: "5",
    text: "Not for sale to persons under 18 years",
    country: "USA",
    language: "English",
    category: "Legal",
    mandatory: true,
    caseSensitive: false,
    isActive: false,
  },
  {
    id: "6",
    text: "Contains nicotine. Nicotine is an addictive chemical",
    country: "USA",
    language: "English",
    category: "Health Warning",
    mandatory: true,
    caseSensitive: false,
    isActive: true,
  },
];

const Rules = () => {
  const [searchQuery, setSearchQuery] = useState("");
  const [rules, setRules] = useState(mockRules);

  const filteredRules = rules.filter((rule) =>
    rule.text.toLowerCase().includes(searchQuery.toLowerCase()) ||
    rule.country.toLowerCase().includes(searchQuery.toLowerCase()) ||
    rule.category.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const toggleRule = (id: string) => {
    setRules(rules.map(rule => 
      rule.id === id ? { ...rule, isActive: !rule.isActive } : rule
    ));
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      
      <main className="flex-1 pt-24 pb-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          {/* Header */}
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-8">
            <div>
              <h1 className="font-display text-3xl md:text-4xl font-bold mb-2">
                Compliance Rules
              </h1>
              <p className="text-muted-foreground">
                Manage controlled text rules for compliance validation.
              </p>
            </div>
            <Button variant="hero">
              <Plus className="w-4 h-4 mr-2" />
              Add Rule
            </Button>
          </div>
          
          {/* Filters */}
          <div className="flex flex-col md:flex-row gap-4 mb-6">
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground" />
              <Input
                placeholder="Search rules by text, country, or category..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="pl-10"
              />
            </div>
            
            <Button variant="outline">
              <Filter className="w-4 h-4 mr-2" />
              Filters
            </Button>
          </div>
          
          {/* Rules Grid */}
          <div className="space-y-4">
            {filteredRules.length > 0 ? (
              filteredRules.map((rule) => (
                <RuleCard
                  key={rule.id}
                  {...rule}
                  onToggle={() => toggleRule(rule.id)}
                  onEdit={() => console.log("Edit rule:", rule.id)}
                  onDelete={() => console.log("Delete rule:", rule.id)}
                />
              ))
            ) : (
              <div className="text-center py-12">
                <BookOpen className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
                <h3 className="font-display text-lg font-medium mb-1">No rules found</h3>
                <p className="text-muted-foreground">
                  Try adjusting your search criteria or add a new rule.
                </p>
              </div>
            )}
          </div>
        </div>
      </main>
      
      <Footer />
    </div>
  );
};

export default Rules;
