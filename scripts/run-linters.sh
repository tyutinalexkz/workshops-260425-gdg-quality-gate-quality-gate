#!/bin/bash
set -e

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}📦 Starting Code Quality Checks for Quality Gate Demo...${NC}"

# 1. 🔍 RUFF CHECKS
echo -e "\n${BLUE}--- [1/2] RUFF CHECKS ---${NC}"
echo -e "📝 Running Ruff format..."
ruff format .
echo -e "🔍 Running Ruff check..."
ruff check .

# 2. 📋 PYLINT CHECKS
echo -e "\n${BLUE}--- [2/2] PYLINT CHECKS ---${NC}"
echo -e "📋 Running Pylint..."
# Running on all python files in the root directory
if ! pylint *.py; then
    echo -e "\n${RED}❌ Pylint failed! Target score: 10/10.${NC}"
    exit 1
fi

echo -e "\n${GREEN}✅ All checks passed! Your code is looking great.${NC}"
