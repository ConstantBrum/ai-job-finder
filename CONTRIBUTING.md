# Contributing to LinkedIn Job Finder Agent

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🔒 Safety First

All contributions must maintain the project's safety and compliance guidelines:

1. **Never harvest credentials** - No code that attempts to access, store, or transmit user credentials
2. **Respect site policies** - All automation must include human-like pacing
3. **User confirmation** - Any irreversible actions must require explicit user confirmation
4. **Local only** - All data must remain on the user's local machine
5. **Transparency** - All actions must be logged for user visibility

## 📋 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a welcoming environment

## 🐛 Reporting Issues

When reporting issues, please include:

1. A clear description of the problem
2. Steps to reproduce
3. Expected vs actual behavior
4. Your environment (OS, Node.js version, etc.)
5. Any relevant logs or screenshots

## 💡 Suggesting Features

Feature suggestions should:

1. Align with the project's safety guidelines
2. Be clearly described with use cases
3. Consider impact on existing functionality
4. Include potential implementation approach if possible

## 🔧 Development Setup

```bash
# Clone the repository
git clone https://github.com/ConstantBrum/ai-job-finder.git
cd ai-job-finder

# Install dependencies (when added)
npm install

# Run the agent
node src/index.js --help
```

## 📝 Coding Standards

### JavaScript Style

- Use ES6+ module syntax (`import`/`export`)
- Use async/await for asynchronous operations
- Include JSDoc comments for functions
- Follow existing code style and naming conventions
- Keep functions focused and single-purpose

### File Organization

- Core logic in `src/`
- Examples in `examples/`
- Documentation in root and inline comments
- Tests in `tests/` (when test infrastructure is added)

### Documentation

- Update README.md for user-facing changes
- Add JSDoc comments for new functions
- Include examples for new features
- Update CHANGELOG.md for notable changes

## 🧪 Testing

Currently, this project uses manual testing. When contributing:

1. Test your changes manually
2. Verify all existing functionality still works
3. Test edge cases and error conditions
4. Include test instructions in your PR

Future: We plan to add automated tests. Contributions to test infrastructure are welcome!

## 📤 Pull Request Process

1. **Fork the repository** and create a new branch
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** following the coding standards

3. **Test thoroughly** - Ensure your changes work as expected

4. **Update documentation** - README, inline comments, etc.

5. **Commit with clear messages**
   ```bash
   git commit -m "Add feature: brief description"
   ```

6. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

7. **Open a Pull Request** with:
   - Clear title and description
   - Reference to related issues
   - Summary of changes
   - Testing performed
   - Screenshots (if UI-related)

## ✅ Pull Request Checklist

Before submitting, ensure:

- [ ] Code follows project style guidelines
- [ ] Documentation is updated
- [ ] Manual testing completed
- [ ] Safety guidelines maintained
- [ ] No credentials or sensitive data in code
- [ ] Commit messages are clear
- [ ] PR description is complete

## 🔐 Security

If you discover a security vulnerability:

1. **Do NOT open a public issue**
2. Email the maintainers privately
3. Include details for reproduction
4. Allow time for a fix before public disclosure

## 📜 License

By contributing, you agree that your contributions will be licensed under the ISC License.

## 🙏 Recognition

Contributors will be recognized in:
- README.md contributors section (to be added)
- Release notes for significant contributions
- Project documentation

## 📞 Getting Help

- Open an issue for questions
- Check existing issues and documentation
- Be patient and respectful when asking for help

Thank you for contributing to make this project better! 🎉
