import { Link } from "react-router-dom";


export function Footer() {
  return (
    <footer className="border-t border-border/50 bg-card/50">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand */}
          <div className="col-span-1 md:col-span-2">
            <Link to="/" className="flex items-center gap-2 mb-4">
              <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-primary to-primary/70 flex items-center justify-center">
               
              </div>
              <span className="font-display font-bold text-xl">
                <span className="gradient-text">OCR</span>
                <span className="text-foreground">Comply</span>
              </span>
            </Link>
            <p className="text-muted-foreground max-w-sm">
              Automated OCR-based text compliance verification system for regulatory label checking and audit management.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="font-display font-semibold mb-4">Product</h3>
            <ul className="space-y-2 text-muted-foreground">
              <li><Link to="/" className="hover:text-primary transition-colors">Upload</Link></li>
              <li><Link to="/results" className="hover:text-primary transition-colors">Results</Link></li>
              <li><Link to="/rules" className="hover:text-primary transition-colors">Rules</Link></li>
              <li><Link to="/analytics" className="hover:text-primary transition-colors">Analytics</Link></li>
            </ul>
          </div>

          {/* Resources */}
          <div>
            <h3 className="font-display font-semibold mb-4">Resources</h3>
            <ul className="space-y-2 text-muted-foreground">
              <li><a href="#" className="hover:text-primary transition-colors">Documentation</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">API Reference</a></li>
              <li><a href="#" className="hover:text-primary transition-colors">Support</a></li>
            </ul>
          </div>
        </div>

        <div className="flex flex-col md:flex-row items-center justify-between mt-12 pt-8 border-t border-border/50">
          <p className="text-sm text-muted-foreground">
          
          </p>
          <div className="flex items-center gap-4 mt-4 md:mt-0">
            <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
             
            </a>
            <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
               
            </a>
            <a href="#" className="text-muted-foreground hover:text-primary transition-colors">
              
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
}
