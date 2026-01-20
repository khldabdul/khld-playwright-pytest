#!/bin/bash
# Local report generation script
# Generates Allure report from test results

set -e

ALLURE_RESULTS_DIR="${1:-test-results/allure-results}"
ALLURE_REPORT_DIR="${2:-test-results/allure-report}"

echo "========================================"
echo "Generating Allure Report"
echo "========================================"
echo "Results: ${ALLURE_RESULTS_DIR}"
echo "Report: ${ALLURE_REPORT_DIR}"
echo "========================================"

# Check if Allure is installed
if ! command -v allure &> /dev/null; then
    echo "Error: Allure is not installed."
    echo ""
    echo "Install Allure using one of these methods:"
    echo ""
    echo "macOS:"
    echo "  brew install allure"
    echo ""
    echo "Linux:"
    echo "  wget https://github.com/allure-framework/allure2/releases/download/2.25.0/allure-2.25.0.tgz"
    echo "  tar -xzf allure-2.25.0.tgz"
    echo "  export PATH=\$PATH:\$(pwd)/allure-2.25.0/bin"
    echo ""
    echo "Windows:"
    echo "  scoop install allure"
    echo ""
    exit 1
fi

# Check if results exist
if [ ! -d "${ALLURE_RESULTS_DIR}" ]; then
    echo "Error: Results directory not found: ${ALLURE_RESULTS_DIR}"
    echo "Run tests first: pytest --alluredir=${ALLURE_RESULTS_DIR}"
    exit 1
fi

# Generate report
echo "Generating report..."
allure generate "${ALLURE_RESULTS_DIR}" --clean -o "${ALLURE_REPORT_DIR}"

echo ""
echo "Report generated successfully!"
echo ""
echo "To view the report, run:"
echo "  allure open ${ALLURE_REPORT_DIR}"
echo ""
echo "Or open in browser:"
echo "  open ${ALLURE_REPORT_DIR}/index.html"
echo ""
