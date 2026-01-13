# Project Structure

## Root Directory Organization
```
ocr-compliance-system/
├── src/                    # Frontend React application
├── backend/               # Flask API server
├── public/               # Static assets
├── dist/                 # Build output
├── node_modules/         # Frontend dependencies
└── docs/                 # Project documentation
```

## Frontend Structure (`src/`)
```
src/
├── components/           # Reusable UI components
│   ├── ui/              # shadcn/ui base components
│   ├── upload/          # File upload components
│   ├── dashboard/       # Dashboard-specific components
│   ├── results/         # Results display components
│   ├── rules/           # Rules management components
│   ├── features/        # Feature showcase components
│   ├── stats/           # Statistics components
│   └── layout/          # Layout components
├── pages/               # Route components
├── services/            # API service layer
├── hooks/               # Custom React hooks
├── types/               # TypeScript type definitions
├── config/              # Configuration files
├── lib/                 # Utility functions
└── assets/              # Images and static files
```

## Backend Structure (`backend/`)
```
backend/
├── models/              # Database models (SQLAlchemy)
├── services/            # Business logic layer
│   ├── ocr_service.py          # OCR processing
│   ├── compliance_service.py   # Compliance validation
│   └── error_detection_service.py # Error detection
├── routes/              # API route handlers
│   ├── ocr_routes.py           # OCR endpoints
│   ├── analytics_routes.py     # Analytics endpoints
│   └── rules_routes.py         # Rules management
├── uploads/             # File storage directory
├── instance/            # Database files
├── logs/                # Application logs
├── examples/            # Usage examples
└── __pycache__/         # Python cache
```

## Key Architecture Patterns

### Frontend Patterns
- **Component Organization**: Group by feature/domain, not by type
- **API Layer**: Centralized service classes with type safety
- **State Management**: TanStack Query for server state, React state for UI
- **Routing**: File-based routing with React Router
- **Styling**: Utility-first with Tailwind, component variants with CVA

### Backend Patterns
- **Layered Architecture**: Routes → Services → Models
- **Blueprint Organization**: Feature-based route grouping
- **Service Layer**: Business logic separated from route handlers
- **Configuration**: Environment-based config with `.env` files
- **Database**: SQLAlchemy ORM with migration support

### File Naming Conventions
- **Frontend**: PascalCase for components (`UserProfile.tsx`)
- **Backend**: snake_case for Python files (`ocr_service.py`)
- **Types**: Descriptive interfaces (`ApiResponse`, `OCRResult`)
- **Hooks**: Prefixed with `use` (`useApi`, `useMobile`)

### Import Patterns
- **Frontend**: Use `@/` alias for src imports
- **Backend**: Relative imports within modules
- **Types**: Centralized in `src/types/` directory
- **Services**: Singleton pattern for API services

### Database Schema
- **6 Core Tables**: documents, ocr_results, compliance_checks, error_detections, compliance_rules, audit_logs
- **Relationships**: Foreign keys with proper constraints
- **Indexing**: Performance optimization on frequently queried fields