# SocialHubAPI Documentation

This directory contains the complete documentation for the SocialHubAPI project, built with MkDocs and Material theme.

## Structure

```
docs/
├── mkdocs.yml              # MkDocs configuration
├── docs/                   # Documentation content
│   ├── index.md           # Homepage
│   ├── quickstart.md      # Quick start guide
│   ├── api/               # API documentation
│   │   ├── posts.md       # Posts API
│   │   ├── users.md       # Users API
│   │   ├── social.md      # Social features
│   │   └── search.md      # User search
│   └── auth/              # Authentication
│       └── index.md       # Auth system
└── site/                  # Built documentation (generated)
```

## Development

### Prerequisites
- Python 3.12+
- Virtual environment activated
- MkDocs and Material theme installed

### Setup
```bash
# Activate virtual environment
source ../venv/bin/activate

# Install MkDocs dependencies
pip install mkdocs mkdocs-material

# Serve documentation locally
mkdocs serve

# Build documentation
mkdocs build
```

### Adding Content

1. **New Pages**: Create `.md` files in the appropriate directory
2. **Navigation**: Update `mkdocs.yml` to include new pages
3. **Links**: Use relative paths for internal links
4. **Images**: Place images in `docs/images/` and reference with `![Alt](images/filename.png)`

### Writing Guidelines

- Use clear, descriptive headings
- Include code examples with syntax highlighting
- Add cross-references between related sections
- Keep content up-to-date with API changes
- Use consistent formatting and style

## Configuration

The documentation is configured in `mkdocs.yml` with:

- **Theme**: Material Design
- **Features**: Search, navigation tabs, code highlighting
- **Extensions**: Admonitions, code blocks, tables, emojis
- **Navigation**: Hierarchical structure with sections

## Deployment

### Local Development
```bash
mkdocs serve
# Documentation available at http://localhost:8000
```

### Production Build
```bash
mkdocs build
# Static files generated in site/ directory
```

### GitHub Pages
```bash
mkdocs gh-deploy
# Deploys to GitHub Pages automatically
```

## Features

### Navigation
- **Home**: Overview and quick start
- **API Reference**: Complete API documentation
- **Authentication**: Security and auth guides
- **Quick Start**: Getting started guide
- 
### Search
- Full-text search across all documentation
- Highlighted search results

### Code Examples
- Syntax highlighting for multiple languages
- Copy-to-clipboard functionality
- Inline code and code blocks

### Responsive Design
- Mobile-friendly layout
- Dark/light theme toggle
- Collapsible navigation

## Related Files

- `../README.md` - Main project README
- `../POSTS_API.md` - Original posts API docs
- `../USERS_API.md` - Original users API docs
- `../SOCIAL_FEATURES.md` - Original social features docs
- `../AUTHENTICATION.md` - Original authentication docs