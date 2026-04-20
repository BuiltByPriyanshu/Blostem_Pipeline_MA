# Contributing to Blostem Pipeline

Thank you for your interest in contributing! Here's how to get started.

## Development Setup

### Backend

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Initialize database
python seed.py

# Start development server
cd backend
uvicorn main:app --reload
```

### Frontend

```bash
# Install dependencies
cd frontend
npm install

# Start development server
npm run dev
```

## Code Style

### Python
- Follow PEP 8
- Use type hints where possible
- Keep functions focused and small
- Add docstrings to public functions

### JavaScript/React
- Use ES6+ syntax
- Follow React best practices
- Use functional components with hooks
- Keep components focused and reusable

## Testing

### Backend
```bash
# Run database tests
python -c "from backend.db import init_db, seed_prospects, seed_partners; init_db(); seed_prospects(); seed_partners()"

# Test API endpoints
curl http://localhost:8000/api/prospects/pipeline
```

### Frontend
```bash
# Build frontend
cd frontend
npm run build
```

## Commit Messages

Use clear, descriptive commit messages:
- `feat: add email sending feature`
- `fix: correct stall detection logic`
- `docs: update README with setup instructions`
- `refactor: simplify prospect scoring algorithm`

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'feat: add amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## Reporting Issues

When reporting issues, please include:
- Description of the problem
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment (OS, Python version, Node version)

## Questions?

Feel free to open an issue or discussion for questions about the project.

Thank you for contributing!
