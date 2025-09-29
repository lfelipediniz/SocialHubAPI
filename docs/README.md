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


## Configuration

The documentation is configured in `mkdocs.yml` with:

- **Theme**: Material Design
- **Features**: Search, navigation tabs, code highlighting
- **Extensions**: Admonitions, code blocks, tables, emojis
- **Navigation**: Hierarchical structure with sections

## Deployment


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