FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy

WORKDIR /app

# Copy dependency files first for better caching
COPY pyproject.toml setup.py ./

# Install Python dependencies
RUN pip install --no-cache-dir -e .

# Copy application code
COPY apps/ apps/
COPY config/ config/
COPY infrastructure/ infrastructure/
COPY pages/ pages/
COPY conftest.py pytest.ini ./

# Create test results directory
RUN mkdir -p test-results

# Default command runs all tests
CMD ["pytest", "apps/", "-v", "--alluredir=test-results/allure-results"]
