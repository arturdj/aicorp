# AI Corp WebUI API Client - Makefile
# Common tasks for development and installation

.PHONY: install install-dev test clean lint format help uninstall check build

# Default target
help:
	@echo "AI Corp WebUI API Client - Available commands:"
	@echo ""
	@echo "Installation:"
	@echo "  install     - Install the aicorp command for current user"
	@echo "  install-dev - Install with development dependencies"
	@echo "  uninstall   - Comprehensive removal with cleanup options"
	@echo ""
	@echo "Development:"
	@echo "  test        - Run test suite"
	@echo "  lint        - Run code linting"
	@echo "  format      - Format code with black"
	@echo "  clean       - Clean build artifacts"
	@echo "  build       - Build distribution packages"
	@echo "  check       - Check aicorp installation status"
	@echo ""
	@echo "Usage:"
	@echo "  make install    # Quick install"
	@echo "  make uninstall  # Comprehensive removal"
	@echo "  make test       # Run tests"

# Installation targets
install:
	@echo "📦 Installing aicorp command..."
	pip3 install -e . --user
	@echo "✅ Installation complete!"
	@echo ""
	@echo "Test with: aicorp --help"
	@echo "If command not found, add ~/.local/bin to your PATH"

install-dev:
	@echo "📦 Installing with development dependencies..."
	pip3 install -e ".[dev]" --user
	@echo "✅ Development installation complete!"

uninstall:
	@echo "🗑️  Running comprehensive uninstall..."
	./scripts/uninstall.sh

# Development targets
test:
	@echo "🧪 Running tests..."
	python3 -m pytest tests/ -v

lint:
	@echo "🔍 Running linting..."
	python3 -m flake8 src/
	python3 -m mypy src/

format:
	@echo "🎨 Formatting code..."
	python3 -m black src/ tests/

clean:
	@echo "🧹 Cleaning build artifacts..."
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	@echo "✅ Cleaned successfully"

# Quick development workflow
dev: install-dev test lint
	@echo "🚀 Development setup complete!"

# Build distribution packages
build:
	@echo "📦 Building distribution packages..."
	python3 -m build
	@echo "✅ Build complete - check dist/ directory"

# Check if aicorp command is working
check:
	@echo "🔍 Checking aicorp installation..."
	@which aicorp || echo "❌ aicorp not found in PATH"
	@aicorp --help > /dev/null && echo "✅ aicorp command working" || echo "❌ aicorp command failed"
