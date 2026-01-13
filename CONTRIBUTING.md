# Contributing to Selenium Pytest Automation Framework

Thank you for your interest in contributing to this project! This document provides guidelines and best practices for contributing.

## Code of Conduct

By participating in this project, you agree to maintain a respectful and collaborative environment.

## Getting Started

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/Demo-POM.git`
3. Create a feature branch: `git checkout -b feature/your-feature-name`
4. Make your changes
5. Run tests to ensure everything works
6. Commit your changes: `git commit -m "Add your feature"`
7. Push to your fork: `git push origin feature/your-feature-name`
8. Create a Pull Request

## Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest
```

## Coding Standards

### Python Style Guide

- Follow PEP 8 style guide
- Use meaningful variable and function names
- Add docstrings to all classes and functions
- Keep functions small and focused
- Maximum line length: 100 characters

### Page Object Model Guidelines

1. **Locators**: Define all locators as class variables at the top
2. **Methods**: Each method should perform a single action
3. **Error Handling**: Use custom exceptions for better error messages
4. **Waits**: Use explicit waits, avoid implicit waits and sleep()
5. **Inheritance**: All page objects should inherit from BasePage

### Test Guidelines

1. **Naming**: Use descriptive test names following pattern `test_STORY_ID_description`
2. **Markers**: Add appropriate pytest markers (@pytest.mark.story, @pytest.mark.P1, etc.)
3. **Documentation**: Include docstrings with story ID, persona, priority, and description
4. **Assertions**: Use clear assertion messages
5. **Data**: Use CSV files for data-driven tests
6. **Independence**: Tests should be independent and not rely on execution order

## Adding New Features

### Adding a New Page Object

1. Create a new file in `src/pages/`
2. Inherit from `BasePage`
3. Define locators as class variables
4. Implement methods for page interactions
5. Add error handling
6. Document all methods

Example:
```python
from selenium.webdriver.common.by import By
from src.pages.base_page import BasePage

class NewPage(BasePage):
    # Locators
    ELEMENT = (By.ID, "element_id")
    
    def perform_action(self):
        """Perform specific action on the page."""
        self.click(*self.ELEMENT)
```

### Adding New Tests

1. Create test methods in appropriate test file
2. Add pytest markers for traceability
3. Update `traceability.json`
4. Add test data to CSV if needed
5. Document test purpose and expected behavior

Example:
```python
@pytest.mark.story("STORY-ID")
@pytest.mark.P1
def test_new_feature(self, driver, base_url):
    """
    Test: STORY-ID - Feature description
    Persona: User type
    Priority: P1
    Description: Detailed test description
    """
    # Test implementation
    pass
```

### Adding Test Data

1. Add data to appropriate CSV file in `tests/data/`
2. Ensure CSV headers match parameter names
3. Include scenario identifiers
4. Document data format in comments

## Testing Your Changes

### Run All Tests
```bash
pytest
```

### Run Specific Tests
```bash
pytest tests/test_login.py
pytest -m story_AUTH_001
pytest -k "test_valid_login"
```

### Run with Coverage
```bash
pip install pytest-cov
pytest --cov=src --cov-report=html
```

### Run Linting
```bash
pip install flake8 pylint
flake8 src/ tests/
pylint src/ tests/
```

## Pull Request Guidelines

### Before Submitting

- [ ] All tests pass locally
- [ ] Code follows style guidelines
- [ ] New tests added for new features
- [ ] Documentation updated
- [ ] Traceability.json updated
- [ ] No credentials or secrets in code
- [ ] Commit messages are clear and descriptive

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #issue_number

## Testing
Describe testing performed

## Checklist
- [ ] Tests pass
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] Traceability updated
```

## Reporting Issues

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment details (OS, Python version, browser)
- Screenshots if applicable
- Error logs

### Feature Requests

Include:
- Clear description of the feature
- Use case and benefits
- Proposed implementation (optional)
- Examples or mockups (optional)

## Documentation

### Code Documentation

- Add docstrings to all classes and functions
- Use clear and concise language
- Include parameter descriptions
- Document return values
- Add usage examples for complex functions

### README Updates

- Keep README.md up to date
- Update setup instructions if dependencies change
- Add new features to feature list
- Update troubleshooting section as needed

## Security

### Credential Handling

- Never commit credentials or tokens
- Use environment variables for sensitive data
- Add credential files to .gitignore
- Sanitize logs to remove sensitive information

### Dependency Management

- Keep dependencies up to date
- Review security advisories
- Use specific version numbers in requirements.txt
- Test thoroughly after dependency updates

## Review Process

1. **Automated Checks**: CI/CD pipeline runs automatically
2. **Code Review**: At least one maintainer reviews the code
3. **Testing**: Reviewer verifies tests pass and coverage is adequate
4. **Documentation**: Reviewer checks documentation is complete
5. **Approval**: Maintainer approves and merges PR

## Release Process

1. Update version number
2. Update CHANGELOG.md
3. Create release branch
4. Run full test suite
5. Create GitHub release
6. Tag release
7. Merge to main

## Questions?

If you have questions:
- Open an issue for discussion
- Contact maintainers
- Check existing documentation

## License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

Thank you for contributing!