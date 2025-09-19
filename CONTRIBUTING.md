# Contributing to Dark Web Search Tool

We welcome contributions from all team members! This document outlines the process for contributing to the project.

## Team Responsibilities

### Team Member Roles

- **Team Member 1**: [Name] - Project Lead & Backend Development
  - Overall project coordination
  - Core search engine implementation
  - Database design and management

- **Team Member 2**: [Name] - Frontend Development & UI/UX
  - User interface design and implementation
  - Frontend JavaScript development
  - User experience optimization

- **Team Member 3**: [Name] - Web Crawling & Data Processing
  - Web crawler implementation
  - Content parsing and processing
  - Data pipeline development

- **Team Member 4**: [Name] - Testing & Documentation
  - Test suite development and maintenance
  - Documentation writing and updates
  - Quality assurance and code review

## Development Workflow

### 1. Setting Up Your Development Environment

```bash
# Clone the repository
git clone https://github.com/Tomatenmark05/darkwebsearch.git
cd darkwebsearch

# Run the setup script
python scripts/setup.py

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Start development
python src/app.py
```

### 2. Branch Naming Convention

Use the following naming convention for branches:

- `feature/feature-name` - New features
- `bugfix/bug-description` - Bug fixes
- `hotfix/critical-fix` - Critical fixes
- `docs/documentation-update` - Documentation updates

Examples:
- `feature/advanced-search`
- `bugfix/search-results-pagination`
- `docs/api-documentation`

### 3. Commit Message Format

Use clear and descriptive commit messages:

```
type(scope): description

Examples:
feat(search): add TF-IDF scoring algorithm
fix(crawler): handle timeout errors properly
docs(readme): update installation instructions
test(parser): add content parsing test cases
```

### 4. Pull Request Process

1. Create a feature branch from `main`
2. Make your changes with appropriate tests
3. Ensure all tests pass: `pytest tests/`
4. Update documentation if needed
5. Create a pull request with:
   - Clear description of changes
   - Link to any related issues
   - Screenshots for UI changes
6. Request review from at least one other team member
7. Address review feedback
8. Merge after approval

## Code Standards

### Python Code Style

- Follow PEP 8 guidelines
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Keep functions small and focused
- Use type hints where appropriate

Example:
```python
def parse_content(self, html_content: str, url: str = None) -> dict:
    """
    Parse HTML content and extract structured data.
    
    Args:
        html_content (str): Raw HTML content to parse
        url (str, optional): Source URL for context
        
    Returns:
        dict: Parsed content with metadata
    """
```

### Frontend Code Style

- Use consistent indentation (2 spaces)
- Use meaningful variable names
- Add comments for complex logic
- Follow modern JavaScript practices (ES6+)
- Use Bootstrap classes for consistent styling

### Testing Guidelines

- Write tests for all new features
- Aim for at least 80% code coverage
- Use descriptive test names
- Test both success and failure cases
- Mock external dependencies

Example:
```python
def test_search_with_multiple_terms(self):
    """Test search functionality with multiple query terms"""
    # Setup, action, assertion
```

## Project Structure Guidelines

### Adding New Features

When adding new features:

1. **Backend**: Add to appropriate module in `src/`
2. **Frontend**: Update templates and static files
3. **Tests**: Add comprehensive test coverage
4. **Documentation**: Update relevant documentation

### File Organization

- Keep related functionality together
- Use clear file and directory names
- Avoid deep nesting of directories
- Separate concerns appropriately

## Communication Guidelines

### Daily Standups

Brief daily check-ins to discuss:
- What you worked on yesterday
- What you plan to work on today
- Any blockers or challenges

### Code Reviews

- Be constructive and respectful
- Focus on code quality and functionality
- Suggest improvements, don't just point out problems
- Respond to feedback promptly

### Issue Tracking

Use GitHub Issues to track:
- Feature requests
- Bug reports
- Tasks and assignments
- Project milestones

## Legal and Ethical Guidelines

### Important Reminders

- This project is for educational purposes only
- Respect website terms of service and robots.txt
- Do not download or store illegal content
- Follow all applicable laws and regulations
- Maintain ethical standards in all development

### Data Handling

- No personal information should be stored
- Implement appropriate data sanitization
- Respect privacy and data protection laws
- Document data sources and usage

## Getting Help

### Resources

- Project documentation in `docs/` directory
- Code examples in existing modules
- Test cases for reference implementations
- Team members via GitHub issues or discussions

### Troubleshooting

Common issues and solutions:

1. **Database errors**: Check if database is properly initialized
2. **Import errors**: Ensure virtual environment is activated
3. **Test failures**: Run individual tests to isolate issues
4. **Dependency conflicts**: Try recreating virtual environment

### Contact

For questions or support:
- Create a GitHub issue for bugs or feature requests
- Use GitHub Discussions for general questions
- Contact team lead for urgent matters

## Recognition

All team members will be credited for their contributions in:
- Project documentation
- Code comments where appropriate
- Final project presentation
- Academic submissions

Thank you for contributing to the Dark Web Search Tool project!