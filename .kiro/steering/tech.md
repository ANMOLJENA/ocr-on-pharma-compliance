# Technology Stack

## Frontend
- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **Styling**: Tailwind CSS + shadcn/ui components
- **Routing**: React Router DOM
- **State Management**: TanStack Query (React Query)
- **Forms**: React Hook Form with Zod validation
- **Charts**: Recharts
- **File Upload**: React Dropzone

## Backend
- **Framework**: Flask (Python)
- **Database**: SQLite (development), PostgreSQL (production)
- **ORM**: SQLAlchemy with Flask-SQLAlchemy
- **OCR Engines**: 
  - Tesseract (local, free)
  - Azure Computer Vision (cloud)
  - Google Cloud Vision (cloud)
  - AWS Textract (cloud)
- **Image Processing**: OpenCV, Pillow, NumPy
- **PDF Processing**: PyPDF2, pdf2image
- **CORS**: Flask-CORS

## Development Tools
- **TypeScript**: Strict type checking
- **ESLint**: Code linting
- **Prettier**: Code formatting (via Lovable)
- **Path Aliases**: `@/` for src directory

## Common Commands

### Frontend Development
```bash
# Install dependencies
npm install

# Start development server (port 8080)
npm run dev

# Build for production
npm run build

# Build for development
npm run build:dev

# Lint code
npm run lint

# Preview production build
npm run preview
```

### Backend Development
```bash
# Navigate to backend
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Setup database and rules
python setup.py

# Test OCR installation
python test_tesseract.py

# Start development server (port 5000)
python app.py

# Quick start (Windows)
start_server.bat

# Quick start (Linux/Mac)
./start_server.sh
```

### Full Stack Development
Run both servers simultaneously:
- Frontend: `npm run dev` (http://localhost:8080)
- Backend: `cd backend && python app.py` (http://localhost:5000)

## Configuration
- Frontend config: `vite.config.ts`, `tsconfig.json`
- Backend config: `backend/config.py`, `backend/.env`
- UI components: `components.json` (shadcn/ui)
- Styling: `tailwind.config.ts`, `postcss.config.js`