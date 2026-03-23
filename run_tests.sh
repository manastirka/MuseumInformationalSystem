#!/bin/bash
#
# Museum Information System - Test Runner
# =======================================
# Runs the automated testing agent with proper configuration
#

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}Museum System - Automated Test Runner${NC}"
echo -e "${CYAN}========================================${NC}"

# Configuration
BASE_URL="${BASE_URL:-http://localhost:5000}"
USERNAME="${TEST_USERNAME:-admin}"
PASSWORD="${TEST_PASSWORD:-admin123}"
REPORT_FILE="test_report_$(date +%Y%m%d_%H%M%S).json"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: Python 3 is required but not installed.${NC}"
    exit 1
fi

# Check if the app is running
echo -e "\n${YELLOW}Checking if application is running at ${BASE_URL}...${NC}"
if curl -s --connect-timeout 5 "$BASE_URL" > /dev/null 2>&1; then
    echo -e "${GREEN}Application is accessible!${NC}"
else
    echo -e "${RED}Warning: Application may not be running at ${BASE_URL}${NC}"
    echo -e "Starting the app first? Run: ./start_all.sh or python app.py"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Install dependencies if needed
echo -e "\n${YELLOW}Checking dependencies...${NC}"
pip3 install -q requests beautifulsoup4 colorama 2>/dev/null

# Check for Selenium (optional)
if python3 -c "import selenium" 2>/dev/null; then
    echo -e "${GREEN}Selenium available - browser testing enabled${NC}"
else
    echo -e "${YELLOW}Selenium not installed - browser testing disabled${NC}"
    echo -e "Install with: pip install selenium"
fi

# Run the tests
echo -e "\n${CYAN}Starting automated tests...${NC}"
echo -e "Base URL: ${BASE_URL}"
echo -e "Username: ${USERNAME}"
echo -e "Report:   ${REPORT_FILE}\n"

python3 automated_test_agent.py \
    --base-url "$BASE_URL" \
    --username "$USERNAME" \
    --password "$PASSWORD" \
    --output "$REPORT_FILE"

EXIT_CODE=$?

# Summary
echo -e "\n${CYAN}========================================${NC}"
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
else
    echo -e "${RED}Some tests failed. Check ${REPORT_FILE} for details.${NC}"
fi
echo -e "${CYAN}========================================${NC}"

# Show how to view the report
echo -e "\n${YELLOW}View report:${NC}"
echo -e "  cat ${REPORT_FILE} | python -m json.tool | less"
echo -e "  or open in browser: python -c \"import json,webbrowser; webbrowser.open('file://${PWD}/${REPORT_FILE}')\""

exit $EXIT_CODE
